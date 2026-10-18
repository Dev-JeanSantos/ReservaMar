# Design Partners — validação comercial e UX com operadores piloto

**Definição:** Design Partner é um operador de pescaria/passeio que participa das entrevistas, testa protótipos e dá feedback antes de escalarmos o produto. Não confundir com a biblioteca de componentes ou padrões de software.

## Perfil inicial
- 2–3 empresas de pescaria embarcada compartilhada, preferencialmente com até poucas embarcações e reservas frequentes por WhatsApp.
- Variar uma operação mais informal (caderno/WhatsApp) e outra já usando planilha/software, para distinguir dor real de hábito de trabalho.
- Recrutar de forma ética por relacionamento ou contato público; explicar que o produto ainda é piloto sem garantia de funcionalidades futuras.

## Entrevista de descoberta (antes do software)
1. Mostre como registra uma reserva real hoje, desde primeiro contato até embarque.
2. Quem decide número de vagas, preço, horário e sinal? Em qual etapa a vaga fica indisponível?
3. O que acontece quando dois atendentes atendem ao mesmo tempo?
4. Quantas reservas por semana e quantos cancelamentos ocorrem? Peça intervalos, não chute.
5. Como confere Pix e comprova recebimento? Evite coletar dados bancários/documentos pessoais.
6. O que mais toma tempo? Que falhas já causaram prejuízos?
7. Quanto pagaria por um painel que resolvesse esse problema — e o que ele teria de economizar para valer a pena?
8. Aceitaria testar durante 2–4 semanas, com treinamento de 15 minutos e feedback semanal?

## Teste de usabilidade (15–30 minutos)
- Sem instruções detalhadas, peça: criar barco, publicar saída, reservar 2 vagas, registrar sinal e confirmar.
- Observe tempo, cliques errados, termos confusos, falha ao interpretar estados e uso real de 390px no celular.
- Simule outra pessoa pegando a última vaga; confirme se a explicação de 409 é clara.
- Pergunte o que falta e o que poderia ser eliminado. Recolha consentimento antes de gravar sessão.

## Critérios de avanço do piloto (hipóteses, revisar)
- Pelo menos 2 operadores completam o fluxo principal com dados de teste sem assistência em <=8 minutos após breve orientação.
- Zero conflitos de vagas em testes simultâneos; zero acesso cruzado entre empresas.
- >=1 operador disposto a pagar valor explícito depois do piloto; interesse verbal sozinho não vale como receita.
- Custo de suporte estimado por conta e capacidade real de dedicar <=4–6 horas semanais a manutenção/negócio.

## Controle de feedback
Tabela recomendada no repositório privado (sem PII): `Data | Tipo de operador | Tarefa testada | Problema observado | Gravidade | Frequência | Decisão | Spec impactada`.

## Segurança comercial
Antes de usar dados reais, validar condições comerciais, política de privacidade e tratamento de dados com revisão apropriada. Operadores são responsáveis por licenças e exigências do serviço turístico/náutico; ReservaMar não certifica ou garante habilitação regulatória.
