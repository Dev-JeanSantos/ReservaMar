---
inclusion: always
---
# Segurança, qualidade e privacidade (invioláveis)

## Proteção de dados
- HTTPS na produção; proteção CSRF em mutações com cookie de sessão; cookies Secure/HttpOnly/SameSite; sessão inválida em logout; rate limit para login; credenciais seguras; redigir testes de autorização negativos.
- Toda leitura/mutação de entidade de negócio deriva `tenantId` da sessão e usa filtro de domínio + SQL; teste com 2 tenants deve provar isolamento inclusive ao adivinhar UUID de outro.
- Dados pessoais mínimos. Dados demo sintéticos; nunca gravar senhas, telefone completo, tokens, dados de pagamento ou dados de cliente em logs/analytics.
- Política de privacidade, retenção e exclusão exigem decisão operacional antes da produção. LGPD por design, consentimento quando aplicável, acesso restrito, registro de incidentes.
- Não implementar fake auth ou botão login sem backend no ambiente real. Seed e usuários demo só `local/test`, nunca produção.

## Back-end
- Validar request DTO; mapear erros via Problem Details e códigos estáveis. Nunca responder stack trace ao consumidor.
- Testes reais com PostgreSQL/Testcontainers para locking, Flyway e queries tenant; teste concorrente obrigatório (10 requisições disputando últimas 2 vagas).
- Regra no domínio + transaction boundary no application service; sem lógica em controller ou componente UI.
- Exigir idempotência para criação de reservas e registro de recebimentos.
- Timeouts e tratamento de falhas para integrações externas futuras; não implementá-las no MVP.

## Front-end
- WCAG 2.2 AA como alvo, foco visível, teclado e leitor de tela nos fluxos-chave, contraste adequado, erros com texto, rótulos explícitos, botões >=44px na versão móvel.
- Estados loading/empty/error/success, feedback em duplicidade, network timeout, confirmação de exclusões/cancelamentos, validação server-side alinhada ao form.
- Sem armazenamento de sessão em localStorage; sem usar `dangerouslySetInnerHTML` para conteúdo externo.
- Valores monetários em pt-BR; datas no fuso local da saída com timezone claro; não deduzir disponibilidade como absoluta.

## Definition of Done
Aplicar `docs/quality/definition-of-done.md` a toda task. Não encerrar como 'feito' sem evidência de comandos executados, testes e revisão visual, nem inventar evidências.
