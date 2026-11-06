# Roteiro para vídeo de até 5 minutos

**Duração planejada: 4min40s (280 segundos).** Reservar até 20 segundos de margem. Inserir nomes e RAs nos slides antes de gravar. Os tempos são metas de ensaio, não medição de um vídeo já gravado.

Grave a tela com os slides e a narração do grupo. Publique no YouTube como público ou não listado, confirme que o professor consegue abrir e insira o link real no README. A publicação não foi realizada por este pacote.

## Slide 1 — 0:00 a 0:20

Nosso projeto investiga duas tarefas: detectar que a vibração está anormal e identificar o tipo de falha. Usamos o CWRU e comparamos quatro modelos. O foco não é apenas obter alta acurácia, mas verificar o que acontece quando a carga do motor muda.

## Slide 2 — 0:20 a 0:55

A bancada possui motor de dois HP, dinamômetro e acelerômetros. Selecionamos o canal drive end, com normalidade e falhas na pista interna, na esfera e na pista externa. São três diâmetros e quatro cargas. Os sinais são reais; os defeitos foram induzidos por eletroerosão. Os arquivos oficiais têm seus hashes verificados. Adotamos baseline a 48 quilohertz, reduzido a 12, uma premissa explicitada e testada por sensibilidade, que precisa de conferência documental pelo grupo.

## Slide 3 — 0:55 a 1:35

Se janelas da mesma gravação aparecem no treino e no teste, a avaliação pode ficar otimista. Por isso dividimos por carga antes do janelamento: zero e um HP para treino, dois para validação e três para teste. Extraímos dezessete atributos, como RMS, curtose, centroide e energias relativas por faixa. A padronização usa apenas o treino. Isso elimina compartilhamento de gravações, mas não comprova separação entre rolamentos físicos, que podem ter sido medidos em várias cargas.

## Slide 4 — 1:35 a 2:10

Na detecção, o ajuste vê somente janelas normais. O limiar é o percentil noventa e cinco dos escores normais de validação. Já no diagnóstico utilizamos os rótulos das quatro classes. Comparamos uma pequena grade e escolhemos os parâmetros por macro-F1 na validação. A SVM com C igual a zero vírgula um já liderava nessa etapa. Mantivemos o teste reservado e incluímos um baseline majoritário para contextualizar as métricas.

## Slide 5 — 2:10 a 3:00

Na carga de teste, a SVM acertou quinhentas e oitenta e seis de quinhentas e noventa e uma janelas. Os cinco erros foram de esfera para pista externa, todos na gravação cento e oitenta e oito. A Random Forest teve oitenta e quatro vírgula sessenta por cento de acurácia e confundiu oitenta e nove janelas de pista interna com esfera. Portanto, detectar a presença de falha não é o mesmo que acertar sua origem. As matrizes completas mostram todas as quatro classes do recorte, e o relatório também apresenta os resultados por gravação.

## Slide 6 — 3:00 a 3:45

Os dois detectores encontraram todas as falhas, mas os falsos positivos revelam o problema. O Isolation Forest alarmou em quatorze das cinquenta e nove janelas normais. A One-Class SVM alarmou em todas. Na validação, ambos tinham apenas três vírgula trinta e nove por cento de falsos positivos. Isso sugere deslocamento da normalidade com a carga. A área sob a curva da One-Class SVM foi um, porque ela ordenou os escores corretamente, mas o limiar calibrado em outra carga falhou. Por isso não devemos apresentar apenas a taxa de detecção.

## Slide 7 — 3:45 a 4:20

Há limitações importantes. Temos só uma gravação normal no teste e janelas consecutivas não são repetições independentes. O mesmo rolamento pode aparecer em cargas diferentes. Os defeitos são induzidos, e a aquisição do normal pode ter características diferentes. A sensibilidade mostrou que a interpretação da taxa do baseline muda os falsos positivos. Antes de uma aplicação prática, precisamos confirmar essa taxa, coletar mais normalidade por carga, reservar rolamentos inteiros e avaliar falhas naturais.

## Slide 8 — 4:20 a 4:40

Concluímos que a SVM foi a melhor alternativa no protocolo avaliado, enquanto os detectores precisam de calibração representativa da carga. O material inclui código, dados e resultados rastreáveis. Declaramos o uso de ChatGPT e Codex na preparação e execução, com revisão e responsabilidade final do grupo.
