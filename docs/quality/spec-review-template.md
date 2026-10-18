# Template para revisão de cada Feature Spec no Kiro

## Requisitos (`requirements.md`)
- Nome da spec, objetivo, persona, escopo IN/OUT e dependências anteriores.
- IDs REQ estáveis e histórias `Como <papel>, quero <capacidade>, para <benefício>`.
- Critérios observáveis EARS `WHEN... SHALL...`, erros, roles, cross-tenant, concorrência e acessibilidade quando aplicável.
- Tabela `BR-xxx → REQ-yy → cenário de teste`.
- Lista de decisões abertas; Kiro deve solicitar aceite, não preenchê-las implicitamente.
- **Gate humano: APROVADO / AJUSTAR.**

## Design (`design.md`)
- Visão de componentes com diagramas Mermaid (arquitetura + sequência do fluxo principal e erro principal).
- Backend: endpoints DTO, domínio, casos de uso, ports/adapters, autorização, transações, locks, migrations, índices e rollback.
- Frontend: mapa de rotas, componentes, states, responsividade, form schema, chamadas API, estados de cache/refetch, labels e acessibilidade.
- Contratos de eventos (se houver; MVP não usa eventos distribuídos), horas/timezones, tipos monetários, exceptions e Problem Details.
- Test plan unit/integration/E2E incluindo fronteiras e casos extremos.
- Alternativas, tradeoffs, custos operacionais e riscos.
- **Gate humano: APROVADO / AJUSTAR.**

## Tasks (`tasks.md`)
Cada item com `- [ ]` deve dizer:
- ID e descrição curta, spec/REQ e BR correspondentes.
- Dependências, arquivos esperados, passos backend/front/DB, comandos de teste.
- Critérios de conclusão objetivos e outputs observáveis.
- Separar tarefas apenas independentes (nunca migrar schema e codificar consumidores do schema em paralelo sem coordenação).
- Nunca marcar concluída com teste não executado; registrar bloqueios e evidência real.
- **Gate humano: PRONTO PARA EXECUÇÃO / AJUSTAR.**

## Relatório padrão após task
```text
Spec / Task:
Requisitos atendidos:
Arquivos criados/alterados:
Comandos executados (saída/resumo):
Testes novos e casos relevantes:
Comportamento UI verificado (viewport/device):
Segurança/tenant/concorrência verificados:
Impacto contrato e migrations:
Pendências ou bloqueios:
```
