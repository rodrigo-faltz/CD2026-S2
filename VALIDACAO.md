# Registro de validação

## Versão final (11 nov. 2026)

Execução em Windows 10, Python 3.12.9, versões de `requirements.txt`, com os dados de `dados/raw/`.

| Verificação | Resultado |
|---|---|
| Notebook executado do zero com `jupyter nbconvert --execute` (pasta `resultados/` apagada antes) | Sem erros, 104 s |
| Números mantidos comparados com a versão anterior (detecção, diagnóstico por carga e por diâmetro, comparação por gravação, tabela resumo e as 5 matrizes de confusão) | **Idênticos** (tolerância 1e-9) |
| Seleção de hiperparâmetros com `GridSearchCV(cv=LeaveOneGroupOut())` comparada com a validação cruzada manual anterior | Mesmas predições nas 14 combinações de dobra e modelo |
| Schema do notebook (`nbformat.validate`) | Válido; nenhuma saída de erro |
| APIs que mudam entre versões do Colab (`include_groups`, `tick_labels`) | Não usadas |

O download pela fonte oficial não foi repetido nesta versão: o código de download e conferência de SHA-256 não mudou.
A execução no serviço Google Colab ainda deve ser feita por um integrante.

## Versão anterior

Execução em 6 nov. 2026, Windows 11, Python 3.12, versões de `requirements.txt`.

## Reprodutibilidade

| Verificação | Resultado |
|---|---|
| Notebook executado num diretório vazio com `jupyter nbconvert --execute` (comando do README) | Sem erros, 280 s |
| Download dos 40 arquivos da fonte oficial do CWRU | 40/40 com SHA-256 igual ao esperado |
| Mesmo notebook executado no repositório, com os dados de `dados/raw/` | Sem erros |
| Comparação das duas execuções | 27 arquivos de resultados (CSV, JSON, MD) e o manifesto **idênticos** |
| Schema do notebook (`nbformat.validate`) | Válido |

## Integridade e protocolo

- Os 40 arquivos têm o SHA-256 fixado no notebook; a execução para se algum divergir. Não há geração de dados
  substitutos.
- O servidor do CWRU às vezes interrompe a transferência de arquivos grandes (observado nos arquivos 204, 217, 239 e
  240). O notebook tenta até 5 vezes por fonte, com espera crescente, e só aceita o arquivo se o hash conferir.
- Toda divisão de dados é feita por gravação (carga ou diâmetro); janelas de uma mesma gravação nunca aparecem em treino
  e teste ao mesmo tempo.
- Hiperparâmetros são escolhidos por validação cruzada interna dentro de cada dobra; o teste externo é usado uma vez.
- Limiares de detecção são calibrados apenas com dados normais de treino.

## Referências

Os 24 DOIs da lista de referências foram consultados no Crossref (título, autores, periódico, volume, páginas e ano). As
páginas do CWRU foram acessadas diretamente; a tabela de arquivos de 48 kHz e a geometria do rolamento conferem com o
código.

## Não verificado

- A execução no serviço Google Colab não foi feita nesta validação. O notebook usa apenas bibliotecas presentes no Colab
  e não depende de arquivos locais; para usar exatamente as versões de referência, há a opção `PINAR_VERSOES = True`.
- Com versões de bibliotecas diferentes das de referência, os resultados podem variar ligeiramente.
