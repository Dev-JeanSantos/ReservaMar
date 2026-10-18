# ReservaMar — Design system e padrões de componentes

## Direção visual
Painel profissional, simples, confiável e legível em barcos, cais e escritórios, em telas pequenas. Não confundir com marketplace turístico. Nome comercial, logo e paleta são provisórios; validar identidade com design partners.

### Tokens CSS de referência
```css
:root {
  --brand-700: #07576B;     /* oceano / primária: verificar AA no texto */
  --brand-500: #087E8B;     /* foco/acento */
  --success-700: #136B4A;
  --warning-700: #8A5500;
  --danger-700: #B42318;
  --ink-900: #14212B;
  --ink-600: #4C5A64;
  --surface-0: #FFFFFF;
  --surface-50: #F5F8FA;
  --border-200: #CDD9DF;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --space-unit: 4px;
}
```
**Não assumir contraste AA automaticamente**: executar teste automático e avaliação visual com combinações usadas. Tema claro primeiro; dark mode apenas backlog. Tipografia sistema (`Inter` se auto-hospedada e licenciada; caso contrário system-ui). Base 16px, mínimo 14px para metadados sem prejudicar leitura, line-height >=1.4.

## Grid e breakpoints
- 360–599px: uma coluna, botões 44–48px de altura, navegação compacta, painel de saída em cards.
- 600–1023px: layout de tablet, cards agrupados, botões acessíveis.
- 1024px+: menu lateral persistente e listas em tabela com filtros.
- Conteúdo principal: largura máxima 1280px, gutters 16px mobile / 24–32px desktop.
- A interface deve funcionar com zoom 200% sem perda de informações ou interações críticas.

## Componentes comuns e estados
| Componente | Contrato visual e funcional |
|---|---|
| `PageHeader` | título, resumo, CTA de criação, breadcrumb se necessário |
| `AvailabilityMeter` | `ocupadas / capacidade`; texto e progress visual, nunca somente cor |
| `DepartureCard` | data/hora fuso, atividade, barco, vagas, status e ação |
| `BookingStatusBadge` | `PENDING` = `Aguardando sinal`, `CONFIRMED` = `Confirmada`, `EXPIRED` = `Expirada`, `CANCELLED` = `Cancelada` |
| `CurrencyField` | exibe BRL; converte input seguro em centavos; rejeita valores inválidos |
| `PhoneField` | máscaras amigáveis, normalização backend para E.164 |
| `DateTimeField` | data e hora local clara; conversão para UTC ao salvar |
| `ConfirmDialog` | obrigatório em cancelamentos/reversão de pagamentos, detalhando irreversibilidade |
| `ProblemBanner` | mensagem clara a partir de `problem.code`, `correlationId` opcional para suporte |
| `EmptyState` | estado sem dados e CTA contextual |
| `Skeleton/Spinner` | carregamento com descrição acessível |

## Princípios de formulários
- Campo obrigatório marcado, label sempre visível, exemplos (placeholder não substitui label).
- Validação no blur / submit, erros próximos ao campo e resumo quando apropriado; preservar inputs em 409/422.
- Ação primária fixa dentro da viewport em mobile se houver formulário longo e sem encobrir teclado.
- Data/hora mostra fuso `Horário de Brasília` quando aplicável à saída (usar timezone armazenada, não supor UTC do navegador).
- Exibir centavos e formatação BRL; antes de confirmar reserva mostrar `2 vagas x R$ 300,00 = R$ 600,00`, `Sinal: R$ 180,00`.
- Mensagens sem jargão técnico: 409 `As vagas mudaram. Restam 2. Ajuste a reserva.`; erro 500 `Não foi possível concluir. Tente novamente.` e suporte ID.

## Navegação básica
- Menu: Visão geral / Saídas / Reservas / Clientes / Embarcações / Atividades; Equipe e Configurações somente OWNER.
- Dashboard: próximas saídas, reservas pendentes, vencimentos e últimas confirmações (não BI).
- Saídas: cards por data com ocupação, filtros e CTA criar saída.
- Detalhe da saída: disponibilidade + lista de reservas + CTA reservar.
- Reserva: cadastro cliente → seats → revisão preço/sinal → confirmação criação PENDING → instruções para contato/pagamento.
- Pagamentos: histórico e ação `Registrar sinal recebido` com informação clara de conferência manual.

## Acessibilidade e QA visual
- Alvo WCAG 2.2 AA; contraste alvo 4.5:1 texto normal, 3:1 texto grande, foco visível.
- Navegação por teclado, labels ARIA apropriados, announcements para status da ação e erros.
- Screenshots de teste 390x844 e 1366x768; considerar loading, vazio, erro de rede, 409 e diálogos.
- Testar 200% zoom, tela estreita, Safari iOS e Chrome Android se acessíveis.
- Não usar layout de landing page/marketing dentro do painel.

## Dependências e padrões
React + TypeScript strict, Tailwind + Radix/shadcn/ui auditado, iconografia Lucide, React Hook Form/Zod. Layout e copy pt-BR. Design tokens definidos globalmente, sem hex hardcoded disperso na UI.
