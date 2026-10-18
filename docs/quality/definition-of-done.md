# Checklist de qualidade — DoR / DoD por spec e por task

## Definition of Ready (requisitos e design)
- [ ] Problema e persona identificados; objetivo observável e métrica.
- [ ] Escopo IN / OUT escrito; dependências e riscos conhecidos.
- [ ] IDs `BR-xxx` mapeados para critérios EARS e casos de erro.
- [ ] Regras de tenant/role, datas UTC/fuso e centavos esclarecidas.
- [ ] Design com endpoints, contratos, estados e migrations definidas; exemplos JSON.
- [ ] Frontend com telas, estados loading/empty/error/409/422/success, mobile e acessibilidade.
- [ ] Sequência entre API/DB/UI consistente; testes de concorrência onde cabíveis.
- [ ] Requirements e design aprovados explicitamente antes de gerar/executar tasks.

## Definition of Done (toda task)
- [ ] Implementação limitada à spec, sem nova tecnologia não aprovada.
- [ ] Código compilado/lintado/formatado; nenhuma credencial ou PII no git/log.
- [ ] APIs versionadas, DTOs e `Problem Details` consistentes; contrato OpenAPI atualizado.
- [ ] Domínio/serviços testados: happy path, validação, não autorizado, outro tenant, estado impossível, idempotência.
- [ ] Alteração de DB com migration incremental e constraints/índices; teste em PostgreSQL real quando envolvido.
- [ ] Se altera inventário/vagas: teste concorrente real demonstrando nenhuma reserva acima da capacidade.
- [ ] Frontend com estados vazios/erro/loading, controles acessíveis e interface mobile e desktop.
- [ ] Teste de integração UI/API com HTTP real ou E2E; MSW apenas para testes isolados.
- [ ] Comandos reais de lint, build, unit, integration e E2E executados, ou impossibilidade relatada com razão exata (não marcar done se bloqueado).
- [ ] Mapeamento de requirement IDs ↔ testes; regressão crítica preservada.
- [ ] Documentação atualizada: README, OpenAPI, ADR se necessário; task marcada após revisão.
- [ ] Relatório final: arquivos alterados, comandos/resultados, screenshots quando possível, riscos e pendências.

## Critérios de release piloto
- [ ] Teste ponta a ponta no celular: login → barco → atividade → saída → contato → reserva → Pix manual → confirmação → cancelamento.
- [ ] Teste 2 tenants com operações cruzadas negadas, incluindo listagens e agregados.
- [ ] 10 concorrentes disputando 2 vagas sem overbooking.
- [ ] Reenvio idempotente na falha de rede; sessão/cookies/CSRF validados.
- [ ] Backup PostgreSQL restaurado em ambiente de teste e retenção definida.
- [ ] Segredos fora do repositório, HTTPS, logs sem PII, CORS/same-origin conferidos.
- [ ] Textos de privacidade/contato e termos de uso revisados antes de dados reais.
- [ ] Operador piloto testou 5 reservas reais/assistidas e informou ao menos 3 melhorias.
- [ ] Custos reais de infraestrutura e suporte contabilizados para não vender abaixo do custo.

## Tarefas de automação no CI (alvo)
- `./gradlew ktlintCheck detekt test integrationTest bootJar` ou comandos reais configurados durante bootstrap.
- `npm ci && npm run lint && npm run typecheck && npm run test:run && npm run build` em `apps/web`.
- `npx playwright test` E2E em ambiente de CI preparado.
**Não assumir que esses scripts já existem neste pacote; a spec de bootstrap deve criá-los e validar nomes e execução.**
