# ADR-0003 — Controle transacional da capacidade de saída

- Data: 2026-10-18
- Status: **Proposta**

## Contexto
Vagas são escassas. Duas requisições concorrentes podem tentar ocupar o mesmo último lugar, inclusive quando um atendente altera capacidade simultaneamente.

## Decisão
- Fonte de verdade: `departures.capacity_snapshot`; bookings ativos (`PENDING` com `hold_expires_at > now()` e `CONFIRMED`) consomem vagas.
- **Sem coluna `available_seats` mutável** na primeira versão, para evitar drift. Disponibilidade derivada em transação/consulta consistente.
- Criar, confirmar/cancelar, prorrogar hold e alterar capacidade de saída em transação Spring, com **row-level lock `SELECT ... FOR UPDATE` na `departures` antes de operar bookings**. Toda operação que altera alocação deve seguir a mesma ordem de locks.
- Operação revalida estado, vencimento, tenant, capacidade e idempotência. `POST /bookings` com chave de idempotência; lock impede overbooking; banco é a autoridade.
- Reservas começam `PENDING`, retêm capacidade por 12 h por padrão (parâmetro 1–24 h por operador, hipótese a validar), expiram mesmo se scheduler falhar (lazy evaluation por instante). `CONFIRMED` exige recebimento de sinal ou dispensa auditada.
- Expiração usa `Clock` injetável em teste. Serviço agendado muda status PENDING vencido para EXPIRED; não é fonte exclusiva da disponibilidade.
- Constraints DB: números >=0, capacidade >0, `seats>0`, unicidade/idempotência, escopo operador. Índices para saídas/status/prazo.

## Casos extremos que os testes devem cobrir
Duas chamadas com última vaga; 10 chamadas simultâneas por 2 vagas; chamada duplicada; hold expirado no exato instante; capacidade reduzida concorrente; confirmação após expiração; cancelamento de confirmado; status da saída CLOSED; acesso de tenant externo; relógio divergente.

## Alternativa rejeitada
`COUNT` da lista no frontend ou check-then-insert sem lock — sujeito a overbooking.

## Trade-off
Lock serializa escritas por saída, aceitável para operações pequenas; medir contenção no piloto.
