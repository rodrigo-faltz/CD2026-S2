# Detecção e diagnóstico de falhas em rolamentos — CWRU 48 kHz

**ECM514 — Ciência de Dados · Projeto Desafio do 2º semestre de 2026**

**Integrantes:**
- Amanda Carolina Ambrizzi Ramin 22.00721-0
- André Felipe Silva Xavier 22.01339-3
- Otto Camargo Kuchkarian 22.00571-4
- Rafael Assanti 22.01464-0
- Rodrigo Fernandes Faltz 21.01660-7

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rodrigo-faltz/CD2026-S2/blob/main/CWRU_Projeto.ipynb)

Detectamos e diagnosticamos defeitos de rolamento (pista interna, esfera e pista externa) em 40 gravações reais de
vibração do *Bearing Data Center* da Case Western Reserve University, comparando três detectores de anomalia, dois
classificadores e uma regra física baseada em análise de envelope. Os modelos são avaliados em **cargas** e em
**diâmetros de defeito** que não viram no treino.

O notebook segue o roteiro das aulas: dados → atributos (tabela X, y) → separação treino/teste → seleção de modelos com
`GridSearchCV` → `classification_report`, matriz de confusão e curva ROC. Cada seção começa com a pergunta que responde
e termina com a leitura do resultado; as células só de infraestrutura (download, figuras) aparecem recolhidas no Colab.

## Sumário de entregas

| Entrega | Arquivo |
|---|---|
| Notebook executável no Colab (código, análises e figuras) | [`CWRU_Projeto.ipynb`](CWRU_Projeto.ipynb) |
| Relatório técnico | [`RELATORIO.md`](RELATORIO.md) · [`RELATORIO.docx`](RELATORIO.docx) |
| Dados empregados (40 arquivos MAT originais) | [`dados/raw/`](dados/raw/) · [`dados/manifesto.csv`](dados/manifesto.csv) |
| Tabela resumo de resultados | [abaixo](#tabela-resumo-de-resultados) · [`resultados/tabela_resumo.csv`](resultados/tabela_resumo.csv) |
| Matrizes de confusão completas | [Anexo A do relatório](RELATORIO.md#anexo-a--matrizes-de-confusão-completas) · `resultados/matriz_*.csv` |
| Slides da apresentação (usados no vídeo) | [`APRESENTACAO.html`](APRESENTACAO.html) — 15 slides narrados + 4 de apêndice, abra no navegador; versão em [PowerPoint](APRESENTACAO.pptx) e [PDF](APRESENTACAO.pdf) |
| Vídeo da apresentação (até 5 min) | **YouTube:** _link do vídeo_ |
| Roteiro com as falas dos 5 integrantes | [`ROTEIRO_APRESENTACAO.md`](ROTEIRO_APRESENTACAO.md) |
| Referências bibliográficas | [`REFERENCIAS.md`](REFERENCIAS.md) |
| Declaração de uso de IA | [Seção 9 do relatório](RELATORIO.md#9-declaração-de-uso-de-inteligência-artificial) |
| Registro de validação da execução | [`VALIDACAO.md`](VALIDACAO.md) |

## Tabela resumo de resultados

Validação cruzada deixando uma **carga** de fora (4 dobras), conjunto de atributos adimensionais + envelope. Métricas por
janela somando as dobras, exceto a regra de envelope (por gravação). N = normal, PI = pista interna, E = esfera,
PE = pista externa. "Tipo de falha identificada" lista as classes com recall ≥ 0,5; "acurácia por classe" é o recall.
A tabela é copiada de [`resultados/tabela_resumo.md`](resultados/tabela_resumo.md), gerada pelo notebook.

| Dataset        | Técnica                                                | Tipo de falha identificada           |   Taxa de detecção (TPR) |   Falso positivo (FPR) | Acurácia por classe (se houver diagnóstico)   |
|:---------------|:-------------------------------------------------------|:-------------------------------------|-------------------------:|-----------------------:|:----------------------------------------------|
| CWRU 48 kHz DE | Curtose do envelope (indicador) — detecção, por janela | não se aplica                        |                   0.6790 |                 0.0297 | não se aplica                                 |
| CWRU 48 kHz DE | Mahalanobis — detecção, por janela                     | não se aplica                        |                   0.7282 |                 0.1386 | não se aplica                                 |
| CWRU 48 kHz DE | Isolation Forest — detecção, por janela                | não se aplica                        |                   0.8076 |                 0.0891 | não se aplica                                 |
| CWRU 48 kHz DE | Random Forest — diagnóstico, por janela                | Pista interna; Esfera; Pista externa |                   0.9989 |                 0.0000 | N: 1.00; PI: 0.95; E: 0.99; PE: 0.95          |
| CWRU 48 kHz DE | SVM RBF — diagnóstico, por janela                      | Pista interna; Esfera; Pista externa |                   1.0000 |                 0.0495 | N: 0.95; PI: 0.97; E: 0.92; PE: 0.90          |
| CWRU 48 kHz DE | Regra de envelope — diagnóstico, por gravação          | Pista interna; Pista externa         |                   0.5833 |                 0.2500 | N: 0.75; PI: 0.83; E: 0.00; PE: 0.75          |

**Principais conclusões**

- **Detecção:** os escores de Mahalanobis e do Isolation Forest separam normal e falha quase perfeitamente (ROC-AUC de
  0,975 a 1,000), mas o limiar não se
  transfere entre cargas com só quatro gravações normais. Com uma referência normal em cada carga, a distância de
  Mahalanobis detecta 100% das falhas sem falsos alarmes.
- **Diagnóstico com carga nova:** Random Forest acerta 96,8% das janelas e 92,5% das gravações. O pior caso é a carga de
  0 HP (macro-F1 de 0,83 contra 0,99 nas outras).
- **Diagnóstico com diâmetro de defeito novo:** os classificadores com atributos estatísticos caem abaixo do acaso
  (macro-F1 de 0,07 a 0,12). A regra de envelope, baseada na física do rolamento, acerta 69% das gravações. A acurácia
  alta com carga nova vem, em boa parte, do reconhecimento de rolamentos já vistos.

## Como executar

### No Google Colab (recomendado)

1. Clique no botão **Abrir no Colab** acima.
2. Menu **Ambiente de execução → Executar tudo**.

Não é preciso GPU, conta do Kaggle nem upload de arquivos. O notebook baixa os 40 arquivos (≈ 275 MB) da fonte oficial
do CWRU, confere o SHA-256 de cada um e gera tudo em `resultados/`. A execução leva cerca de 3 a 5 minutos. O Colab já
traz as bibliotecas necessárias.

**Sobre os números.** Os resultados do relatório e de `resultados/` foram gerados com as versões de `requirements.txt`
(scikit-learn 1.9.1). O Colab usa outras versões (no teste de 11/11/2026, scikit-learn 1.6.1), e com elas **só os
números da Random Forest mudam um pouco**: por exemplo, a macro-F1 com 0 HP no teste vai de 0,83 para 0,85, e a acurácia
da Random Forest com 0 HP na tabela de vazamento vai de 85,5% para 79,4%. Detecção, SVM e regra de envelope saem
idênticos, e as conclusões não mudam. Para reproduzir **exatamente** os números do relatório no Colab, rode antes esta
célula, reinicie a sessão quando o Colab pedir e depois use *Executar tudo*:

```
%pip install -q numpy==2.5.4 scipy==1.18.1 pandas==3.1.1 scikit-learn==1.9.1 matplotlib==3.11.2
```

### Localmente

Python 3.12 é a versão de referência.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace CWRU_Projeto.ipynb
```

Com o repositório clonado, os dados de `dados/raw/` são usados diretamente (após a conferência dos hashes).

## Dados

- **Fonte:** CWRU Bearing Data Center — [normais](https://engineering.case.edu/bearingdatacenter/normal-baseline-data) e
  [falhas no drive end a 48 kHz](https://engineering.case.edu/bearingdatacenter/48k-drive-end-bearing-fault-data).
- **Recorte:** 4 gravações normais e 36 com falha (pista interna, esfera e pista externa a 6h × diâmetros de 0,007",
  0,014" e 0,021" × cargas de 0 a 3 HP), canal do drive end, todas a 48 kHz. A justificativa está na seção 2.2 do
  relatório.
- **Integridade:** [`dados/manifesto.csv`](dados/manifesto.csv) lista URL oficial, SHA-256, canal, amostras e rotação de
  cada arquivo.
- São medições reais de bancada, com defeitos induzidos por eletroerosão. Nenhum dado sintético foi usado.

## Estrutura do repositório

```
CWRU_Projeto.ipynb    notebook (única fonte de código)
RELATORIO.md/.docx    relatório técnico
APRESENTACAO.html/.pptx/.pdf, ROTEIRO_APRESENTACAO.md
REFERENCIAS.md, VALIDACAO.md, requirements.txt
dados/raw/            40 arquivos .mat originais
dados/manifesto.csv   rastreabilidade dos dados
resultados/           métricas, predições, matrizes e figuras geradas pelo notebook
```
