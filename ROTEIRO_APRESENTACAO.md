# Roteiro da apresentação (5 integrantes)

Apresentação: [`APRESENTACAO.html`](APRESENTACAO.html) — 10 slides, dois por integrante. Duração estimada: **3:49** de fala a 150 palavras por minuto; com trocas de slide e de integrante, cerca de 4min15s a 4min30s, abaixo do limite de 5 minutos do enunciado. Abra o HTML no navegador, use **→ / ←** para navegar, **N** para ver a fala de cada slide e **F** para tela cheia.

## Divisão

| Integrante | Slides | Tema | Tempo |
|---|---|---|---|
| Integrante 1 | 1–2 | Abertura e problema | 0:00–0:47 |
| Integrante 2 | 3–4 | Dados e atributos | 0:47–1:35 |
| Integrante 3 | 5–6 | Métodos e detecção | 1:35–2:21 |
| Integrante 4 | 7–8 | Diagnóstico e generalização | 2:21–3:06 |
| Integrante 5 | 9–10 | Discussão crítica e conclusões | 3:06–3:49 |

Troque "Integrante N" pelos nomes antes de gravar e preencha os nomes e RAs no slide 1.

## Cobertura do enunciado

O enunciado (seção 6, item 4) pede um vídeo de no máximo 5 minutos no YouTube com os slides usados. A rubrica (seção 7) avalia os itens abaixo; a tabela mostra onde cada um aparece na fala.

| Critério da rubrica | Peso | Slides |
|---|---|---|
| Levantamento e seleção dos métodos | 1 | 2, 4, 5 |
| Aplicação dos métodos e métricas | 2 | 4, 5 |
| Resultados de detecção | 2 | 6 |
| Resultados de classificação | 1 | 7, 8 |
| Qualidade da discussão crítica | 2 | 8, 9 |
| Apresentação | 1 | todos |

## Falas

### Slide 1 — Abertura · Integrante 1 (0:00–0:24)

*Critério: Apresentação*

Olá! Nosso trabalho é sobre detectar e diagnosticar falhas em rolamentos usando vibração. Esse traço na tela é um sinal real do nosso dataset: um rolamento com defeito na pista externa. Cada pico é uma esfera batendo no defeito. A pergunta que guiou o projeto foi: quando o modelo acerta, ele aprendeu o defeito ou só reconheceu o rolamento?

### Slide 2 — Problema · Integrante 1 (0:24–0:47)

*Critério: Levantamento e seleção dos métodos*

O enunciado pede duas coisas: detectar que algo mudou e identificar o que mudou. Transformamos isso em três perguntas. Detecção: só com dados normais, dá para alarmar sem alarme falso? Diagnóstico: o defeito está na pista interna, na esfera ou na pista externa? E generalização: isso funciona numa carga ou num tamanho de defeito que o modelo nunca viu?

### Slide 3 — Dados · Integrante 2 (0:47–1:12)

*Critério: Apresentação · descrição do dataset*

Usamos o dataset da Case Western Reserve University, sugerido no enunciado: um motor de 2 HP com defeitos feitos por eletroerosão, em três tamanhos e quatro cargas. São 40 gravações reais. Usamos só a coleção de 48 quilohertz, a mesma taxa das gravações normais. Assim não reamostramos nada e o modelo não aprende a diferença de aquisição no lugar da falha.

### Slide 4 — Atributos · Integrante 2 (1:12–1:35)

*Critério: Aplicação dos métodos*

Além de estatísticas como curtose, usamos a análise de envelope, a técnica clássica para rolamentos. Filtramos na banda mais impulsiva, tiramos o envelope e olhamos o espectro dele. Os picos aparecem onde a geometria prevê: 106 hertz na pista externa, 160 na interna. Na pista externa são nítidos; na esfera, não há pico claro, como diz a literatura.

### Slide 5 — Métodos · Integrante 3 (1:35–1:56)

*Critério: Aplicação dos métodos e métricas*

Para detectar, treinamos cinco detectores só com dados normais, de um indicador simples de curtose até um autoencoder. Para diagnosticar, Random Forest, SVM e uma regra física: vence o maior pico de envelope. Avaliamos de dois jeitos, sempre separando gravações inteiras: deixando uma carga de fora e deixando um tamanho de defeito de fora.

### Slide 6 — Detecção · Integrante 3 (1:56–2:21)

*Critério: Resultados de detecção*

Os escores separam normal e falha quase perfeitamente: a área sob a curva ROC fica entre 0,975 e 1. O problema é o limiar. Só temos quatro gravações normais, e a de 0 HP é diferente das outras. Mas, com uma referência normal da mesma carga, Mahalanobis detecta todas as falhas sem nenhum alarme falso. A detecção funciona; falta referência normal.

### Slide 7 — Diagnóstico · Integrante 4 (2:21–2:42)

*Critério: Resultados de classificação*

No diagnóstico com uma carga nova, a Random Forest acerta 96,8% das janelas e a SVM 93%, contra 30% do baseline que sempre chuta a classe mais comum. Por gravação, de 90 a 92,5%. Os erros se concentram em 0 HP, onde as gravações são mais curtas, e no defeito de 0,014 polegada.

### Slide 8 — Generalização · Integrante 4 (2:42–3:06)

*Critério: Resultados de classificação · discussão*

Mas, com um tamanho de defeito que o modelo nunca viu, o resultado se inverte. Com atributos estatísticos, os modelos ficam abaixo do acaso e jogam o diâmetro novo inteiro numa única classe. Só o envelope mantém algum desempenho, e a regra física acerta 69% das gravações. Boa parte dos 95% vinha de reconhecer o rolamento, não o defeito.

### Slide 9 — Discussão crítica · Integrante 5 (3:06–3:28)

*Critério: Qualidade da discussão crítica*

Funcionou: o envelope nas pistas, a detecção com referência local e o diagnóstico com carga nova. Não funcionou: transferir o limiar entre cargas, generalizar para diâmetros novos e reconhecer esfera. O porquê: cada tamanho de defeito é um rolamento gravado numa sessão, e os modelos estatísticos aprendem essa assinatura. Por isso abandonamos nossa primeira versão, de 99%.

### Slide 10 — Conclusões · Integrante 5 (3:28–3:49)

*Critério: Apresentação*

Alta acurácia não basta: é preciso perguntar o que o modelo aprendeu. As limitações são poucos dados normais, defeitos induzidos e uma única bancada. Com mais tempo, gravaríamos mais referências normais e testaríamos com rolamentos novos e com o dataset de Paderborn. Usamos IA como apoio, como declaramos no relatório. Obrigado!

## Dicas para a gravação

- Ensaiem com cronômetro: se passar de 4min50s, cortem frases dos slides 3 e 5, que têm mais detalhe técnico.
- Na troca de integrante, quem entra começa a falar já no slide seguinte, sem cumprimentar de novo.
- Quem apresentar os slides 6 a 9 deve conseguir explicar as figuras: curva ROC, matriz de confusão e por que o resultado com diâmetro novo fica abaixo do acaso.
- Publiquem o vídeo como público ou não listado, confiram se abre sem login e coloquem o link no README.
