# API seed — endpoints e contratos iniciais

Esta página é um **esboço contratual**, não um OpenAPI completo. A spec de bootstrap deve configurar publicação OpenAPI 3.1; specs seguintes expandem-no e geram tipos TypeScript. JSON usa strings ISO-8601 UTC (`Z`), moeda em centavos, UUID; endpoints sob `/api/v1`.

## Auth e contexto
| Método | Rota | Função | Acesso |
|---|---|---|---|
| POST | `/auth/login` | autenticar e obter sessão cookie | público com rate limit |
| POST | `/auth/logout` | destruir sessão | autenticado |
| GET | `/auth/me` | dados mínimos, operador ativo e role | autenticado |
| GET | `/auth/csrf` | token CSRF no cookie/response conforme implementação | público/anon seguro |

Auth mesma origem: envio `credentials: 'include'`, cookie HttpOnly, token CSRF em header em POST/PATCH/DELETE. Não expor password em logs nem resposta.

## Catálogo e saídas
| Método | Rota | Resultado |
|---|---|---|
| GET, POST | `/boats` | listar/criar embarcação do operador |
| PATCH | `/boats/{id}` | alterar/inativar, sem quebrar saídas |
| GET, POST | `/activities` | listar/criar atividade |
| PATCH | `/activities/{id}` | alterar/inativar |
| GET, POST | `/departures` | listar/criar saídas |
| GET, PATCH | `/departures/{id}` | ler/editar com validação da capacidade |
| GET | `/departures/{id}/availability` | saldo e instante de leitura |
| POST | `/departures/{id}/close` | interromper novas vendas |
| POST | `/departures/{id}/cancel` | cancelar saída e bloquear novas reservas |

## Clientes e reservas
| Método | Rota | Resultado |
|---|---|---|
| GET, POST | `/customers` | buscar/criar contato |
| GET | `/customers/{id}` | detalhes mínimos |
| GET, POST | `/bookings` | listar/criar reserva (POST exige `Idempotency-Key`) |
| GET | `/bookings/{id}` | detalhe, vencimento e saldo |
| POST | `/bookings/{id}/confirm` | confirmar após depósito/dispensa |
| POST | `/bookings/{id}/cancel` | cancelar com motivo |
| GET | `/dashboard/summary` | números úteis, derivados do banco |

## Recebimentos manuais
| Método | Rota | Resultado |
|---|---|---|
| GET, POST | `/bookings/{id}/payment-entries` | listar/lançar recebimento manual |
| POST | `/bookings/{id}/payment-entries/{entryId}/reverse` | lançar ajuste negativo com motivo |

## Exemplos de contrato
`POST /api/v1/bookings` header `Idempotency-Key: <uuid>`:
```json
{
  "departureId": "e4ce8806-cf54-4456-abf1-14cfcac1698d",
  "customerId": "ddf6e3a2-e013-45ba-8d3e-a0eb9039b997",
  "seats": 2,
  "notes": "Preferência de contato pela manhã"
}
```
Response 201:
```json
{
  "id": "8f340b97-df72-4a96-8d3a-fb50893a413f",
  "status": "PENDING",
  "seats": 2,
  "totalCents": 60000,
  "requiredDepositCents": 18000,
  "holdExpiresAt": "2026-10-19T09:00:00Z",
  "createdAt": "2026-10-18T21:00:00Z"
}
```
Exemplo de conflito de capacidade `409 application/problem+json`:
```json
{
  "type": "https://example.invalid/problems/capacity-conflict",
  "title": "Vagas indisponíveis",
  "status": 409,
  "code": "CAPACITY_CONFLICT",
  "detail": "A quantidade solicitada ultrapassa as vagas disponíveis.",
  "availableSeats": 1,
  "correlationId": "b4ccaeff02"
}
```
**Nota:** `example.invalid` é placeholder; Kiro deve substituir pela URI de documentação do próprio serviço, sem inventar domínio comercial.

## Política HTTP mínima
- 200 consultas; 201 criação; 204 ação sem corpo; 400 JSON inválido; 401 não autenticado; 403 sem role; 404 desconhecido/outra empresa; 409 capacidade/idempotência/estado; 422 campos semanticamente inválidos; 429 rate limit; 500 erro inesperado com ID de correlação.
- Paginação `page/size` com size máximo 100, ordenação com allowlist; endpoints de listagem sempre filtram tenant.
- Escritas com `Idempotency-Key` persistida e TTL documentado para reservas e pagamentos; falhas de rede devem permitir retry seguro.
- Definir semântica de `If-Match` ou lock otimista para edições concorrentes de telas; não assumir last-write-wins em capacidade.
