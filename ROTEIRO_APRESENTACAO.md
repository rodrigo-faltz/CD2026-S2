# Roteiro da apresentação (5 integrantes)

Apresentação: [`APRESENTACAO.html`](APRESENTACAO.html) — 15 slides narrados, três por integrante, e 4 slides de apêndice para perguntas (sem fala). Duração estimada: **4:07** de fala a 155 palavras por minuto; com trocas de slide e de integrante, cerca de 4min30s, abaixo do limite de 5 minutos do enunciado. Abra o HTML no navegador, use **→ / ←** para navegar, **N** para ver a fala de cada slide e **F** para tela cheia. No vídeo, encerrem no slide 15; o apêndice fica para a correção e para perguntas.

## Divisão

| Integrante | Slides | Temas | Tempo | Palavras |
|---|---|---|---|---|
| Integrante 1 | 1–3 | abertura, contexto, problema | 0:00–0:51 | 133 |
| Integrante 2 | 4–6 | dados, atributos | 0:51–1:39 | 123 |
| Integrante 3 | 7–9 | análise de envelope, métodos, protocolo | 1:39–2:28 | 127 |
| Integrante 4 | 10–12 | detecção, diagnóstico | 2:28–3:17 | 126 |
| Integrante 5 | 13–15 | generalização, discussão crítica, conclusões | 3:17–4:07 | 130 |

Troquem "Integrante N" pelos nomes antes de gravar e preencham os nomes e RAs no slide 1.

## Cobertura do enunciado

O enunciado (seção 6, item 4) pede um vídeo de no máximo 5 minutos no YouTube, com os slides usados. A tabela liga cada critério da rubrica (seção 7) aos slides em que ele aparece.

| Critério da rubrica | Peso | Slides |
|---|---|---|
| Levantamento e seleção dos métodos | 1 | 2, 3, 8 |
| Aplicação dos métodos e métricas | 2 | 6, 7, 9 |
| Resultados de detecção | 2 | 10, 11 |
| Resultados de classificação | 1 | 12, 13, apêndices A–C |
| Qualidade da discussão crítica | 2 | 11, 13, 14 |
| Apresentação | 1 | todos |

Itens do relatório que o enunciado pede e onde aparecem na apresentação: descrição do dataset (slides 4 e 5), fundamentação com referências (slides 2, 8 e apêndice D), metodologia (slides 6, 7 e 9), tabela resumo e matrizes de confusão (slide 12 e apêndices A e B), discussão crítica (slides 13 e 14), uso de IA (slide 15).

## Falas

### Slide 1 — Abertura · Integrante 1 (0:00–0:19)

*Critério: Apresentação*

Olá! Nosso trabalho detecta e diagnostica falhas em rolamentos pela vibração. Esse traço é um sinal real do dataset, com defeito na pista externa: cada pico é uma esfera batendo no defeito. A pergunta central foi: quando o modelo acerta, ele aprendeu o defeito ou só reconheceu o rolamento?

### Slide 2 — Contexto · Integrante 1 (0:19–0:36)

*Critério: Levantamento e seleção dos métodos*

Um defeito localizado gera um impacto a cada passagem de esfera. A frequência desses impactos depende da geometria e da rotação: cerca de 106 hertz na pista externa, 139 na esfera e 160 na pista interna. É essa assinatura que procuramos no sinal.

### Slide 3 — Problema · Integrante 1 (0:36–0:51)

*Critério: Levantamento e seleção dos métodos*

O enunciado pede detectar e diagnosticar. Fizemos três perguntas: só com dados normais, dá para alarmar sem alarme falso? Dá para dizer onde está o defeito? E isso funciona numa carga ou num tamanho de defeito que o modelo nunca viu?

### Slide 4 — Dados · Integrante 2 (0:51–1:09)

*Critério: Apresentação · descrição do dataset*

Usamos o dataset da Case Western, sugerido no enunciado: um motor de 2 HP com defeitos feitos por eletroerosão. Escolhemos só a coleção de 48 quilohertz, a mesma taxa dos normais, para que o modelo não aprenda a diferença de aquisição no lugar da falha.

### Slide 5 — Dados · Integrante 2 (1:09–1:24)

*Critério: Apresentação · quantidade de amostras por classe*

São 40 gravações e 995 janelas de 0,34 segundo. O normal tem só quatro gravações, uma por carga. Conferimos o hash de cada arquivo e tratamos as peculiaridades da fonte, como o arquivo 174, com só 1,3 segundo de sinal.

### Slide 6 — Atributos · Integrante 2 (1:24–1:39)

*Critério: Aplicação dos métodos*

Extraímos 23 atributos por janela, em quatro grupos: amplitude, forma de onda, espectro e envelope. Comparamos três conjuntos. O principal tira a amplitude, que muda com a carga, e acrescenta o envelope, que carrega a física do rolamento.

### Slide 7 — Análise de envelope · Integrante 3 (1:39–1:57)

*Critério: Aplicação dos métodos*

A análise de envelope é a técnica clássica para rolamentos. Escolhemos a banda mais impulsiva pela curtose espectral, filtramos, tiramos o envelope e olhamos o espectro. Na pista externa os picos em 106, 212 e 318 hertz são nítidos; na esfera, não há pico claro.

### Slide 8 — Métodos · Integrante 3 (1:57–2:12)

*Critério: Levantamento e seleção dos métodos*

Para detectar, usamos cinco detectores treinados só com dados normais, de um indicador de curtose até um autoencoder. Para diagnosticar, Random Forest, SVM, uma regra física e um baseline. Cada técnica tem pelo menos duas referências, incluindo aplicações em rolamentos.

### Slide 9 — Protocolo · Integrante 3 (2:12–2:28)

*Critério: Aplicação dos métodos e métricas*

Avaliamos de dois jeitos, sempre separando gravações inteiras: deixando uma carga de fora e deixando um tamanho de defeito de fora. O limiar de detecção usa normais fora da amostra, e os hiperparâmetros são escolhidos em validação interna, sem tocar no teste.

### Slide 10 — Detecção · Integrante 4 (2:28–2:48)

*Critério: Resultados de detecção*

Com carga nova, os escores separam bem: a área sob a curva ROC vai de 0,975 a 1. Mas o limiar não transfere: o normal de 0 HP dispara alarme em 64 a 100% das janelas. O melhor compromisso foi o Isolation Forest, com 81% de detecção e 9% de falso positivo.

### Slide 11 — Detecção · Integrante 4 (2:48–3:02)

*Critério: Resultados de detecção · discussão*

Quando há uma referência normal da mesma carga, o cenário muda: Mahalanobis detecta 100% das falhas sem nenhum alarme falso. Então a detecção funciona; o que falta são dados normais de cada condição de operação.

### Slide 12 — Diagnóstico · Integrante 4 (3:02–3:17)

*Critério: Resultados de classificação*

No diagnóstico com carga nova, a Random Forest acerta 96,8% das janelas e a SVM 93%, contra 30% do baseline. Por gravação, de 90 a 92,5%. Os erros se concentram em 0 HP e no defeito de 0,014 polegada.

### Slide 13 — Generalização · Integrante 5 (3:17–3:31)

*Critério: Resultados de classificação · discussão crítica*

Com um tamanho de defeito novo, o resultado se inverte. Os modelos estatísticos ficam abaixo do acaso e jogam o diâmetro inteiro numa única classe. Só o envelope resiste, e a regra física acerta 69% das gravações.

### Slide 14 — Discussão crítica · Integrante 5 (3:31–3:51)

*Critério: Qualidade da discussão crítica*

Funcionou o envelope nas pistas, a detecção com referência local e o diagnóstico com carga nova. Não funcionou transferir o limiar, generalizar para diâmetro novo e reconhecer esfera. O motivo: cada diâmetro é um rolamento físico, e os modelos aprendem sua assinatura. Por isso abandonamos nossa primeira versão, de 99%.

### Slide 15 — Conclusões · Integrante 5 (3:51–4:07)

*Critério: Apresentação*

Alta acurácia não basta: é preciso perguntar o que o modelo aprendeu. As limitações são poucos dados normais, defeitos induzidos e uma única bancada. Com mais tempo, gravaríamos mais referências e testaríamos no Paderborn. Usamos IA como apoio, como declaramos no relatório. Obrigado!

## Apêndice (sem fala)

| Slide | Conteúdo |
|---|---|
| 16 | Apêndice A: Tabela resumo exigida pelo enunciado |
| 17 | Apêndice B: Matrizes de confusão completas |
| 18 | Apêndice C: Erros por gravação |
| 19 | Apêndice D: Referências principais |

## Dicas para a gravação

- Ensaiem com cronômetro. Se passar de 4min50s, encurtem as falas dos slides 5, 9 e 14, que são as mais longas.
- Cada integrante deve dominar os números do próprio bloco: quem fala nos slides 10 a 13 precisa explicar a curva ROC, a matriz de confusão e por que o resultado com diâmetro novo fica abaixo do acaso.
- Na troca de integrante, quem entra começa direto no conteúdo, sem cumprimentar de novo.
- O slide fica na tela enquanto a pessoa fala: não é preciso ler as tabelas, só apontar o número principal.
- Publiquem o vídeo como público ou não listado, confiram se abre sem login e coloquem o link no README.
