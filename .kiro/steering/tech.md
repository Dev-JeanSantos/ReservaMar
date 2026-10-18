---
inclusion: always
---
# Stack e engenharia obrigatórias

- Repositório monorepo: `apps/api` e `apps/web`, `docs/` e `.kiro/` na raiz.
- Backend: JDK 21, Kotlin >=2.2 compatível, Spring Boot **4.1.x** estável, Spring WebMVC (não WebFlux), Spring Security, Spring Validation, Spring Session JDBC, Spring Data JPA, PostgreSQL 17+, Flyway, Gradle Kotlin DSL. Preferir a linha mais recente de patch dentro de 4.1.x suportada no momento do bootstrap; registrar versões finais no build e lockfile. Em Spring Boot 4 usar starters modulares corretos (`spring-boot-starter-webmvc`, etc.) após validar documentação oficial.
- Auth: sessão Spring Security com cookie `HttpOnly; Secure; SameSite=Lax` em produção, CSRF habilitado para mutações, sessão persistida com Spring Session JDBC, password hash Argon2id se disponível/compatível ou BCrypt configurado com custo adequado. Nunca tokens no localStorage.
- Frontend: React 19, TypeScript `strict`, Vite, React Router, TanStack Query, React Hook Form + Zod, Tailwind CSS, shadcn/ui/Radix, date-fns, lucide-react. Não usar Next.js, Redux ou frontend gerado em runtime neste MVP.
- API REST JSON `/api/v1`, contratos OpenAPI 3.1 gerados e revisados, erros RFC 9457 Problem Details, validação nos dois lados, backend autoritativo. Swagger UI desabilitado por padrão (`SWAGGER_ENABLED=false`); ativar apenas em ambiente local via variável de ambiente explícita. `/v3/api-docs` permanece ativo em todos os ambientes para geração de tipos.
- Testes: JUnit 5 + AssertJ + MockMvc + Testcontainers PostgreSQL; Vitest + Testing Library + MSW; Playwright E2E. Mock apenas em fronteiras externas, nunca simular banco nos testes de concorrência.
- Observabilidade: Actuator, Micrometer/Prometheus opcional, logs estruturados com correlação, sem PII no log. Migrations Flyway versionadas e nunca editadas depois de aplicadas.
- Deploy de piloto: Docker Compose no desenvolvimento. Hospedagem HTTPS com reverse proxy servindo web e API sob **mesma origem**, PostgreSQL com backup, segredos via env/secret manager.
- Idioma: pt-BR nos textos; inglês no código e no esquema. Datas ISO-8601 com offset/UTC na API, apresentação no fuso `America/Sao_Paulo`. Valores monetários internos em centavos (`Long`) e JSON em `amountCents`.
- Não introduzir Kafka, Redis, NoSQL, microsserviços ou Kubernetes sem ADR aprovada.
