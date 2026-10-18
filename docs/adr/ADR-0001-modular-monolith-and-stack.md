# ADR-0001 — Monólito modular hexagonal em Kotlin + React

- Data: 2026-10-18
- Status: **Proposta (aceite do proprietário necessário)**
- Decisores: fundador e Kiro (assessoria técnica, sem autoridade final)

## Contexto
Micro-SaaS B2B em validação, um desenvolvedor principal, baixa complexidade operacional e necessidade de rastreabilidade entre UI e backend. Precisamos integrar login, saídas, vagas, reservas e sinais sem custo de infraestrutura distribuída.

## Decisão
- Um repositório, um backend Spring Boot 4.1.x Kotlin e um frontend React TypeScript compilado separadamente, servido sob **mesma origem** na produção.
- Backend **monólito modular orientado a domínio**, com boundaries `identity`, `catalog`, `departures`, `bookings`, `customers`, `payments`, `reporting`, camada hexagonal pragmática por módulo.
- PostgreSQL transacional e migrações Flyway. UI SPA responsiva com REST OpenAPI 3.1.
- Sem evento distribuído, BFF extra ou duplicação de regras de negócio no browser.
- Docker Compose local; hospedagem de baixo custo somente após validar operador piloto.

## Alternativas consideradas
- **Microserviços/filas:** separação e escala, mas deployment, tracing, custo e transações mais difíceis — rejeitado no MVP.
- **Firebase/Firestore ou MongoDB:** agilidade inicial, mas baixa clareza para lock transacional de assentos e queries relacionais — rejeitado para reservas.
- **Next.js full stack:** potencial SSR e produtividade, mas duplica estratégia tecnológica sem necessidade SEO no painel privado — rejeitado MVP.
- **Spring Boot 3.5:** bem suportado, porém linha 4.1.x estável em 2026; reconsiderar se lib indispensável impedir compatibilidade.

## Consequências
(+) Transações consistentes e menos serviços; (+) stack conhecida pelo fundador; (+) deploy enxuto. (-) Escalabilidade vertical inicial; (-) disciplina de boundaries por package; (-) é preciso checar compatibilidade de dependências do Boot 4.1.x.

## Guardrails
Domínio sem dependência de framework. `gradle test`, testes de integração e build web devem rodar no CI. Toda exceção exige nova ADR.
