---
inclusion: auto
name: frontend-design
description: UI UX responsive design system React TypeScript ReservaMar forms mobile accessibility operator dashboard
---
# Frontend, padrões visuais e UX

`docs/design/design-system.md` e `docs/design/user-journeys.md` são fontes detalhadas.

- UI primeiro para telefone de operadores: botões grandes, interação com uma mão, tabela desktop e cartões móveis, fluxo de registrar reserva em até 4 passos.
- Paleta identidade marinha: azul oceano (ação), turquesa (reserva disponível), neutros e vermelho de alerta. Não usar apenas cor para comunicar estados.
- Reutilizar componentes via design system com variantes: Button, Input, CurrencyField, DateTimeField, StatusBadge, AvailabilityMeter, BookingCard, ConfirmDialog, EmptyState, ErrorState, PageHeader.
- Texto em pt-BR direto, claro: `Vagas disponíveis`, `Reservar vagas`, `Aguardando sinal`, `Confirmada`, `Expirada`, `Cancelada`.
- Rotas do MVP: `/login`, `/dashboard`, `/boats`, `/activities`, `/departures`, `/departures/:id`, `/bookings/new`, `/bookings/:id`, `/customers`, `/settings/team` (OWNER).
- Responsivo, mobile 360–430px com navegação inferior ou menu compacto; desktop >=1024px com sidebar; 768px tablet.
- Filtros por dia/status; keyboard navigation, campos com errors, Toast informativo, diálogos de confirmação, skeletons e estados vazios.
- Sem 'mock data' em telas de produção depois de integradas; MSW limitado a desenvolvimento/testes. Backend fonte da verdade, inclusive taxa de ocupação.
