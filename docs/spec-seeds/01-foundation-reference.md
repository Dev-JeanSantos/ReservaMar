# Seed 01 — Fundação do projeto (referência de requisitos)

A primeira spec já dispõe de `requirements.md` em `.kiro/specs/01-foundation-bootstrap/requirements.md`. Use o modo Requirements-First do Kiro para revisar e completar esse arquivo.

O design gerado precisa conter:
1. Repositório monorepo Kotlin API + React UI (mesma origem em produção).
2. Spring Boot 4.1.x compatível com JDK21, Kotlin, Gradle e starters corretos.
3. PostgreSQL, Flyway, configuração local/test/produção e variáveis de ambiente sem secrets.
4. OpenAPI 3.1, geração de clientes/tipos TS, Problem Details com code/correlation ID.
5. Base design system e UI sem lógica mock disfarçada de dados de negócio.
6. Testcontainers, testes unitários e CI que realmente executa scripts existentes.
7. Documentação para rodar localmente com comandos concretos.

O Kiro deve propor `tasks.md` **após review do design**, com backend e frontend implementados/testados incrementalmente, e preservar o escopo de bootstrap (sem módulo de reservas antes da hora).
