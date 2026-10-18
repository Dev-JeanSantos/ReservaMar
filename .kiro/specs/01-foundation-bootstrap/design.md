# Feature Spec 01 — Fundação do monorepo (design)

> **Status:** RASCUNHO DE DESIGN — aguardando aprovação antes de gerar tasks.md e antes de qualquer código.
> Referência: [ADR-0001](../../../docs/adr/ADR-0001-modular-monolith-and-stack.md) | [Definition of Done](../../../docs/quality/definition-of-done.md) | [steering/tech.md](../../../.kiro/steering/tech.md) | [steering/structure.md](../../../.kiro/steering/structure.md)

---

## 1. Estrutura de diretórios

```
ReservaMar/                               ← raiz do monorepo
├── apps/
│   ├── api/                              ← Spring Boot 4.1.1 / Kotlin / Gradle
│   │   ├── build.gradle.kts
│   │   ├── settings.gradle.kts
│   │   ├── gradle/
│   │   │   ├── libs.versions.toml        ← Version Catalog (todas as versões pinadas)
│   │   │   └── wrapper/
│   │   │       ├── gradle-wrapper.jar
│   │   │       └── gradle-wrapper.properties
│   │   ├── gradlew / gradlew.bat
│   │   └── src/
│   │       ├── main/
│   │       │   ├── kotlin/br/com/reservamar/
│   │       │   │   ├── ReservaMarApplication.kt
│   │       │   │   └── common/           ← erros, segurança, datas, tenancy (futuro)
│   │       │   │       ├── error/
│   │       │   │       │   ├── GlobalExceptionHandler.kt   (Problem Details RFC 9457)
│   │       │   │       │   └── CorrelationIdFilter.kt
│   │       │   │       └── system/
│   │       │   │           └── VersionController.kt        (GET /api/v1/system/version)
│   │       │   └── resources/
│   │       │       ├── application.yml                     (base — sem segredos)
│   │       │       ├── application-local.yml               (gitignored)
│   │       │       └── db/migration/
│   │       │           └── V001__create_schema_version.sql
│   │       └── test/
│   │           └── kotlin/br/com/reservamar/
│   │               ├── common/system/VersionControllerTest.kt   (MockMvc)
│   │               └── common/infra/DatabaseMigrationTest.kt    (Testcontainers)
│   │
│   └── web/                              ← React 19 / TypeScript / Vite
│       ├── package.json
│       ├── tsconfig.json                 (strict: true)
│       ├── vite.config.ts
│       ├── index.html
│       └── src/
│           ├── main.tsx
│           ├── app/                      ← root, router, providers
│           │   ├── App.tsx
│           │   └── Router.tsx
│           ├── features/                 ← auth, catalog, departures... (specs futuras)
│           ├── shared/
│           │   ├── api/
│           │   │   └── client.ts         (fetch wrapper + tratamento de erro)
│           │   ├── ui/
│           │   │   └── ErrorBoundary.tsx
│           │   ├── lib/
│           │   └── types/
│           └── tests/
│               └── e2e/                  (Playwright — specs futuras)
│
├── infra/
│   ├── compose/
│   │   └── docker-compose.yml            ← PostgreSQL 17 local
│   └── proxy/                            ← placeholder (definição futura)
│
├── .github/
│   └── workflows/
│       ├── api-ci.yml
│       └── web-ci.yml
│
├── docs/                                 (existente — mantido)
├── scripts/                              (existente — mantido)
├── .kiro/                                (existente — mantido)
├── .gitignore
└── README.md
```

---

## 2. Backend — `apps/api`

### 2.1 Stack e versões fixas

| Componente | Versão |
|---|---|
| JDK | 21 (LTS) |
| Kotlin | 2.2.0 |
| Spring Boot | 4.1.1 |
| Spring Framework | 7.x (gerenciado pelo Boot BOM) |
| Gradle | 8.x (via wrapper — versão exata gerada no bootstrap) |
| springdoc-openapi | 3.1.1 (MAJOR em lockstep com Spring Boot 4) |
| Spring Session JDBC | gerenciado pelo Spring Boot BOM |
| Flyway | gerenciado pelo Spring Boot BOM |
| PostgreSQL driver | gerenciado pelo Spring Boot BOM |
| Testcontainers | gerenciado pelo Spring Boot BOM |

> Todas as versões travadas em `gradle/libs.versions.toml`. O Gradle wrapper garante build reproduzível.

### 2.2 Dependências `build.gradle.kts`

```kotlin
plugins {
    kotlin("jvm") version "2.2.0"
    kotlin("plugin.spring") version "2.2.0"
    id("org.springframework.boot") version "4.1.1"
    id("io.spring.dependency-management") version "1.1.7"
}

dependencies {
    // Core Web
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    implementation("org.springframework.boot:spring-boot-starter-validation")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
    implementation("org.jetbrains.kotlin:kotlin-reflect")

    // Dados
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.flywaydb:flyway-core")
    runtimeOnly("org.postgresql:postgresql")

    // Sessão persistida no PostgreSQL (Spring Session JDBC)
    implementation("org.springframework.boot:spring-boot-starter-jdbc")
    implementation("org.springframework.session:spring-session-jdbc")

    // OpenAPI / Swagger UI
    implementation("org.springdoc:springdoc-openapi-starter-webmvc-ui:3.1.1")

    // Testes
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.testcontainers:junit-jupiter")
    testImplementation("org.testcontainers:postgresql")
}
```

### 2.3 Endpoints expostos nesta spec

| Método | Path | Descrição |
|---|---|---|
| GET | `/actuator/health` | Saúde da aplicação (Spring Actuator) |
| GET | `/api/v1/system/version` | Versão da aplicação e ambiente |
| GET | `/v3/api-docs` | Contrato OpenAPI 3.1 (JSON) |
| GET | `/swagger-ui.html` | Swagger UI (local apenas, via `SWAGGER_ENABLED=true`) |

Resposta de `/api/v1/system/version`:
```json
{
  "version": "0.1.0",
  "environment": "local"
}
```

### 2.4 Tratamento de erros (Problem Details RFC 9457)

Todos os erros seguem RFC 9457, suportado nativamente pelo Spring Boot 4:

```json
{
  "type": "https://reservamar.com.br/errors/validation",
  "title": "Validation Failed",
  "status": 422,
  "detail": "Campo 'name' é obrigatório",
  "correlationId": "uuid-gerado-por-request"
}
```

- Stack traces **nunca** expostos em resposta
- `correlationId` gerado por `CorrelationIdFilter` e incluído em todos os erros e logs
- Códigos estáveis por tipo de erro (definidos nas specs seguintes)

### 2.5 Configuração e segredos

`application.yml` (commitado — sem segredos):
```yaml
spring:
  application:
    name: reservamar-api
  datasource:
    url: ${DATABASE_URL}           # obrigatório — falha explícita se ausente (AC-01.3)
    username: ${DATABASE_USER}     # obrigatório
    password: ${DATABASE_PASSWORD} # obrigatório
  jpa:
    hibernate:
      ddl-auto: validate           # Flyway é source of truth
  flyway:
    enabled: true
    locations: classpath:db/migration
  session:
    store-type: jdbc               # Spring Session JDBC — sessões no PostgreSQL
    jdbc:
      initialize-schema: never     # Flyway gerencia o schema de sessões

management:
  endpoints:
    web:
      exposure:
        include: health
  endpoint:
    health:
      show-details: never          # nunca expor detalhes internos

app:
  version: "@project.version@"
  environment: ${APP_ENV:local}

springdoc:
  swagger-ui:
    enabled: ${SWAGGER_ENABLED:false}   # desabilitado por padrão; ativo só com SWAGGER_ENABLED=true
  api-docs:
    enabled: true                       # /v3/api-docs sempre disponível para geração de tipos
```

> **AC-01.3 garantido:** sem `DATABASE_URL`, a app falha explicitamente na inicialização com mensagem clara.

### 2.6 Migration de sessões

A tabela de sessões do Spring Session JDBC será criada via Flyway:

`V002__create_spring_session_tables.sql` — script oficial do Spring Session adaptado para PostgreSQL.

---

## 3. Frontend — `apps/web`

### 3.1 Stack e versões fixas

| Componente | Versão |
|---|---|
| Node | 22 LTS |
| React | 19.x |
| TypeScript | 5.x (strict: true) |
| Vite | 6.x |
| React Router | 7.x |
| TanStack Query | 5.x |
| React Hook Form | 7.x |
| Zod | 3.x |
| Tailwind CSS | 4.x |
| shadcn/ui | componentes copiados e auditados |
| date-fns | 4.x |
| lucide-react | latest stable |
| Vitest | 3.x |
| React Testing Library | 16.x |
| MSW | 2.x |

### 3.2 Estrutura interna (conforme `steering/structure.md`)

```
src/
├── app/               ← root, router, providers (QueryClientProvider, RouterProvider)
├── features/          ← uma pasta por domínio (specs futuras: auth, catalog, etc.)
├── shared/
│   ├── api/           ← client.ts (fetch wrapper), types.generated.ts (gitignored)
│   ├── ui/            ← componentes base: Button, ErrorBoundary, EmptyState, ErrorState
│   ├── lib/           ← formatadores de moeda, datas, telefone
│   └── types/         ← tipos compartilhados não gerados
└── tests/
    └── e2e/           ← Playwright (specs futuras)
```

### 3.3 Tela inicial do bootstrap

- Rota `/` — placeholder explícito "ReservaMar — em breve"
- Layout responsivo: mobile 360–430px e desktop ≥1024px (AC-02.2)
- Sem dados fictícios apresentados como reais
- `ErrorBoundary` na raiz da aplicação
- `client.ts` detecta API indisponível e retorna estado de erro legível — sem tela branca (AC-02.3)

### 3.4 Proxy Vite em desenvolvimento

```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': 'http://localhost:8080',
    '/actuator': 'http://localhost:8080'
  }
}
```

Evita CORS em dev e simula a mesma origem do deploy — sem Nginx nesta fase.

### 3.5 Tipagem baseada em contrato (AC-02.4 / AC-04.3)

- `openapi-typescript@7.x` gera tipos a partir de `/v3/api-docs` (ou spec estática)
- Script: `npm run generate:types`
- Saída: `src/shared/api/types.generated.ts` (gitignored — gerado em build/CI)

---

## 4. Banco e migrações — `infra/compose/docker-compose.yml`

```yaml
services:
  postgres:
    image: postgres:17-alpine
    environment:
      POSTGRES_DB: reservamar_local
      POSTGRES_USER: reservamar
      POSTGRES_PASSWORD: localonly
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U reservamar"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

- Credenciais exclusivas para local (AC-03.1)
- `application-local.yml` (gitignored) aponta para essas credenciais
- `.env.example` documenta as variáveis necessárias

### 4.1 Migrations Flyway

| Versão | Arquivo | Conteúdo |
|---|---|---|
| V001 | `V001__create_schema_version.sql` | Tabela sentinela — valida Flyway funcionando |
| V002 | `V002__create_spring_session_tables.sql` | Tabelas do Spring Session JDBC |

> Migrations **nunca editadas após aplicadas** (steering/tech.md).

---

## 5. CI — GitHub Actions

### `api-ci.yml` (trigger: `push`/`PR` em `apps/api/**`)

```
steps:
  1. checkout
  2. setup JDK 21
  3. cache Gradle (~/.gradle)
  4. ./gradlew test          (JUnit 5 + Testcontainers PostgreSQL real)
  5. ./gradlew build
  6. ./gradlew check         (ktlint + detekt)
```

### `web-ci.yml` (trigger: `push`/`PR` em `apps/web/**`)

```
steps:
  1. checkout
  2. setup Node 22
  3. cache node_modules
  4. npm ci
  5. npm run typecheck       (tsc --noEmit)
  6. npm run test:run        (Vitest --run, sem watch)
  7. npm run build
```

> AC-05.1 garantido: lint + testes + build para ambos em todo PR.

---

## 6. Fluxo de execução local

```
┌──────────────────────────────────────────┐
│  docker compose -f infra/compose/        │
│  docker-compose.yml up -d                │
│  └─ PostgreSQL 17 :5432 (healthy)        │
└─────────────────┬────────────────────────┘
                  │
┌─────────────────▼────────────────────────┐
│  ./gradlew bootRun  (apps/api/)          │
│  └─ Flyway: V001 + V002 aplicadas        │
│  └─ Spring Session JDBC iniciado         │
│  └─ API em :8080                         │
│  └─ /actuator/health ✓                   │
│  └─ /api/v1/system/version ✓             │
│  └─ /v3/api-docs ✓                       │
│  └─ /swagger-ui.html ✓ (SWAGGER_ENABLED) │
└─────────────────┬────────────────────────┘
                  │
┌─────────────────▼────────────────────────┐
│  npm run dev  (apps/web/)                │
│  └─ Vite dev server :5173                │
│  └─ proxy /api → :8080                   │
│  └─ tela inicial responsiva              │
└──────────────────────────────────────────┘
```

---

## 7. Pontos de atenção / riscos

| Risco | Mitigação |
|---|---|
| Spring Boot 4.1.1 + springdoc 3.1.1 sem uso prévio | Primeira task do backend valida a integração antes de avançar |
| Testcontainers no CI pode ser lento | Cache de layers Docker no GitHub Actions |
| `openapi-typescript@7.x` + OpenAPI 3.1 | Verificar na task de contrato antes de integrar no frontend |
| Script V002 (Spring Session) precisa ser o oficial PostgreSQL | Buscar script na documentação oficial do Spring Session ao implementar |

---

## 8. O que este design NÃO inclui (fora do escopo desta spec)

- Autenticação / Spring Security / CSRF (Spec 02)
- Multi-tenancy e isolamento por operador (Spec 02)
- Módulos de negócio: catalog, departures, bookings, payments (Specs 03–05)
- Dashboard e comunicação (Spec 06)
- Deploy em produção e proxy reverso (decisão futura)
- Playwright E2E (Spec 07)
