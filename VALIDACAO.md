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

- O download pela fonte oficial não foi repetido nesta versão: o código de download e de conferência do SHA-256 não
  mudou.
- A execução no serviço Google Colab ainda deve ser feita por um integrante. O notebook usa apenas bibliotecas presentes
  no Colab e não depende de arquivos locais; as versões da execução de referência estão em `requirements.txt`.
- Com versões de bibliotecas diferentes das de referência, os resultados podem variar ligeiramente.

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
