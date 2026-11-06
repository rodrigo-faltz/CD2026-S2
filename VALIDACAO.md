# Validação da entrega

Execução realizada em 06/11/2026.

- 40 arquivos MAT reais baixados da fonte oficial, com canais e SHA-256 verificados.
- 2.331 janelas: 1.150 de treino, 590 de validação e 591 de teste.
- 17 atributos numéricos finitos; nenhum ID de gravação atravessa partições.
- Código Python executado integralmente e notebook executado novamente em diretório limpo, sem arquivos auxiliares; oito células de código executadas, zero erros.
- As métricas e o manifesto da reexecução independente do notebook foram idênticos aos do script.
- Matrizes de diagnóstico 4×4 conferidas: 591 exemplos cada e acurácias consistentes com metricas.json.
- Cenário de sensibilidade à taxa do baseline executado separadamente e documentado.
- Notebook validado contra o schema nbformat; PPTX reaberto com oito slides; DOCX reaberto; slides em PDF renderizados e inspecionados visualmente.
- Integridade das entradas e ausência de vazamento entre gravações verificadas por asserções executáveis.

## Limites desta validação

O notebook foi executado em Python 3.12 nesta sessão, não no serviço Google Colab. A compatibilidade proposta usa instalação por pip e somente bibliotecas comuns, mas o grupo deve confirmar uma execução no Colab. A premissa de taxa de aquisição do baseline está explicitada no relatório e depende de conferência documental; a sensibilidade não substitui essa confirmação. Não se verificou generalização para rolamentos físicos inéditos ou falhas naturais. A execução não realizou cadastro acadêmico nem publicação de vídeo no YouTube. O material está sendo publicado no repositório indicado no README.
