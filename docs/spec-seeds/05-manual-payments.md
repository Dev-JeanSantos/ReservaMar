# Seed 05 — Registro manual de sinal Pix e confirmação

**Depende de:** 04. **ADRs:** 0002, 0004. **Regras:** BR-007–009, BR-013–015, BR-022.

## Problema
O sinal é recebido diretamente pelo operador (fora do ReservaMar). O sistema precisa registrar o fato sem fingir integração bancária, permitir ajustes rastreáveis e confirmar reservas corretamente.

## Escopo IN
- Ledger `payment_entries` tenant-scoped: `RECEIPT` positivo e `REVERSAL` referenciando recebimento (ajuste negativo), método `PIX_MANUAL`, valor em centavos, referência opcional, data/hora, registrador, razão de reversão.
- `POST /bookings/{id}/payment-entries` idempotente e autorizado, com prevenção de valor inválido/acima do total; `GET` histórico; reversão por lançamento compensatório.
- Serviço confirmar reserva `PENDING` ainda válida quando recebimento líquido >= sinal mínimo ou `depositWaived=true` com motivo do usuário autorizado. Nunca confirmar automaticamente baseado em documento, texto ou registro de recebimento sem ação do atendente.
- Ao cancelar com recebimento, manter histórico e mensagem de operação externa pendente (`Verifique eventual reembolso fora do sistema`).
- UI: botão `Registrar pagamento recebido`, valor, revisão, confirmação, histórico auditável, botão `Confirmar reserva`, `dispensar sinal` com motivo, estados erro/duplicidade.

## EARS mínimos
- WHEN atendente registra PIX_MANUAL após conferir sua conta bancária THEN SHALL persistir recebimento com ator, data e valor, sem efetuar transação financeira.
- WHEN repete mesmo request/key THEN SHALL responder com mesmo entry sem duplicar valor.
- WHEN valor é <=0 ou ultrapassa saldo devido THEN SHALL rejeitar 422/409 adequado.
- WHEN PENDING ainda válido e sinal suficiente THEN SHALL permitir confirmação explícita e mudar para CONFIRMED mantendo vagas.
- WHEN sinal insuficiente e não há dispensa THEN SHALL rejeitar confirmação 409 com saldo necessário.
- WHEN reserva expirou THEN SHALL rejeitar confirmação mesmo que receba pagamento manual atrasado, e sinalizar pendência para resolução.
- WHEN recebimento precisar correção THEN SHALL registrar REVERSAL vinculada e motivada, sem deletar trilha original.
- WHEN cliente cancela com pagamentos THEN SHALL preservar ledger e informar que reembolso não foi executado.

## Design.md deve cobrir
Esquema ledger, tipo de ajuste, idempotência, authorization, atomicidade entre pagamento/confirmação e inventory lock, formas de impedir double spend e rollback, telas de revisão, linguagem que diferencia `registrado` de `confirmado pelo banco` (não há verificação bancária).

## tasks.md deve incluir
DB/ledger; regras/ports; tests de valores, duplicidade, autorização, expiração; endpoints e OpenAPI; UI forms, visual de saldo e avisos; E2E recebimento→confirmação e cancelamento sem estorno.

## Não objetivos
Integração bancária, Pix cobrança, gateway, webhooks, cartão, split, cobranças de assinatura SaaS, reembolso monetário.
