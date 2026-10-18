# Seed 03 — Cadastro de embarcações, atividades e saídas

**Depende de:** 02. **ADRs:** 0001, 0002, 0003. **Regras:** BR-001, 004, 010, 011, 020, 022, 023.

## Problema
Operador precisa configurar barco, produto (pescaria compartilhada) e saídas com vagas, horário, preço e sinal.

## Escopo IN
- CRUD com inativação (soft deactivate) de Boat e Activity, ambos tenant-scoped.
- Criar, listar, detalhar e atualizar Departure (status SCHEDULED/CLOSED/CANCELLED), snapshots de capacidade, preço e sinal por passageiro; validações server-side.
- Lista filtrável por data/status, cards mobile e tabela desktop, formulários com RHF/Zod, feedback/empty/error/loading.
- Owner cancela saída; STAFF edita dados permitidos exceto cancelar/gerir configurações. Confirmar comportamento de fechamento da saída.
- Interface `GET /departures/{id}/availability` exibe ocupação. Inicialmente occupied=0 sem booking; integre após seed 04.

## EARS mínimos
- WHEN OWNER cria Boat com capacidade <1 THEN SHALL rejeitar campo com erro explicativo.
- WHEN operador cria Departure com barco/atividade do outro tenant THEN SHALL rejeitar sem revelar dados.
- WHEN cria Departure com data passada THEN SHALL rejeitar 422.
- WHEN capacidade da saída excede capacidade do barco THEN SHALL rejeitar.
- WHEN preço <0 ou sinal por pessoa > preço por pessoa THEN SHALL rejeitar.
- WHEN Boat ou Activity é editado após a saída criada THEN SHALL preservar snapshots na Departure.
- WHEN a saída CLOSED/CANCELLED ou já iniciada recebe pedido de reserva THEN SHALL bloquear (integração seed 04).
- WHEN OWNER cancela saída com reservas ativas THEN SHALL cancelar também tais reservas em transação consistente e preservar lançamentos de pagamento (integração seed 04/05).
- WHEN redução de capacidade abaixo das vagas ativas for solicitada THEN SHALL falhar 409 sem mudança (após integração seed 04).

## Design.md deve cobrir
DDL, constraints, lifecycle, lock da Departure, endpoint schema, timezone local → UTC, seleção de dados, desenho das telas, UX de cancelamento com reservas e pendências, índices e testes.

## tasks.md deve incluir
Migrations; domain/ports/adapters; handlers REST; testes tenant e status; OpenAPI; clientes tipados e forms React; viewport 390px e desktop; E2E criar saída.

## Não objetivos
Mapas, GPS, múltiplos barcos na mesma saída, fretamento exclusivo, precificação dinâmica, fotos/galeria, cancelamento bancário.
