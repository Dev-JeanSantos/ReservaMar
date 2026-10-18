# Jornada e protótipos textuais de telas (fonte para design.md do Kiro)

## Jornada A — primeiro acesso e configuração
1. OWNER recebe acesso por provisionamento controlado (não cadastro público no MVP).
2. Abre `/login`, autentica, escolhe operador se tiver mais de um membership.
3. Dashboard vazio mostra passos 1) Adicionar embarcação, 2) Criar atividade, 3) Publicar saída.
4. `BoatForm` recebe nome e capacidade inteira >0; `ActivityForm` recebe título e descrição.
5. `DepartureForm`: embarcação, atividade, início local, vagas/capacidade (<= capacidade do barco), preço por pessoa, sinal por pessoa, horário/estado.
6. Dashboard passa a exibir próxima saída e CTA `Adicionar reserva`.

## Jornada B — registrar reserva pelo WhatsApp
1. Atendente recebe cliente pelo WhatsApp, abre detalhe de saída com `4 de 6 ocupadas`.
2. Toca `Nova reserva` e escolhe/cadastra contato; define 2 vagas.
3. Revisão: preço, sinal, regra de 12h de bloqueio e limite. Submete com idempotência.
4. Resposta 201 mostra `Aguardando sinal`, data limite, total e botão `Abrir WhatsApp`.
5. Falha concorrente 409: vagas atualizadas, sem perda de contato digitado; usuário ajusta ou cancela.
6. Após conferir Pix na conta, registra manualmente recebimento, vê saldo e clica `Confirmar reserva`.
7. UI detalha confirmação; histórico mostra ator e horário.

## Jornada C — cancelamento
1. Detalhe da reserva mostra nome e status, vagas e pagamentos registrados.
2. Atendente clica `Cancelar reserva`, informa motivo e confirma no diálogo.
3. API valida role/tenant/estado e libera vagas; pagamento existente permanece no histórico com mensagem `Verificar reembolso fora do sistema`.
4. A UI atualiza dashboard/saída por invalidation de queries, não por mutação local improvisada.

## Jornada D — expiração
1. O operador vê reserva `Aguardando sinal até 18:00`.
2. Ao expirar sem confirmação, disponibilidade já volta a aumentar mesmo antes da rotina de limpeza.
3. Ao tentar confirmar, backend responde `409 BOOKING_HOLD_EXPIRED`; UI indica que a vaga foi liberada e exige criar nova reserva sujeita a saldo.
4. Se houver recebimento manual lançado, app destaca pendência de reconciliação, sem confirmação automática.

## Jornada E — interrupções e riscos operacionais
- Perda de rede ao enviar reserva: UI não repete com nova idempotency key; permite retry com a **mesma chave** até resposta inequívoca.
- Cancelamento de saída com reservas confirmadas: OWNER recebe aviso da quantidade e pendências financeiras antes de confirmar.
- Dois operadores/tenants: logout/login não pode preservar queries de dados privados em cache; limpar cache de query ao trocar sessão/tenant.
- Teclado e zoom: focos, modais e botões acessíveis em viewport móvel.

## Wireframe lógico mobile (não visual final)
```text
┌─────────────────────────────────┐
│ ReservaMar        ☰             │
│ Boa tarde, Operador             │
│ [12 Reservas] [3 Pendentes]     │
│                                 │
│ Próximas saídas                 │
│ ┌─────────────────────────────┐ │
│ │ Sáb 24/out 05:00            │ │
│ │ Pescaria Alto-mar            │ │
│ │ 4 de 6 vagas ocupadas        │ │
│ │ [Ver detalhes] [Reservar]    │ │
│ └─────────────────────────────┘ │
│                                  │
│ Início | Saídas | Reservas       │
└─────────────────────────────────┘
```

O Kiro deve produzir `design.md` por feature com componentes, variações de estado e descrição de screenshots esperados; não começar a estilização sem fluxo de dados real.
