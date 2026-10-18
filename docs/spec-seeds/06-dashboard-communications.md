# Seed 06 — Dashboard operacional + atalho WhatsApp

**Depende de:** 04 e 05. **ADRs:** 0001 e 0004. **Regras:** BR-012, 016–018, 022.

## Problema
Atendente precisa identificar rapidamente saídas próximas, vagas e reservas pendentes sem navegar por várias telas. Deseja iniciar conversa manual com cliente.

## Escopo IN
- `GET /dashboard/summary` com reservas pendentes não expiradas, saídas futuras, vagas livres nas próximas saídas e notificações operacionais (sem sistema de push).
- Lista de próximas saídas ordenada por horário, filtros básicos e atalhos para detalhes.
- Pendências: reservas com hold próximo de expirar; se pagamento registrado e booking expirado, destaque conciliação/atendimento.
- Botão `Conversar no WhatsApp` que abre `https://wa.me/<digits>?text=<encodeURIComponent(message)>` apenas após clique, com telefone normalizado e mensagem revisável.
- UI mobile-first, cards úteis, estados vazios, loading/error, skeleton e testes de navegação.

## EARS mínimos
- WHEN OWNER/STAFF abre dashboard THEN SHALL ver dados somente do operador ativo e contagens coerentes com disponibilidade derivada no servidor.
- WHEN não há reservas THEN SHALL apresentar empty state e CTA `Criar saída`, sem números fabricados.
- WHEN cliente tem telefone válido e operador aciona WhatsApp THEN SHALL abrir link externo para chat (não enviar servidor-side).
- WHEN telefone inválido THEN SHALL desabilitar link e orientar correção, sem navegar para destino incorreto.
- WHEN sessão muda/logout THEN SHALL limpar cache/dados privados no frontend.
- WHEN hold vence THEN SHALL refletir contador atualizado na próxima consulta/refresh, sem manter vaga ocupada.

## Design.md deve cobrir
Queries e índices eficientes, agregados tenant-safe, evitar N+1, estratégia de refetch TanStack Query, proteção dados em métricas, protocolo de link, responsividade, acessibilidade, deep link seguro.

## tasks.md deve incluir
Endpoint + testes reais, UI cards e filtros, hooks query, componentes padrão e labels pt-BR, testes para timezone, URL encoding, links inválidos, E2E fluxo mobile e segurança entre tenants.

## Não objetivos
Disparo de mensagem via Meta, automação, IA de atendimento, notificações push, ranking de vendedores, BI financeiro detalhado.
