---
inclusion: always
---
# Produto — ReservaMar (codinome)

## Problema
Operadores de pescaria embarcada de pequeno porte agendam por WhatsApp e podem perder o controle de capacidade, datas, sinais, confirmação e comunicação. Hipótese ainda não validada; entrevistar operadores.

## Cliente pagante e personas
- **Admin do operador:** dono/gerente, paga assinatura no futuro; cadastra barcos, atividades e saídas; resolve conflitos, confere Pix.
- **Atendente:** registra clientes e reservas; acesso restrito aos recursos de seu operador.
- **Turista/pescador:** no MVP não acessa a plataforma; fala com o operador por WhatsApp.
- **Admin da plataforma:** suporte e provisionamento inicial; **não** deve ter acesso irrestrito aos dados de clientes no uso normal.

## North star
Confiabilidade da agenda: disponibilidade correta e reservas auditáveis, com pouco esforço no celular. Métricas piloto: taxa de reservas sem conflito, tempo de registro de reserva e número de operadores que concordam em pagar.

## Fluxo MVP
Operador entra → cadastra embarcação/atividade → cria uma saída → consulta vagas → cadastra cliente → faz reserva pendente (bloqueia vagas até deadline) → confere o Pix fora do app → registra recebimento manual e confirma → pode abrir WhatsApp do cliente via link → cancela quando necessário.

## Guardrails
Não é marketplace, OTA, sistema hoteleiro, gateway de pagamento nem central de mensagens. Não prometer receita garantida, integração Pix automática ou conformidade legal sem revisão.

## Design partners
Selecionar 2–3 operadores piloto para testar onboarding e fluxo. Recolher feedback de campo, autorizações e métricas, sem expor dados pessoais em demos.
