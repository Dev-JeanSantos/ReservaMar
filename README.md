# ReservaMar — Kit de fundação para Kiro

> **Estado:** documentação primária de produto e arquitetura (18/10/2026). **Não é um aplicativo implementado.** Nome comercial provisório e hipóteses de mercado pendentes de validação.

## Objetivo
Micro-SaaS B2B, multiempresa, para operadores brasileiros de **pescarias embarcadas compartilhadas**. Operadores gerenciam barcos, saídas, vagas, reservas, sinais Pix **manualmente conciliados** e conversas abertas pelo WhatsApp. O MVP **não** oferece checkout, marketplace, confirmação automática de Pix, integração ativa com a Meta nem autoatendimento do turista.

## Leitura na ordem correta
1. `docs/START-IN-KIRO.md`: primeira conversa e ritual de aprovação no Kiro.
2. `.kiro/steering/`: decisões permanentes que orientam todas as mudanças.
3. `docs/adr/`: decisões e justificativas arquiteturais.
4. `docs/domain/`: modelo, invariantes, estados e casos extremos.
5. `docs/architecture/` + `docs/api/`: fronteiras e contratos.
6. `docs/design/`: design system, telas e fluxo para desktop/celular.
7. `docs/spec-seeds/`: insumos independentes para geração de Feature Specs no Kiro.
8. `.kiro/specs/01-foundation-bootstrap/requirements.md`: exemplo de requisitos EARS já estruturado para a primeira spec; **peça ao Kiro gerar/revisar design.md e tasks.md** com gates humanos.
9. `docs/quality/definition-of-done.md`: checklist de revisão por feature.

## Como usar
Extraia todo o conteúdo **na raiz do repositório** aberto no Kiro (mantendo o diretório oculto `.kiro/`). Leia `docs/START-IN-KIRO.md` e cole o prompt inicial no chat Kiro usando **Feature Spec / Requirements-First**, revisando requirements → design → tasks antes da implementação. **Não solicite 'construa tudo' em uma sessão.**

## Stack proposta
- API: Kotlin 2.2+ / JDK 21 / Spring Boot 4.1.x (baseline testada na geração) / Spring MVC / Spring Security / Gradle Kotlin DSL.
- Dados: PostgreSQL 17+ / Flyway / Spring Data JPA ou JDBC conforme complexidade do agregado; migrations como fonte de verdade.
- UI: React 19 + TypeScript / Vite / React Router / TanStack Query / React Hook Form + Zod / Tailwind CSS + shadcn/ui (componentes copiados e auditados).
- Testes: JUnit 5, AssertJ, Testcontainers PostgreSQL e MockMvc para API; Vitest, React Testing Library, MSW e Playwright para UI/E2E.
- Deploy: Docker Compose local; deploy monolítico e frontend estático sob mesmo domínio via reverse proxy; infraestrutura gerenciada a definir no piloto.

**Versões:** a base Spring Boot 4.1.1 era estável em 18/10/2026; Kiro deverá validar versões **mutuamente compatíveis** e gravá-las no lockfile, wrapper e version catalog durante a spec de bootstrap. Evitar dependências inventadas ou copiar exemplos de Spring Boot 3 para 4 sem checagem.

## Fora do MVP
Pousadas, mercado de oferta ao turista, split de pagamentos, estornos automatizados, cobrança de assinatura, WhatsApp Cloud API, IA generativa, native mobile, offline transacional, multiidioma, microserviços, event bus e BI avançado.

## Restrições críticas
Jamais ultrapassar a capacidade da saída; nunca expor dados entre operadores; nunca marcar Pix como confirmado sem registro explícito do operador; não armazenar cartão; não enviar mensagem automática sem consentimento e integração legalmente configurada; nunca confiar apenas na validação do frontend.

## Natureza do pacote
Este é um **pacote de documentos**, não uma implementação, uma homologação de segurança nem uma comprovação de que há demanda comercial. Regras negociáveis estão identificadas como hipóteses / itens a validar com design partners.
