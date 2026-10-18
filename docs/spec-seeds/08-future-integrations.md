# Seed 08 — Backlog futuro NÃO AUTORIZADO PARA IMPLEMENTAÇÃO NO MVP

**Gate prévio:** pelo menos 2 operadores ativos e validação de disposição de pagar; requisitos comerciais e orçamento revisados. **Criar ADR nova antes de implementar.**

## Possíveis specs separadas (não agrupar)
1. **Self-booking público**: link para turista reservar, política anti-abuso, disponibilidade, privacidade, confirmação/autenticação de telefone, antifraude e prevenção de double booking.
2. **Checkout Pix por PSP**: conta merchant do operador, webhooks autenticados e idempotentes, reembolso/chargeback, gestão de credenciais e termos de repasse; jamais receber pagamentos de turistas diretamente na conta da plataforma sem avaliação jurídica.
3. **WhatsApp Cloud API oficial**: opt-in/opt-out, templates, janela de atendimento, cobrança Meta e filas/retries auditáveis, dados mínimos.
4. **Assinaturas SaaS**: plano e limite de uso, billing para operadores, cobrança/nota fiscal conforme regime, trial, inadimplência sem perda indevida de dados.
5. **Fretamento exclusivo e multiproduto**: inventário por embarcação, bloqueios por horário e política de conflito; possível migração de domínio de capacidade.
6. **Pousadas**: NOVO bounded context de room inventory, tarifas por diária, overbooking entre canais e integração com OTAs; não reutilizar cegamente o modelo de Departure.

## Checklist de introdução
- Problema validado e preço potencial.
- Implicação legal/privacidade/consentimento revisada.
- ADR atualizada e risco/benefício/custo aprovado.
- Requirements EARS, design, tasks e segurança testáveis.
- Testes integrados com API de terceiros em sandbox e fallback de falha.
