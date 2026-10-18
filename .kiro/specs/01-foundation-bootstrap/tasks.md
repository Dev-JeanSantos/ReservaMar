# Feature Spec 01 — Fundação do monorepo (tasks)

> **Status:** RASCUNHO DE TASKS — aguardando aprovação antes de qualquer implementação.
> Referência: [design.md](./design.md) | [requirements.md](./requirements.md) | [ADR-0001](../../../docs/adr/ADR-0001-modular-monolith-and-stack.md) | [Definition of Done](../../../docs/quality/definition-of-done.md)

---

## Ordem de execução

```
TASK-01 → TASK-02 → TASK-03 → TASK-04 → TASK-05 → TASK-06 → TASK-07 → TASK-08
```

Cada task só começa após a anterior estar verde (build + testes passando). Nenhuma task marcada concluída sem evidência de comandos executados.

---

## TASK-01 — Estrutura base do monorepo

**Objetivo:** criar a estrutura de diretórios definitiva conforme `steering/structure.md` e `design.md`.

**Passos:**
1. Criar pastas: `apps/api/`, `apps/web/`, `infra/compose/`, `infra/proxy/`, `.github/workflows/`
2. Atualizar `.gitignore` com os novos caminhos:
   - `apps/api/.gradle/`, `apps/api/build/`
   - `apps/web/node_modules/`, `apps/web/dist/`
   - `apps/api/src/main/resources/application-local.yml`
   - `apps/web/src/shared/api/types.generated.ts`
3. Atualizar `README.md` com estrutura final e comandos de início rápido

**Comandos de validação:**
```bash
# verificar estrutura criada
Get-ChildItem -Recurse -Depth 3 apps/, infra/, .github/
```

**DoD:**
- [ ] Estrutura de pastas criada conforme `design.md` seção 1
- [ ] `.gitignore` cobre todos os artefatos gerados dos dois apps
- [ ] `README.md` atualizado com estrutura e comandos
- [ ] Commit: `chore: monorepo final structure — apps/api, apps/web, infra/compose`

---

## TASK-02 — Docker Compose + PostgreSQL local

**Objetivo:** ambiente de banco reproduzível para desenvolvimento local.

**Passos:**
1. Criar `infra/compose/docker-compose.yml` com PostgreSQL 17-alpine e healthcheck
2. Criar `infra/compose/.env.example` documentando `DATABASE_URL`, `DATABASE_USER`, `DATABASE_PASSWORD`
3. Validar que `docker compose up` sobe o banco saudável

**Comandos de validação:**
```bash
docker compose -f infra/compose/docker-compose.yml up -d
docker compose -f infra/compose/docker-compose.yml ps        # postgres: healthy
docker compose -f infra/compose/docker-compose.yml down
```

**DoD:**
- [ ] `docker compose up` sobe PostgreSQL 17 com status `healthy`
- [ ] Credenciais exclusivas para local (não reutilizáveis em produção)
- [ ] `.env.example` documenta todas as variáveis necessárias
- [ ] Commit: `infra: Docker Compose PostgreSQL 17 with healthcheck`

---

## TASK-03 — Scaffold do backend (apps/api)

**Objetivo:** projeto Kotlin + Spring Boot 4.1.1 com build reproduzível e estrutura hexagonal inicial.

**Passos:**
1. Criar projeto com Gradle Kotlin DSL, JDK 21, Kotlin 2.2.0, Spring Boot 4.1.1
2. Configurar `gradle/libs.versions.toml` com todas as versões pinadas
3. Adicionar dependências conforme `design.md` seção 2.2 (incluindo Spring Session JDBC e springdoc 3.1.1)
4. Criar pacote `br.com.reservamar.common.` com subpacotes `error/` e `system/`
5. Criar `application.yml` sem segredos, com variáveis de ambiente obrigatórias
6. Criar `application-local.yml` (gitignored) apontando para credenciais do Docker Compose
7. Criar `.env.example` em `apps/api/`
8. Validar que `./gradlew build` passa

**Comandos de validação:**
```bash
cd apps/api
./gradlew build
./gradlew dependencies --configuration runtimeClasspath | Select-String "springdoc","spring-session","flyway"
```

**DoD:**
- [ ] `./gradlew build` verde sem warnings críticos de deprecação
- [ ] `libs.versions.toml` com todas as versões pinadas
- [ ] `application.yml` sem nenhum segredo commitado
- [ ] `application-local.yml` listado no `.gitignore`
- [ ] Pacote `common/` criado com estrutura `error/` e `system/`
- [ ] Spring Session JDBC, springdoc 3.1.1 e Testcontainers no classpath
- [ ] Commit: `feat(api): scaffold Spring Boot 4.1.1 Kotlin with hexagonal structure and version catalog`

---

## TASK-04 — Flyway + migrations V001 e V002

**Objetivo:** migrations funcionando com banco real, incluindo tabelas do Spring Session.

**Passos:**
1. Criar `V001__create_schema_version.sql` — tabela sentinela de bootstrap
2. Criar `V002__create_spring_session_tables.sql` — script oficial Spring Session para PostgreSQL
3. Escrever `DatabaseMigrationTest.kt` com Testcontainers (PostgreSQL real)
4. Configurar `spring.session.jdbc.initialize-schema: never` em `application.yml` (Flyway gerencia)

**Comandos de validação:**
```bash
cd apps/api
./gradlew test --tests "*DatabaseMigrationTest*"
# com banco local rodando:
docker compose -f ../../infra/compose/docker-compose.yml up -d
./gradlew bootRun &
# verificar no log: "Successfully applied 2 migrations"
```

**DoD:**
- [ ] `DatabaseMigrationTest` passa com PostgreSQL real via Testcontainers (AC-03.3)
- [ ] V001 e V002 aplicadas sem erros no banco local
- [ ] Alterar V001 depois de aplicada resulta em falha clara do Flyway (AC-03.2)
- [ ] `ddl-auto: validate` ativo — JPA não cria/altera schema
- [ ] Commit: `feat(api): Flyway migrations V001 schema_version and V002 spring_session`

---

## TASK-05 — Endpoints de sistema, OpenAPI e Problem Details

**Objetivo:** health, version, contrato OpenAPI 3.1 e tratamento de erros funcionando.

**Passos:**
1. Criar `CorrelationIdFilter.kt` — gera `X-Correlation-Id` por request e inclui no MDC e resposta
2. Criar `GlobalExceptionHandler.kt` — Problem Details RFC 9457 para todos os erros, sem stack trace
3. Criar `VersionController.kt` — `GET /api/v1/system/version`
4. Configurar Actuator: expor apenas `/actuator/health`, `show-details: never`
5. Confirmar springdoc: `/v3/api-docs` ativo, `/swagger-ui.html` apenas com `SWAGGER_ENABLED=true`
6. Escrever `VersionControllerTest.kt` com MockMvc

**Comandos de validação:**
```bash
cd apps/api
./gradlew test
# com app rodando com SWAGGER_ENABLED=true:
curl http://localhost:8080/actuator/health
curl http://localhost:8080/api/v1/system/version
curl http://localhost:8080/v3/api-docs | ConvertFrom-Json | Select-Object openapi
```

**DoD:**
- [ ] `GET /api/v1/system/version` retorna `{"version":"0.1.0","environment":"local"}` (AC-01.2)
- [ ] `GET /actuator/health` retorna `{"status":"UP"}` sem detalhes internos
- [ ] `GET /v3/api-docs` retorna contrato OpenAPI 3.1 válido (AC-04.1)
- [ ] Erro de validação retorna Problem Details com `correlationId`, sem stack trace (AC-04.2)
- [ ] Swagger UI inacessível sem `SWAGGER_ENABLED=true`
- [ ] `VersionControllerTest` passando com MockMvc
- [ ] Commit: `feat(api): system endpoints, OpenAPI 3.1, Problem Details with correlationId`

---

## TASK-06 — Scaffold do frontend (apps/web)

**Objetivo:** projeto React 19 + TypeScript strict com estrutura conforme `steering/structure.md`.

**Passos:**
1. Criar projeto Vite (React + TypeScript)
2. Configurar `tsconfig.json` com `strict: true`
3. Instalar dependências: React Router 7, TanStack Query 5, React Hook Form 7, Zod 3, Tailwind 4, date-fns 4, lucide-react
4. Criar estrutura: `src/app/`, `src/features/`, `src/shared/{api,ui,lib,types}/`, `src/tests/e2e/`
5. Configurar Vite proxy: `/api` e `/actuator` → `http://localhost:8080`
6. Criar `src/app/App.tsx` e `src/app/Router.tsx` com rota `/` (placeholder)
7. Criar `src/shared/ui/ErrorBoundary.tsx`
8. Criar `src/shared/api/client.ts` com fetch wrapper e tratamento de erro
9. Validar `npm run build` sem erros TypeScript

**Comandos de validação:**
```bash
cd apps/web
npm ci
npm run typecheck    # tsc --noEmit, zero erros
npm run build        # dist/ gerado sem erros
```

**DoD:**
- [ ] `npm ci && npm run build` sem erros (AC-02.1)
- [ ] TypeScript `strict: true`, zero `@ts-ignore` ou `any` explícito
- [ ] Estrutura `app/`, `features/`, `shared/`, `tests/` criada conforme steering
- [ ] Viewport 390px: layout navegável sem overflow (AC-02.2)
- [ ] API indisponível: mensagem de erro legível, sem tela branca (AC-02.3)
- [ ] Sem dados fictícios apresentados como reais
- [ ] Commit: `feat(web): scaffold React 19 TypeScript Vite with feature-sliced structure`

---

## TASK-07 — Geração de tipos a partir do contrato OpenAPI

**Objetivo:** tipagem do frontend derivada do contrato backend — fonte de verdade única.

**Passos:**
1. Instalar `openapi-typescript@7.x` como devDependency
2. Criar script `generate:types` no `package.json` apontando para `http://localhost:8080/v3/api-docs`
3. Adicionar `src/shared/api/types.generated.ts` ao `.gitignore`
4. Atualizar `client.ts` para usar os tipos gerados
5. Validar `npm run typecheck` com tipos gerados

**Comandos de validação:**
```bash
# com backend rodando:
cd apps/web
npm run generate:types    # gera src/shared/api/types.generated.ts
npm run typecheck         # zero erros com tipos gerados
```

**DoD:**
- [ ] `generate:types` executa sem erros com backend rodando (AC-04.3)
- [ ] `client.ts` tipado com tipos gerados — sem `any` explícito (AC-02.4)
- [ ] `types.generated.ts` no `.gitignore` e não commitado
- [ ] Commit: `feat(web): openapi-typescript contract type generation`

---

## TASK-08 — CI GitHub Actions

**Objetivo:** pipeline automático para ambos os apps em todo PR.

**Passos:**
1. Criar `.github/workflows/api-ci.yml`:
   - Trigger: `push`/`pull_request` em `apps/api/**`
   - Setup JDK 21, cache `~/.gradle`
   - `./gradlew test build check` (ktlint + detekt + Testcontainers)
2. Criar `.github/workflows/web-ci.yml`:
   - Trigger: `push`/`pull_request` em `apps/web/**`
   - Setup Node 22, cache `node_modules`
   - `npm ci`, `npm run typecheck`, `npm run test:run`, `npm run build`
3. Adicionar ktlint e detekt ao `build.gradle.kts` de `apps/api`
4. Adicionar script `test:run` ao `package.json` (`vitest run`)

**Comandos de validação:**
```bash
# abrir PR com mudança em apps/api/ e verificar workflow api-ci disparado
# abrir PR com mudança em apps/web/ e verificar workflow web-ci disparado
```

**DoD:**
- [ ] PR em `apps/api/**` dispara `api-ci.yml` (AC-05.1)
- [ ] PR em `apps/web/**` dispara `web-ci.yml` (AC-05.1)
- [ ] Falha em qualquer step bloqueia merge (AC-05.2)
- [ ] ktlint e detekt rodam no CI do backend
- [ ] Vitest `--run`, typecheck e build rodam no CI do frontend
- [ ] Commit: `ci: GitHub Actions pipelines for api and web with path filters`

---

## Resumo de comandos por app

### Backend
```bash
# Subir banco
docker compose -f infra/compose/docker-compose.yml up -d

# Testes
cd apps/api && ./gradlew test

# Build completo (lint + análise + testes + jar)
cd apps/api && ./gradlew build check

# Rodar aplicação local
cd apps/api && ./gradlew bootRun
```

### Frontend
```bash
# Instalar
cd apps/web && npm ci

# Gerar tipos do contrato (backend deve estar rodando)
cd apps/web && npm run generate:types

# Dev server
cd apps/web && npm run dev

# Build de produção
cd apps/web && npm run build

# Testes CI (sem watch)
cd apps/web && npm run test:run
```
