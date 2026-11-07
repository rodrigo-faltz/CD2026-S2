# Roteiro do vídeo (até 5 minutos)

Duração planejada: **4min35s**, com cerca de 25 s de margem. Um slide por bloco; os tempos são cumulativos.

## Slide 1 — Abertura (0:00–0:20)

Nosso projeto usa vibração real de rolamentos para responder duas perguntas: o rolamento ainda está normal? E, se não
está, onde é o defeito? Mas a pergunta que guiou o trabalho foi outra: quando um modelo acerta, ele aprendeu o defeito
ou só reconheceu o rolamento?

## Slide 2 — Dados (0:20–0:55)

Usamos o dataset da Case Western Reserve University: um motor de 2 HP com rolamentos que receberam defeitos por
eletroerosão na pista interna, na esfera e na pista externa, em três tamanhos e quatro cargas. São 40 gravações reais.
Uma decisão importante: usamos só a coleção de 48 kHz, a mesma taxa das gravações normais. Assim os modelos não podem
aprender a diferença de aquisição no lugar da falha. Todos os arquivos têm o hash conferido.

## Slide 3 — Análise de envelope (0:55–1:40)

Cada vez que uma esfera passa pelo defeito há um impacto, que excita uma ressonância. Filtramos o sinal na banda mais
impulsiva, escolhida pela curtose espectral, e calculamos o espectro do envelope. Os picos aparecem nas frequências
previstas pela geometria do rolamento: 106 Hz para pista externa, 160 para pista interna. Na pista externa os picos são
nítidos; na pista interna, o defeito gira com o eixo e o pico vem modulado; na esfera não há pico claro, como relata a
literatura. Juntamos esses indicadores físicos a atributos estatísticos, num total de 23 por janela.

## Slide 4 — Métodos e avaliação (1:40–2:15)

Para detectar, treinamos cinco detectores só com dados normais, de um indicador simples até um autoencoder. Para
diagnosticar, usamos Random Forest, SVM e uma regra física: vence o maior pico de envelope. E fizemos dois testes,
sempre separando gravações inteiras: carga nova, em que o modelo vê o mesmo rolamento em outra carga, e diâmetro novo,
em que o tamanho de defeito nunca foi visto. O segundo teste é o que mais se aproxima de um defeito novo em campo.

## Slide 5 — Detecção (2:15–2:55)

Os escores dos detectores separam normal e falha quase perfeitamente: a área sob a curva ROC fica entre 0,975 e 1. O
problema é o limiar. Temos só quatro gravações normais, uma por carga, e o normal de 0 HP é diferente dos outros: quando
ele está no teste, os detectores disparam em 64 a 100% das janelas. Quando damos ao detector uma referência normal da
mesma carga, a distância de Mahalanobis detecta todas as falhas sem nenhum alarme falso. Ou seja, a detecção funciona;
falta referência normal.

## Slide 6 — Diagnóstico com carga nova (2:55–3:25)

Com carga nova, a Random Forest acerta 96,8% das janelas e a SVM 93%, contra 30% do baseline. Por gravação, 90 a 92,5%.
Os erros se concentram em 0 HP, onde as gravações são mais curtas, e no defeito de 0,014 polegada.

## Slide 7 — Diagnóstico com diâmetro novo (3:25–4:05)

Aqui o resultado se inverte. Com um tamanho de defeito nunca visto, os mesmos modelos caem abaixo do acaso: eles jogam
todas as gravações do diâmetro novo numa única classe. Só os atributos de envelope mantêm algum desempenho, e a regra
física acerta 69% das gravações. Conclusão: boa parte dos 95% com carga nova vem de reconhecer o rolamento, não o tipo
de defeito.

## Slide 8 — Conclusões (4:05–4:35)

Detectar é fácil com uma referência normal local. O aprendizado de máquina diagnostica bem um rolamento conhecido, mas,
para um defeito novo, a física do rolamento generaliza melhor. As limitações são poucos dados normais, defeitos
induzidos e uma única bancada. Usamos ferramentas de IA como apoio, como declaramos no relatório. Código, dados e
relatório estão no repositório. Obrigado.
