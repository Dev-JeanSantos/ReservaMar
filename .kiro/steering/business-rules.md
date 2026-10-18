---
inclusion: always
---
# Regras de negócio obrigatórias (IDs estáveis)

Leia também `docs/domain/business-rules-and-states.md`. IDs BR-xxx DEVEM aparecer nos acceptance criteria e testes.

- **BR-001** Uma `Departure` pertence a exatamente um `Operator` e uma `Boat`; `Activity` também pertence ao mesmo operador.
- **BR-002** Capacidade disponível = `capacitySnapshot - soma(seats de bookings PENDING válidos ou CONFIRMED)`. Nunca menor que zero. Expiradas não consomem vagas mesmo se limpeza agendada atrasar.
- **BR-003** Uma reserva exige `seats` inteiro >=1 e <= vagas disponíveis; reservar e verificar capacidade na **mesma transação no PostgreSQL**, com lock da `Departure` (ou serialização equivalente demonstrada por teste real de concorrência).
- **BR-004** A capacidade, preço por pessoa e sinal mínimo são **snapshots por saída**. Edições em `Boat`/`Activity` não alteram saídas existentes.
- **BR-005** Reserva nova inicia `PENDING` com `holdExpiresAt` definido pelo servidor; prazo padrão **12 horas**, parametrizável por operador **entre 1 e 24 horas**, hipótese a validar com pilotos.
- **BR-006** Uma reserva PENDING expirada não confirma, não é contada no saldo e pode ser movida para `EXPIRED` por rotina ou lazy evaluation, com transação protegida.
- **BR-007** Só um usuário autorizado pode confirmar; confirmação exige pagamento registrado suficiente para o sinal exigido OU exceção `depositWaived=true` com motivo auditável (quando sinal=0, confirmar manualmente é permitido).
- **BR-008** Uma reserva `CONFIRMED` continua consumindo vagas até ser `CANCELLED`.
- **BR-009** Cancelamento pode ocorrer em `PENDING` ou `CONFIRMED`, com motivo obrigatório e trilha de auditoria; valores recebidos NÃO são automaticamente estornados.
- **BR-010** Saídas `CANCELLED` ou `CLOSED` rejeitam novas reservas; cancelamento de saída exige tratar reservas ativas numa única operação consistente e sinalizar pendências financeiras.
- **BR-011** `Departure.startAt` deve ser futura quando criada; guardar instante UTC e timezone da localidade, padrão `America/Sao_Paulo`; datas em UI local.
- **BR-012** Operador só acessa registros do seu tenant. Identificador de tenant é resolvido pelo backend a partir da sessão autorizada; nunca confiar em `operatorId` enviado pelo navegador.
- **BR-013** Valores em **centavos BRL**; `totalCents = seats * pricePerSeatCents` com checagem de overflow; `requiredDepositCents` definido na saída e escalado pelo número de vagas (ex.: sinal por pessoa); snapshot na reserva.
- **BR-014** Sinal do Pix: **conferência manual fora do sistema** e inclusão de registro de recebimento no aplicativo; anotar método `PIX_MANUAL`, valor, data, usuário registrador, referência opcional. Não inferir quitação por texto/comprovante ou screenshot.
- **BR-015** Não permitir recebimento duplicado por `Idempotency-Key` (por operador + operação); não aceitar valor <=0; pagamento incorreto é compensado por lançamento de ajuste, não apagado sem trilha.
- **BR-016** Clientes têm nome e telefone E.164 ou formato brasileiro validável; exigir consentimento/aviso adequado antes de usar dados para contatos não transacionais. Não coletar documentos dos passageiros no MVP.
- **BR-017** Link de WhatsApp abre no aparelho o número do cliente com mensagem pré-preenchida, após ação explícita do atendente; nenhum envio automático pelo servidor.
- **BR-018** Usuários têm papéis `OWNER` e `STAFF`; `OWNER` gerencia usuários/configurações/cancelamento de saídas; `STAFF` cadastra clientes/reservas, registra pagamentos e confirma reserva, mas não administra equipe.
- **BR-019** Entradas duplicadas precisam de idempotência para `POST /bookings`; repetir a mesma chave/corpo devolve a mesma reserva; mesma chave/corpo diferente retorna conflito.
- **BR-020** O operador não pode reduzir a capacidade da saída abaixo das vagas ativas. Edição concorrente deve preservar a invariante.
- **BR-021** Na UI, disponibilidade exibida é informativa; ao confirmar criação, o servidor recalcula e devolve `409` com vagas atuais caso tenha mudado.
- **BR-022** Qualquer alteração de status, valor, prazo, capacidade ou pagamento registra ator, timestamp, tenant, objeto e mudança relevante sem registrar PII desnecessária nos logs.
- **BR-023** A partir de `Departure.startAt` (segundo relógio do servidor), não aceitar novas reservas nem prorrogar holds; saídas canceladas alteram reservas ativas para `CANCELLED` de forma transacional e preservam histórico financeiro.

## Questões a validar com design partners
- Janela de reserva de 12h; se o sinal mínimo é valor fixo por pessoa ou percentual; se há saídas sem sinal; política de remarcação e cancelamento; necessidade de reservas de fretamento inteiro; usuários com acesso a vários operadores; limite de embarcações por plano; ponto exato da confirmação operacional.
- **Não codificar respostas presumidas como regras definitivas.** Onde uma regra não estiver definida, descrever uma proposta e pedir aceite humano.
