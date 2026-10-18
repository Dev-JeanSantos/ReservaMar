# Ordem das Feature Specs Kiro e dependências

| Ordem | Spec / seed | Dependência | Slice demo verificável |
|---|---|---|---|
| 01 | `.kiro/specs/01-foundation-bootstrap/requirements.md` | nenhuma | API e UI iniciam, CI/compose, OpenAPI, erro padrão |
| 02 | `docs/spec-seeds/02-auth-tenancy.md` | 01 | OWNER entra e isolamentos por operador passam |
| 03 | `docs/spec-seeds/03-resources-departures.md` | 02 | cria embarcação, atividade e saída |
| 04 | `docs/spec-seeds/04-customers-bookings.md` | 03 | reserva pendente com controle atômico de vagas |
| 05 | `docs/spec-seeds/05-manual-payments.md` | 04 | registra sinal e confirma reserva |
| 06 | `docs/spec-seeds/06-dashboard-communications.md` | 04 + 05 | painel e WhatsApp manual no celular |
| 07 | `docs/spec-seeds/07-pilot-hardening.md` | 01–06 | testes de regressão, segurança, backups e piloto |
| 08 | `docs/spec-seeds/08-future-integrations.md` | validação comercial | pagamentos/WhatsApp integrados, futuramente |

## Vertical slice obrigatório
Ao final de cada feature, backend + frontend + contrato + testes + UX + docs devem funcionar de ponta a ponta. Ex.: a spec 04 só está completa com tela que cria reserva de verdade e trata HTTP 409, não só com CRUD de API.

## Gate de investimento
Antes de 04 (bookings), ideal ter 2–3 design partners que confirmem a dor. Em paralelo: coletar feedback e validar preço; não inflar escopo por sugestão de único operador.

## Decisões abertas a confirmar
- `OPEN-01`: nome comercial/marca.
- `OPEN-02`: sinal fixo por pessoa vs percentual; baseline assume por pessoa.
- `OPEN-03`: prazo de hold 12h como ponto de partida.
- `OPEN-04`: método de provisionamento OWNER e e-mail transacional.
- `OPEN-05`: política de privacidade, retenção, atendimento a titulares.
- `OPEN-06`: se STAFF pode cancelar reserva confirmada; baseline sim com motivo.
- `OPEN-07`: hospedagem e observabilidade do piloto conforme orçamento.
