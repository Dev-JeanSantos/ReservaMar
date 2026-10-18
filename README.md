# ReservaMar

> Micro-SaaS B2B para operadores brasileiros de pescarias embarcadas compartilhadas.
> **Estado:** bootstrap em andamento — MVP em desenvolvimento.

## Estrutura do monorepo

```
ReservaMar/
├── apps/
│   ├── api/          # Backend: Kotlin + Spring Boot 4.1.1 + PostgreSQL
│   └── web/          # Frontend: React 19 + TypeScript + Vite
├── infra/
│   ├── compose/      # Docker Compose local (PostgreSQL 17)
│   └── proxy/        # Configuração de proxy (definição futura)
├── .github/
│   └── workflows/    # CI: api-ci.yml e web-ci.yml
├── docs/             # ADRs, domínio, design, spec-seeds, qualidade
├── scripts/          # Scripts utilitários
└── .kiro/            # Steering, specs e hooks do Kiro IDE
```

## Pré-requisitos

- JDK 21
- Docker Desktop (para PostgreSQL local)
- Node 22 LTS

## Início rápido

### 1. Subir o banco de dados

```bash
docker compose -f infra/compose/docker-compose.yml up -d
```

### 2. Configurar variáveis do backend

Copie o exemplo e ajuste:
```bash
cp apps/api/.env.example apps/api/src/main/resources/application-local.yml
```

### 3. Rodar o backend

```bash
cd apps/api
./gradlew bootRun
```

API disponível em `http://localhost:8080`
- Health: `GET /actuator/health`
- Versão: `GET /api/v1/system/version`
- Contrato: `GET /v3/api-docs`
- Swagger UI: `GET /swagger-ui.html` (apenas com `SWAGGER_ENABLED=true`)

### 4. Instalar e rodar o frontend

```bash
cd apps/web
npm ci
npm run dev
```

Frontend disponível em `http://localhost:5173`

### 5. Gerar tipos TypeScript do contrato (backend deve estar rodando)

```bash
cd apps/web
npm run generate:types
```

## Testes

### Backend
```bash
cd apps/api
./gradlew test          # JUnit 5 + Testcontainers
./gradlew check         # lint (ktlint) + análise estática (detekt)
```

### Frontend
```bash
cd apps/web
npm run typecheck       # tsc --noEmit
npm run test:run        # Vitest (sem watch)
npm run build           # build de produção
```

## Documentação

- [`docs/START-IN-KIRO.md`](docs/START-IN-KIRO.md) — como usar este projeto no Kiro IDE
- [`docs/adr/`](docs/adr/) — decisões arquiteturais
- [`docs/domain/`](docs/domain/) — regras de negócio e estados
- [`docs/api/`](docs/api/) — contrato de API (seed)
- [`docs/design/`](docs/design/) — design system e jornadas
- [`.kiro/specs/`](.kiro/specs/) — feature specs (requirements → design → tasks)

## Roadmap de specs

| # | Spec | Status |
|---|---|---|
| 01 | Foundation Bootstrap | 🔄 Em andamento |
| 02 | Auth & Tenancy | ⏳ Aguardando |
| 03 | Resources & Departures | ⏳ Aguardando |
| 04 | Customers & Bookings | ⏳ Aguardando |
| 05 | Manual Payments | ⏳ Aguardando |
| 06 | Dashboard & Communications | ⏳ Aguardando |
| 07 | Pilot Hardening | ⏳ Aguardando |
| 08 | Future Integrations | ⏳ Aguardando |
