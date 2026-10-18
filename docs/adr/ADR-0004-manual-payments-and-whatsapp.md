# ADR-0004 — Pix manual e WhatsApp por deep link no MVP

- Data: 2026-10-18
- Status: **Proposta**

## Decisão
- Sistema **não** cobra nem recebe valores dos turistas. Operador solicita e confere Pix externamente na própria chave/conta bancária; registra no ReservaMar um recebimento `PIX_MANUAL`.
- Ledger simples de recebimentos imutáveis com correções por lançamentos de ajuste referenciados (nunca apagar recebimento confirmado silenciosamente). Não armazenar comprovantes, CPF, documentos, credenciais ou cartão.
- Confirmação de reserva é ato de usuário autorizado, após verificar valor do sinal; qualquer exceção precisa de motivo. Pagamento pode ser lançado acima do sinal exigido até o total devido; valor excedente deve rejeitar ou exigir correção conforme regra do domínio.
- WhatsApp é **ação iniciada pelo operador** com deep link `https://wa.me/<telefone>` com conteúdo opcional codificado. Não enviar mensagens server-to-server, não configurar bots nem cobrar por uso da Meta no MVP.

## Futuro (spec separada)
Checkout com provider/merchant account do operador, webhooks assinados e idempotentes, reconciliação, chargebacks/estorno manual ou automático, opt-in e WhatsApp Cloud API oficial; exigirão ADRs específicas, orçamento e adequação jurídica.

## Riscos
Falso registro manual de recebimento: mitigado por identidade, autorização e auditoria; não equivale a conciliação bancária. Operador permanece responsável por conferir sua conta e cumprir política de cancelamentos/reembolsos.
