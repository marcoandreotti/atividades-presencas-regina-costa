# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

A equipe do Núcleo de Convivência Regina Costa que organiza encontros e precisa consultar atividades e registrar presenças. Pessoas idosas atendidas pelo núcleo são beneficiárias indiretas das atividades. A familiaridade digital básica a intermediária e as barreiras de acesso são hipóteses descritas no planejamento acadêmico, ainda sem validação de campo.

## Product Purpose

Aplicação web acadêmica para organizar atividades e apoiar a chamada e a consulta de presença dos participantes. O sucesso do MVP é permitir que a equipe registre e confira uma chamada de modo claro e acessível. Organizar registros pode apoiar o planejamento de atividades inclusivas; o software sozinho não comprova inclusão nem impacto social.

## Positioning

Protótipo monolítico, em português brasileiro, para o fluxo de atividades e presenças do Núcleo de Convivência Regina Costa. Um posicionamento comercial ou diferencial comparativo não foi definido.

## Operating Context

Uso pela equipe organizadora para localizar encontros, marcar presença ou ausência e revisar o resumo. O projeto é desenvolvido e demonstrado localmente. Fluxo, ambiente e necessidades específicas ainda dependem de validação com a organização.

## Capabilities and Constraints

Aplicação Flask com páginas Jinja, SQLAlchemy e SQLite local. O esquema contém atividades, participantes e presenças, com restrições para valores válidos e duplicidade. O protótipo deve usar somente dados fictícios; não deve armazenar dados reais de participantes nem ser usado em produção. Autenticação e hospedagem remota não estão implementadas nem foram definidas para esta etapa.

## Brand Commitments

Nome: Registro de Atividades e Presenças do Núcleo de Convivência Regina Costa. Interface e textos em português brasileiro. A identidade existente em tons claros e teal deve ser mantida; essa preferência foi confirmada pelo usuário em 14/10/2026.

## Evidence on Hand

Entregas acadêmicas anteriores descrevem as personas hipotéticas, fluxo, requisitos e conexão indireta com ODS 10, Meta 10.2. Não há dados de campo, depoimentos, validação externa ou resultados de impacto confirmados. As demonstrações devem identificar com clareza os dados como fictícios.

## Product Principles

- Deixar claro qual encontro está sendo registrado.
- Apresentar escolhas e resultados por texto, sem depender somente de cor.
- Proteger participantes usando dados fictícios no protótipo.
- Apoiar a conferência e a correção da chamada.
- Tratar a relação com inclusão social como contribuição indireta e ainda não validada.

## Accessibility & Inclusion

A interface deve possibilitar navegação e operação por teclado e toque, com foco visível, rótulos associados, contraste suficiente, controles amplos, ampliação sem perda de conteúdo e estados comunicados por texto. Nenhuma deficiência específica dos operadores foi confirmada; os requisitos visam reduzir barreiras hipotéticas. A relação com ODS 10, Meta 10.2, é indireta e não comprova resultado social.
