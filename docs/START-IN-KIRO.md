# Começar no Kiro — instruções para o proprietário do projeto

## Antes de abrir o Kiro
- Criar um repositório Git privado `reservamar` e extrair este pacote na raiz. Conferir também o diretório oculto `.kiro`.
- Abrir a **raiz do repositório** no Kiro IDE. Escolher Feature Spec / **Requirements-First**, com revisão humana a cada fase.
- Não permitir alterações arbitrárias das ADRs. Se houver incompatibilidade técnica, propor alteração no formato: problema, opções, impacto e migração; aguardar aprovação.
- Usar uma branch por spec; aprovar uma spec por vez; não habilitar 'run all tasks' até entender dependências e custos.

## Prompt inicial — copie para o Kiro

```text
Você é meu arquiteto e desenvolvedor full stack principal no projeto ReservaMar.
Leia integralmente README.md, os arquivos em .kiro/steering/, docs/adr/, docs/domain/, docs/architecture/, docs/api/, docs/design/, docs/quality/ e docs/roadmap/spec-order.md.
Trate essas fontes como documentação primária. Se houver conflitos, use a hierarquia em .kiro/steering/spec-workflow.md e APONTE o conflito, sem inventar decisão.

Sua PRIMEIRA ENTREGA é uma análise de arquitetura e plano de implementação, NÃO código.
1. Explique a arquitetura proposta, riscos, decisões fechadas e hipóteses que precisam de confirmação comercial.
2. Faça uma matriz de rastreabilidade das regras BR-001...BR-023 às specs propostas.
3. Crie/revise a Feature Spec 01-foundation-bootstrap, adotando como base .kiro/specs/01-foundation-bootstrap/requirements.md. Gere primeiro/revise requirements.md no padrão EARS.
4. Aguarde minha aprovação dos requisitos. Só então produza design.md com componentes backend/frontend, interfaces, diagramas, esquema de dados inicial, riscos e testes.
5. Após nova aprovação, gere tasks.md em tarefas pequenas, ordenadas por dependência, incluindo backend, frontend, testes, migrações, documentação, segurança e CI.
6. Para CADA tarefa, aplique docs/quality/definition-of-done.md, informe comandos de validação reais, e NÃO marque concluída sem executá-los. Peça aprovação antes de mudanças arquiteturais.
7. Não implemente os módulos de negócio antes de fechar a spec de bootstrap.
Use pt-BR na documentação e interface; inglês em nomes de código, rotas e tabelas.
```

## Próximas solicitações (uma por vez)

1. `Crie uma nova Feature Spec requirements-first para docs/spec-seeds/02-auth-tenancy.md. Respeite steering e ADR. Gere requirements EARS, aguarde review; depois design; depois tasks. Cubra backend e frontend.`
2. Seguir com `03-resources-departures.md`, `04-customers-bookings.md`, `05-manual-payments.md`, `06-dashboard-communications.md`, `07-pilot-hardening.md`, nessa ordem.
3. Antes de liberar a feature seguinte, executar regressão e a checklist de qualidade.

## Revisão humana exigida
- **Requisitos:** negócio correto? Escopo mínimo? Contraexemplos? Quem paga? Estados claros?
- **Design:** API e UI consistentes? Concorrência comprovável? Tenant seguro? Estimativa de manutenção?
- **Tasks:** pequenas, rastreáveis, testáveis, sem simultaneidade perigosa em migrações/contratos?
- **Código:** testes de integração reais com PostgreSQL; validar manualmente no celular e numa tela desktop.

## Se Kiro pedir contexto adicional
A documentação já fornece um caminho padrão. Dúvidas de negócio devem virar `OPEN-DECISION` explícita, sem suposição silenciosa. Não bloquear a implementação de fundamentos por questões posteriores de modelo comercial.

## Fontes oficiais de funcionamento do Kiro (consultadas em 18/10/2026)
- https://kiro.dev/docs/steering/
- https://kiro.dev/docs/specs/
- https://kiro.dev/docs/specs/feature-specs/requirements-first/
- https://kiro.dev/docs/specs/best-practices/
- https://docs.spring.io/spring-boot/reference/
