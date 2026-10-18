# Seed 07 — Preparar piloto real e estabilizar

**Depende de:** 01–06. **Objetivo:** segurança, operação previsível e feedback de 2–3 design partners.

## Escopo IN
- Hardening HTTP e autenticação: CSRF, cookies Secure, rate limit, cabeçalhos, redaction, escopo de tenants, controle de erros e timeouts.
- Confiabilidade: migrações em staging, backup PostgreSQL programado, **restauração testada**, verificação de logs e health/metrics; custo de hospedagem medido.
- Checklist QA: desktop e celular real, 390px, 200% zoom, teclado e contraste; correções de UX surgidas de piloto.
- Teste E2E completo: login, cadastros, saída, contato, booking concorrente, recebimento Pix manual, confirmação, cancelamento, dashboard.
- Procedimento onboarding assistido, política de privacidade/retencão revisada, canal de suporte, termos comerciais básicos a validar juridicamente.
- Testes de carga mínimos e objetivos de métricas, procedimento de incidentes e rollback.

## EARS mínimos
- WHEN importação de dados demo for feita THEN SHALL usar informações sintéticas sem dados de clientes reais.
- WHEN backup precisar ser restaurado em staging THEN SHALL retornar dados íntegros e relatar tempo real de recuperação.
- WHEN 10 reservas concorrentes disputarem 2 vagas THEN SHALL preservar capacidade com teste real e logs sem PII.
- WHEN user sem autorização tentar IDOR em qualquer entidade THEN SHALL receber resposta segura e sem dados de outro operador.
- WHEN monitoramento detectar falha crítica THEN SHALL registrar correlação e permitir diagnóstico sem dados pessoais.

## Artefatos do design.md
Plano de teste com matriz risco/impacto, arquitetura de deploy, restore exercise, modelo de secrets, plano de rollout e reversão, mockups corrigidos por feedback, limitações explícitas do piloto.

## tasks.md deve incluir
Hardening, observabilidade, restore test, E2E, QA mobile, documentação onboarding e suporte, testes cross-tenant, medição custos, gate de aceite por operador real.

## Não objetivos
SLA contratual 99.9% não medido, marketplace, automação Meta, banco/checkout, infraestrutura complexa.
