# Seed 02 — Identidade, operador e isolamento de dados

**Tipo:** Feature Spec / Requirements-First, backend + frontend. **Depende de:** spec 01. **ADRs:** 0001, 0002. **Regras:** BR-012, BR-018, BR-022.

## Problema/persona
OWNER e STAFF precisam acessar apenas seus dados em sessão segura. O MVP pode criar OWNER por script/admin controlado; não há signup público. Precisamos de contas, memberships, roles e logoff, com login responsivo no celular.

## Escopo IN
- Modelo `users`, `operators`, `operator_memberships`, roles e registro de eventos de login relevante; migrations e índices.
- Provisionamento seguro de OWNER somente por CLI/script restrito (nunca endpoint público sem proteção). Decisão sobre reset de senha deve ficar explícita antes do piloto; provisoriamente via procedimento administrativo seguro.
- Login/logout/me/csrf por Spring Security sessão JDBC, cookies HttpOnly/Secure/SameSite, validação CSRF, login throttle/rate limit, encerramento de sessão.
- API resolve activeOperator a partir de membership validado; negar todos endpoints business sem sessão/tenant válido.
- Tela `/login`, sessão e roteamento protegido; redirecionamento após login; expiração de sessão, 401/403; logout limpa cache TanStack Query.

## Não objetivos
Cadastro público, OAuth social, JWT localStorage, recuperação via SMS, múltiplos usuários com diferentes empresas sem seleção (permitir estrutura mesmo que piloto use 1).

## EARS mínimos
- WHEN usuário envia credenciais válidas THEN SHALL criar sessão segura, vincular operador ativo autorizado e devolver contexto mínimo.
- WHEN credenciais inválidas/força bruta THEN SHALL negar login sem distinguir qual campo falhou, aplicar rate limit.
- WHEN usuário STAFF tenta gerenciar equipe THEN SHALL receber 403 sem realizar mutação.
- WHEN sessão de operador A acessa UUID do operador B THEN SHALL retornar resposta neutra sem dados.
- WHEN logout acontece THEN SHALL invalidar sessão e CSRF, e o frontend SHALL limpar queries/caches privados.
- WHEN token CSRF estiver ausente/inválido em mutação THEN SHALL negar request.

## Design.md deve cobrir
Modelo usuário-membership-operador, decisões de auth, cookie/CSRF, filtros tenant no application service/repositories, adapters HTTP, testes de acesso cruzado, fluxo UI, tratamento de expiração de sessão, provisionamento e secrets.

## tasks.md deve incluir
Migrations, contas e hash, filtros, sessões, teste HTTP de auth e CSRF, testes com dois operadores, tela login, layout protegido, hooks, integração com contrato, CI, docs de bootstrap OWNER.

## Casos de aceitação obrigatórios
2 tenants, UUID de outro tenant, cache do browser após logout, senha inválida, sessão expirada, CSRF faltante, STAFF em OWNER-only, logs sem senha/telefone.
