# ADR-0002 — Isolamento lógico por tenant + autenticação por sessão

- Data: 2026-10-18
- Status: **Proposta**

## Contexto
Operadores concorrentes compartilham infraestrutura e não podem observar ou modificar informações uns dos outros. MVP exige login seguro com baixo custo.

## Decisão
- `operators` representa tenant; `operator_memberships` vincula usuário global a operador e papel (`OWNER`/`STAFF`). Seleção de operador ativo fica na sessão, verificada a cada request.
- Todas as entidades de negócio possuem `operator_id` obrigatório; relações e constraints devem impedir foreign key cruzando tenants. `operators` é o tenant root.
- Tenant **nunca** vem de parâmetro confiado ao cliente; servidor resolve membership e escopo. Acesso a UUID fora do escopo responde `404` não revelador, salvo política de segurança própria.
- Spring Security por cookie de sessão `HttpOnly`, `Secure`, `SameSite=Lax` com HTTPS e **CSRF ativo**; persistência sessão JDBC. Frontend servido no mesmo domínio para reduzir CORS. Password hash Argon2id/BCrypt seguro; rate-limit no login.
- Sem login social, JWT em localStorage ou contas de turista no MVP. Primeiro OWNER criado por provisionamento administrativo protegido; convites STAFF apenas após spec própria.
- Logs e erros não incluem PII nem segredos; dados mínimos; exportação/eliminação LGPD planejada antes de piloto real.

## Alternativas
- DB por tenant: maior isolamento e backup individual, mas alto custo operacional.
- Row-level security PostgreSQL: defesa adicional potencial, porém aumenta cuidados com pool e sessão; avaliar numa ADR futura sem substituir escopo de aplicação.
- OAuth gerenciado: bom futuro, mas dependencia e custo adicionais para MVP.

## Evidência obrigatória
Testes de integração com pelo menos 2 operadores para leitura, edição, cancelamento, IDOR, queries agregadas e membros com papéis distintos. CSRF e cookies inspecionados em testes HTTP.
