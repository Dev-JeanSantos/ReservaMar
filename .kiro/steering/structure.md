---
inclusion: always
---
# Estrutura e organização

```text
reservamar/
├── apps/
│   ├── api/
│   │   ├── src/main/kotlin/br/com/reservamar/
│   │   │   ├── common/              # erro, segurança, datas, tenancy
│   │   │   ├── identity/            # login, usuários, memberships
│   │   │   ├── catalog/             # embarcações, atividades
│   │   │   ├── departures/          # saídas/capacidades
│   │   │   ├── bookings/            # reserva, alocação, prazos
│   │   │   ├── customers/           # contato do cliente
│   │   │   ├── payments/            # registros manuais de pagamento
│   │   │   └── reporting/           # resumo/dashboard
│   │   └── src/main/resources/db/migration/
│   └── web/
│       ├── src/app/                 # root, router, providers
│       ├── src/features/            # auth, catalog, departures, bookings, payments, dashboard
│       ├── src/shared/{api,ui,lib,types}/
│       └── tests/e2e/
├── .kiro/steering/ & .kiro/specs/
├── docs/{adr,architecture,domain,api,design,quality,roadmap,spec-seeds}/
└── infra/{compose,proxy}/
```

## Backend — hexagonal pragmático por domínio
Cada módulo contém `domain/`, `application/port/{in,out}/`, `application/service/`, `adapter/in/web/`, `adapter/out/persistence/` quando justificado. Domínio sem import Spring, JPA, HTTP; regras/invariantes testáveis isoladamente. Controllers não têm negócio; serviços de aplicação transacionam; adaptadores traduzem DTOs/entidades; não expor JPA entities na API.

## Frontend — feature-sliced pragmático
Cada feature possui `api/`, `components/`, `pages/`, `schemas/`, `hooks/`, `tests/`. Chamadas HTTP tipadas em um cliente comum, estado servidor com TanStack Query; forms RHF/Zod; evitar context global para cada tela. Formatar valores/datas na borda de apresentação.

## Contrato transversal
OpenAPI versionado como contrato consumido pelo frontend; gerar types ou cliente usando tooling reproduzível. UI não reconstrói regras de estoque/vagas no browser; servidor é fonte da verdade. Um pull request para mudança incompatível de contrato inclui migrations e UI compatível.
