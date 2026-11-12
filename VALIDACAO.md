# Registro de validação

## Versão final (11 nov. 2026)

Execução em Windows 10, Python 3.12.9, versões de `requirements.txt`, com os dados de `dados/raw/`.

### Reprodutibilidade

| Verificação | Resultado |
|---|---|
| Notebook executado do zero com `jupyter nbconvert --execute` (pasta `resultados/` apagada antes) | Sem erros, 105 s |
| Números mantidos comparados com a versão anterior (detecção, diagnóstico por carga e por diâmetro, comparação por gravação, tabela resumo e as 5 matrizes de confusão) | **Idênticos** (tolerância 1e-9) |
| Seleção de hiperparâmetros com `GridSearchCV(cv=LeaveOneGroupOut())` comparada com a validação cruzada manual anterior | Mesmas predições nas 14 combinações de dobra e modelo |
| Schema do notebook (`nbformat.validate`) | Válido; nenhuma saída de erro |
| APIs que mudam entre versões do Colab (`include_groups`, `tick_labels`) | Não usadas |
| Clone limpo do GitHub (`main`) executado do zero | Sem erros; os 27 arquivos de resultado (CSV e tabela resumo) **idênticos** aos publicados |
| Números citados no `RELATORIO.md` recalculados a partir de `resultados/` | 65 de 65 conferem |

### Execução no Google Colab (11 nov. 2026)

Notebook aberto pelo botão do README e executado com *Executar tudo*, numa sessão nova do Colab, com as bibliotecas do
próprio Colab: numpy 2.4.6, scipy 1.16.3, pandas 2.2.3, scikit-learn 1.6.1 e matplotlib 3.10.0.

| Verificação | Resultado |
|---|---|
| Execução completa | Sem erros, 22 células |
| Download dos 40 arquivos da fonte oficial do CWRU | 40/40 com SHA-256 igual ao esperado |
| Saídas comparadas com a execução de referência | 15 de 22 células idênticas; as diferenças estão só na origem dos dados, nas versões impressas e nos resultados da Random Forest |
| Detecção (3 detectores, 2 cenários), SVM e regra de envelope | **Idênticos** |
| Random Forest | Variações pequenas, sem mudar nenhuma conclusão (tabela abaixo) |

| Resultado da Random Forest | Referência (scikit-learn 1.9.1) | Colab (scikit-learn 1.6.1) |
|---|---|---|
| Vazamento: sorteio de janelas | 99,3% | 99,7% |
| Vazamento: carga nova (0 / 1 / 2 / 3 HP) | 85,5 / 100 / 99,7 / 99,3% | 79,4 / 99,6 / 99,3 / 99,7% |
| Vazamento: diâmetro novo (0,014" / 0,021") | 32,8 / 5,3% | 33,8 / 2,6% |
| Diagnóstico com carga nova, macro-F1 com 0 HP no teste | 0,83 | 0,85 |
| Tabela resumo, recall de pista interna | 0,95 | 0,96 |
| Diâmetro novo, só envelope, acerto por gravação | 55,6% | 52,8% |
| Acerto por gravação: carga nova / diâmetro novo (conjunto B) | 92,5% / 22,2% | 92,5% / 22,2% |

A semente é a mesma (`SEED = 42`), mas o sorteio interno das árvores mudou entre as versões do scikit-learn, por isso só
a Random Forest varia. Para reproduzir exatamente os números do relatório no Colab, instale as versões de
`requirements.txt` antes de executar (instrução no README).

### Integridade e protocolo

- Os 40 arquivos têm o SHA-256 fixado no notebook; a execução para se algum divergir. Não há geração de dados
  substitutos.
- O servidor do CWRU às vezes interrompe a transferência de arquivos grandes (observado nos arquivos 204, 217, 239 e
  240). O notebook tenta até 5 vezes por fonte, com espera crescente, e só aceita o arquivo se o hash conferir.
- Toda divisão de dados é feita por gravação (carga ou diâmetro), exceto no cenário 6.1, em que cada gravação normal é
  dividida em terços no tempo — por isso ele é otimista quanto ao FPR. Fora desse cenário, janelas de uma mesma gravação
  nunca aparecem em treino e teste ao mesmo tempo.
- Hiperparâmetros são escolhidos por validação cruzada interna dentro de cada dobra; o teste externo é usado uma vez.
- Limiares de detecção são calibrados apenas com dados normais de treino (ou de validação, no cenário 6.1).

### Referências

Os 20 DOIs da lista de referências (itens 6 a 25) foram consultados no Crossref (título, autores, periódico, volume,
páginas e ano). As páginas do CWRU (itens 1 a 5) foram acessadas diretamente; a tabela de arquivos de 48 kHz e a
geometria do rolamento conferem com o código.

### Não verificado

- Só foram testadas duas combinações de versões: as de `requirements.txt` (referência) e as do Colab em 11/11/2026. Com
  outras versões, os resultados da Random Forest podem variar ligeiramente, como na tabela acima.

## Versão anterior

Execução em 6 nov. 2026, Windows 11, Python 3.12, versões de `requirements.txt`.

### Reprodutibilidade (versão anterior)

| Verificação | Resultado |
|---|---|
| Notebook executado num diretório vazio com `jupyter nbconvert --execute` (comando do README) | Sem erros, 280 s |
| Download dos 40 arquivos da fonte oficial do CWRU | 40/40 com SHA-256 igual ao esperado |
| Mesmo notebook executado no repositório, com os dados de `dados/raw/` | Sem erros |
| Comparação das duas execuções | 27 arquivos de resultados (CSV, JSON, MD) e o manifesto **idênticos** |
| Schema do notebook (`nbformat.validate`) | Válido |
