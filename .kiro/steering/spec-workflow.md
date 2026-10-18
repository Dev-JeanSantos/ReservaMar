---
inclusion: always
---
# Processo obrigatório Kiro

## Ordem de precedência
1. Regras de segurança, privacidade e invariantes de negócio explicitadas em `.kiro/steering/security-quality.md` e `business-rules.md`.
2. ADRs de status `Accepted` (propostas precisam de aceite humano).
3. Specs cujas fases `requirements/design/tasks` foram revisadas e aprovadas pelo proprietário.
4. Briefs `docs/spec-seeds/` e arquitetura de referência.
5. Preferências de implementação locais.
**Se houver conflito, NÃO supor: apresentar proposta de resolução antes de codificar.**

## Gate para cada feature
1. Ler `docs/spec-seeds/NN-*.md` e referências; gerar `requirements.md` com user stories e EARS, IDs estáveis e cenários de erro.
2. Mostrar critérios verificáveis, fluxos de backend E frontend. Aguardar aprovação humana.
3. Gerar `design.md` com componentes, tabelas, interfaces, sequência, endpoints e estrutura visual, riscos, teste de concorrência e NFRs. Aguardar aprovação.
4. Gerar `tasks.md` com subtarefas backend, frontend, contrato, migração, testes, CI, UX, segurança e documentação, links para requirements; explicar dependências.
5. Executar tasks em incrementos pequenos. Para cada task cumprir `docs/quality/definition-of-done.md`; nenhum teste fictício, nenhuma task marcada concluída sem validação.
6. Atualizar docs e ADR quando houver decisão nova; impedir feature creep.

## Padrões de aceite
- Critério EARS: `WHEN <evento> THEN the system SHALL <comportamento observável>`; redigir em português se preferir, mas preservar WHEN/SHALL.
- Priorizar requisitos funcionais e invariantes testáveis (incluindo casos inválidos, permissão, concorrência e UI).
- Crie specs por feature (não um único `tasks.md` gigante), na sequência `docs/roadmap/spec-order.md`.
- OpenAPI e testes de contrato precedem integração de UI.
- Nunca usar 'run all' antes da aprovação da fase tasks; execução paralela é insegura para tarefas com dependência de esquema e contrato.
- No fim de cada entrega: lista de arquivos alterados, comandos executados e resultado, riscos, evidência de funcionamento, pendências.
