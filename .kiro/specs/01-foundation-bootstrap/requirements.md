# Feature Spec 01 — Fundação do monorepo (requirements iniciais)

> **Status:** RASCUNHO DE REQUISITOS para revisão no Kiro. Não autoriza gerar código antes de revisar requisitos, design e tasks. **Não existem design.md/tasks.md intencionalmente**: peça ao Kiro que os produza no fluxo de spec após aprovação.

## Visão
Como mantenedor do ReservaMar, quero um monorepo com aplicação API e web funcionando em localhost, contrato OpenAPI, segurança preparada e CI mínimo para criar features com qualidade e consistência.

## Escopo
IN: monorepo, backend/gradle/CI, web/vite/CI, Docker Compose PostgreSQL, Flyway inicial, endpoints health / versão, manejo de erros, contract generation, pipeline mínimo, configurações local/test sem segredos.
OUT: usuários reais, autenticação final, catálogo, reservas, pagamentos, deploy produção, pagamentos digitais.

## Requirements

### REQ-01 — Backend base
**User Story:** Como desenvolvedor, quero inicializar uma aplicação Kotlin Spring Boot 4.1.x com build reproduzível para implementar os módulos.
- AC-01.1: WHEN o desenvolvedor executar `./gradlew test` em `apps/api` em ambiente preparado THEN o sistema SHALL executar testes de backend sem depender de serviços externos não declarados.
- AC-01.2: WHEN o backend iniciar com env de desenvolvimento válida THEN o sistema SHALL expor `/actuator/health` e `/api/v1/system/version` sem revelar segredos.
- AC-01.3: WHEN a configuração obrigatória do banco estiver ausente no perfil de produção THEN o sistema SHALL falhar explicitamente na inicialização, sem usar valores inseguros padrão.
- AC-01.4: WHEN dependências forem geradas THEN o sistema SHALL usar JDK 21, Kotlin compatível e Spring Boot 4.1.x verificado, sem bibliotecas legadas incompatíveis.

### REQ-02 — Frontend base
**User Story:** Como operador futuro, quero uma aplicação web responsiva acessível para usar no celular.
- AC-02.1: WHEN o desenvolvedor executar `npm ci && npm run build` em `apps/web` THEN o sistema SHALL compilar React/TypeScript strict sem erros.
- AC-02.2: WHEN o navegador abrir `/` numa viewport 390px THEN o sistema SHALL mostrar uma tela inicial com navegação adequada, sem dados de operação fictícios apresentados como reais.
- AC-02.3: WHEN API estiver indisponível THEN o sistema SHALL apresentar estado de erro legível, sem tela branca.
- AC-02.4: WHEN TypeScript for validado THEN o sistema SHALL manter `strict` e tipagem de respostas da API baseada em contrato OpenAPI.

### REQ-03 — Banco, migrations e desenvolvimento local
**User Story:** Como mantenedor, quero ambiente local reproduzível.
- AC-03.1: WHEN rodar compose conforme README THEN o sistema SHALL inicializar PostgreSQL com credenciais exclusivas local/test e executar migrations Flyway.
- AC-03.2: WHEN uma migration falhar THEN o sistema SHALL interromper a inicialização com mensagem diagnóstica, sem modificar scripts previamente aplicados.
- AC-03.3: WHEN ocorrer build em CI THEN o sistema SHALL executar testes com PostgreSQL real via Testcontainers quando testes dependam de banco.

### REQ-04 — Contrato e erros
**User Story:** Como dev frontend, quero contrato único e erros previsíveis.
- AC-04.1: WHEN o backend publicar endpoints REST THEN o sistema SHALL documentá-los em OpenAPI 3.1 versionado.
- AC-04.2: WHEN uma requisição inválida chegar THEN o sistema SHALL responder com Problem Details estável, `correlationId`, e nenhum stack trace.
- AC-04.3: WHEN o frontend precisar de tipos REST THEN o sistema SHALL gerar/validar tipos a partir do OpenAPI por um comando reproduzível.

### REQ-05 — Qualidade e gates
**User Story:** Como dono do projeto, quero validar cada alteração antes de integrá-la.
- AC-05.1: WHEN um PR for aberto THEN CI SHALL rodar lint, testes, builds e verificações de segurança básicas para os dois apps.
- AC-05.2: WHEN um teste/compilação falhar THEN a task SHALL permanecer incompleta até corrigida ou explicitamente marcada como bloqueada.
- AC-05.3: WHEN Kiro produzir design e tarefas THEN SHALL referenciar ADR-0001 e `docs/quality/definition-of-done.md`, incluindo pelo menos 1 task de documentação, de testes de integração e verificação responsiva.

## Design guidance para o Kiro, NÃO é design aprovado
- Gerar `design.md` com diretórios, Gradle wrapper, config de plugins, Docker Compose, proxy local, scripts NPM, health endpoint, OpenAPI, arquivos CI e diagrama de execução.
- Antes de tasks, explicar compatibilidade do Spring Boot 4.1.x com Kotlin e JDK21 e escolher mecanismo único de geração do OpenAPI (por exemplo springdoc de versão explicitamente compatível; se incerto, alternativa comprovável e testada).
- `tasks.md` deve dividir bootstrap de api, web, banco, testes, integração de contratos e CI; registrar comandos exatos e DoD.
