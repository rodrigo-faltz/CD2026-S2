# Baixar o projeto CWRU

- **[Baixar pacote completo — documentos + dados reais](https://github.com/rodrigo-faltz/CD2026-S2/raw/refs/heads/main/Projeto_CWRU_Completo.zip)** (aproximadamente 48 MB).
- **[Baixar pacote leve — documentos, sem os MAT](https://github.com/rodrigo-faltz/CD2026-S2/raw/refs/heads/main/Projeto_CWRU_Sem_Dados.zip)**. O notebook baixa os dados quando for executado.
- **[Abrir a análise no Google Colab](https://colab.research.google.com/github/rodrigo-faltz/CD2026-S2/blob/main/CWRU_Projeto.ipynb)**.

Depois do download, extraia o ZIP. O pacote contém relatório Word/Markdown/HTML, slides PowerPoint/PDF, notebook executado, código, referências, métricas e roteiro de apresentação. Os mesmos arquivos estão disponíveis individualmente neste repositório.

---

# ECM514 — CWRU: detecção e diagnóstico de falhas

Projeto executado sobre 40 gravações reais do CWRU. A SVM RBF apresentou acurácia de 99,15% no teste de carga reservada. O detector Isolation Forest apresentou TPR de 100% e FPR de 23,73%; os falsos alarmes são uma limitação central. Leia a discussão e a premissa de taxa de aquisição no relatório antes de interpretar os resultados.

## Sumário de entregas

- [Notebook executado e autocontido](CWRU_Projeto.ipynb)
- [Relatório técnico](RELATORIO.md) e [versão Word](RELATORIO.docx)
- [Slides editáveis](APRESENTACAO.pptx) e [slides em PDF](APRESENTACAO.pdf)
- [Roteiro de 4min40s](ROTEIRO_VIDEO.md)
- [Dados e rastreabilidade](dados/manifesto.csv); arquivos MAT em `dados/raw/` no pacote completo
- [Tabela padronizada de resultados](resultados/tabela_resumo.csv)
- [Métricas detalhadas](resultados/metricas.json), matrizes PNG/CSV e predições em `resultados/`
- [Referências, ao menos duas por técnica](REFERENCIAS.md)
- [Código Python](analise.py), [dependências](requirements.txt) e [validação da entrega](VALIDACAO.md)
- **Vídeo no YouTube:** pendente de gravação e publicação pelo grupo; inserir aqui o link real.
- **Repositório GitHub:** https://github.com/rodrigo-faltz/CD2026-S2
- **Integrantes:** preencher nomes e RAs de até seis alunos.

## Executar no Google Colab

1. Abra https://colab.research.google.com/ e escolha **Arquivo → Fazer upload de notebook**.
2. Envie `CWRU_Projeto.ipynb`. Não é necessário enviar o ZIP, montar Drive ou obter token do Kaggle.
3. Use ambiente Python com CPU e execute todas as células, incluindo a instalação. Se o Colab solicitar reinício após instalar, reinicie e execute novamente.
4. O notebook baixa cerca de 134 MiB da fonte oficial (40 arquivos) e verifica SHA-256. Não há substituição por dados artificiais se a rede falhar.
5. As saídas surgem em `resultados/` e os MAT em `dados/raw/` no diretório da sessão. A última célula permite baixar resultados compactados no Colab.
6. O relatório já está incorporado ao notebook. A pasta do ZIP adicional permite abrir figuras externas em Markdown/Word.

O notebook foi testado por execução integral em Python na sessão, com versões fixadas; a execução no serviço Colab ainda deve ser conferida pelo grupo. Não há necessidade de GPU. O tempo depende da rede e da máquina.

## Executar localmente

Python 3.12 é a versão de referência. No terminal, a partir da pasta deste README:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python analise.py
```

No Windows, ative com `.venv\Scripts\activate`. Os arquivos baixados são reutilizados, mas seus hashes são conferidos. Em caso de falha de integridade, não ignore a checagem: confira a origem e o manifesto. A pasta de resultados será atualizada pela execução.

Para reproduzir a sensibilidade de taxa, depois da análise principal:

```bash
python sensibilidade.py
```

Esse cenário escreve em `experimento_taxa_12k/resultados/`, sem substituir os resultados principais.

## Protocolo e resultados

Treino: cargas 0–1 HP; validação: 2 HP; teste: 3 HP. Nenhuma gravação atravessa partições. O protocolo conserva possíveis rolamentos físicos compartilhados entre cargas, de modo que a conclusão se restringe à mudança de carga no domínio selecionado.

| Dataset           | Técnica         | Tipo de falha identificada           |   Taxa de detecção (TPR) |   Falso positivo (FPR) | Acurácia por classe (recall)                                                 |
|:------------------|:----------------|:-------------------------------------|-------------------------:|-----------------------:|:-----------------------------------------------------------------------------|
| CWRU — recorte DE | IsolationForest | não se aplica                        |                   1.0000 |                 0.2373 | não se aplica                                                                |
| CWRU — recorte DE | OneClassSVM     | não se aplica                        |                   1.0000 |                 1.0000 | não se aplica                                                                |
| CWRU — recorte DE | RandomForest    | Pista interna; Esfera; Pista externa |                   1.0000 |                 0.0000 | Normal: 1.0000; Pista interna: 0.5000; Esfera: 1.0000; Pista externa: 0.9887 |
| CWRU — recorte DE | SVM_RBF         | Pista interna; Esfera; Pista externa |                   1.0000 |                 0.0000 | Normal: 1.0000; Pista interna: 1.0000; Esfera: 0.9718; Pista externa: 1.0000 |
| CWRU — recorte DE | Baseline_dummy  | Pista interna; Esfera; Pista externa |                   1.0000 |                 1.0000 | Normal: 0.0000; Pista interna: 0.0000; Esfera: 1.0000; Pista externa: 0.0000 |

Valores em proporções. A coluna por classe representa recall. Todas as quatro classes do recorte estão nas matrizes completas. A SVM foi selecionada por macro-F1 na validação, antes de examinar o teste. Não foi ajustado um novo limiar no teste.

**Premissa a conferir:** baseline 97–100 interpretado a 48 kHz e reduzido a 12 kHz com anti-aliasing; falhas DE da coleção 12 kHz. Os MAT não informam explicitamente a taxa. Uma sensibilidade alternativa de 12 kHz, com números diferentes de janelas, consta no relatório. Não tratar as métricas como independentes dessa premissa.

## Dados e publicação

Origem: https://engineering.case.edu/bearingdatacenter/welcome. Os arquivos MAT do pacote completo são cópias dos downloads oficiais, sem geração de dados. O manifesto lista os URLs e hashes. Os defeitos foram induzidos por EDM, mas a vibração foi medida em bancada. O recorte cobre quatro famílias de condição, três diâmetros e pista externa apenas a 6 horas.

Cada MAT é menor que 100 MB. Pode-se publicar os 40 arquivos individualmente em `dados/raw/` no GitHub; **não enviar o ZIP completo como um único arquivo ao repositório**, pois pode ultrapassar 100 MB. Alternativamente disponibilizar os MAT em Drive público e inserir o link. O download automático oficial também é implementado para reprodutibilidade.

Antes de enviar: preencher autores; conferir premissa de aquisição e referências; executar no Colab; revisar relatório e slides; conferir os arquivos publicados no GitHub; gravar vídeo de no máximo cinco minutos; inserir URL real do YouTube. O prazo de cadastro indicado no enunciado é 17/09/2026; o PDF não informa uma data final de entrega.

## Uso de IA

ChatGPT/Codex auxiliou na interpretação do enunciado, elaboração e execução do código e preparação do texto e slides. Os resultados foram calculados em dados reais. O grupo precisa revisar e validar o material e declarar esse uso na versão final, conforme solicitado pelo professor.
