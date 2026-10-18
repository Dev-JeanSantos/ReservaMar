# Seed 04 — Clientes, reservas e inventário transacional

**Depende de:** 03. **ADRs:** 0002, 0003. **Regras:** BR-001–013, 016, 018–023.

## Problema
Atendente registra uma reserva de X vagas para saída compartilhada, sem overbooking, inclusive em atualizações simultâneas pelo mesmo ou outro usuário.

## Escopo IN
- Clientes tenant-scoped: nome, telefone; criar, buscar com limites e editar dados não sensíveis (com trilha).
- `Booking` com 1 titular e quantidade de passageiros; `PENDING`, `CONFIRMED`, `EXPIRED`, `CANCELLED`, idempotência.
- `POST /bookings` atômico: bloquear row da Departure, verificar status, holds válidos e capacidade, calcular snapshots de preço/sinal e prazo, criar booking, auditar e devolver 201.
- Cancelar e expirar; confirmação após recebimento/waiver será finalizada na seed 05, mas state machine/teste preparado.
- Job de expiração e lazy evaluation; `Clock` para testes e tempo de servidor; gateway de aplicação para cálculo de disponibilidade.
- UI: selecionar saída, cliente, assentos e revisão, botão criar, tela detalhe/pendência, conflito 409, cancelamento com motivo.

## EARS mínimos
- WHEN existem 2 vagas e chegam 10 requests simultâneos para 1 assento THEN SHALL persistir no máximo 2 reservas ativas e rejeitar o restante com 409.
- WHEN duas requisições possuem mesma Idempotency-Key e mesmo payload THEN SHALL retornar mesma reserva, sem consumir vagas adicionais.
- WHEN mesma Idempotency-Key vem com payload diferente THEN SHALL retornar 409 de reutilização indevida.
- WHEN hold expira THEN SHALL liberar vagas mesmo antes de job rodar; pedido de confirmação não pode ressuscitar booking expirado.
- WHEN cancelamento legítimo ocorre THEN SHALL liberar vagas, manter auditoria e dados necessários.
- WHEN cliente/saída pertence a outro tenant THEN SHALL rejeitar sem data leak.
- WHEN capacity alterada concorrentemente THEN SHALL manter soma das vagas ativas <= capacitySnapshot.
- WHEN API retorna 409 de vagas THEN UI SHALL mostrar quantidade atual e permitir alteração preservando formulário.

## Design.md deve cobrir
Fluxo de locks SQL `SELECT FOR UPDATE`, índices, transação Spring, pseudo-algoritmo, state machine, deadline UTC, API idempotency persistence, comandos UI, queries de invalidação, retries, casos de erro e testes Testcontainers concorrentes.

## tasks.md deve incluir
Migrations e constraints; domain invariants; repositórios lock; services transacionais; expiração; testes concorrência e idempotência; endpoints, OpenAPI e tipos; UI mobile, erro 409, E2E 2 operadores.

## Não objetivos
Checkout Pix, reserva iniciada por turista, múltiplos titulares, documentos individuais de passageiros, remarcar/cancelar com regras financeiras automáticas.
