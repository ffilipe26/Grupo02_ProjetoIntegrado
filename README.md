# PROJETO INTEGRADO – COMPARTILHAFATEC (GRUPO 2)

**FATEC FERRAZ DE VASCONCELOS | CENTRO PAULA SOUZA**

Curso: Tecnologia em Análise e Desenvolvimento de Sistemas
Projeto Interdisciplinar – Inglês, Redes de Computadores e Sistemas Distribuídos

---

## IDENTIFICAÇÃO DO GRUPO

| Grupo | Tema |
| --- | --- |
| Grupo 2 | Compartilhamento distribuído de arquivos |

**Título da solução:** CompartilhaFATEC – Protótipo de Compartilhamento de Arquivos em Rede

| Integrante | Nome completo | RA | Função (líder, gestor ou integrante) |
| --- | --- | --- | --- |
| 1 | Alecsander Torres | 2920482421030 | Integrante |
| 2 | Filipe Acierno | 2920482421034 | Líder |
| 3 | Guilherme Souza | 2920482421020 | Integrante |
| 4 | Michael Coutinho | 2920482421031 | Gestor |
| 5 | Yago Nunes da Silva | 2920482421021 | Integrante |
| 6 | Giovanni Pereira | RA_GIOVANNI | Integrante |

---

## DESCRIÇÃO DA SOLUÇÃO

O CompartilhaFATEC é um serviço de compartilhamento de arquivos em rede local. Um computador executa o servidor de arquivos, escrito em Python, e os usuários acessam o sistema pelo navegador, no computador ou no celular, para enviar arquivos, ver a lista dos arquivos disponíveis e baixá-los.

**Implementado:** servidor de arquivos (`servidor.py`), interface web, envio (upload), listagem e download, validação do nome do arquivo, tratamento de nomes repetidos e de envios interrompidos, limite de 50 MB por arquivo, registro das requisições (log) e armazenamento em pasta local.

**Simulado:** nenhum componente do sistema é simulado; a topologia é a rede local real usada nos testes. O acesso a partir de outro dispositivo (celular) foi comprovado no teste T03 da Etapa 3.

---

## ENTREGAS

### Etapa 3 – Protótipo, testes e relatório

| Arquivo ou pasta | Conteúdo |
| --- | --- |
| [Etapa3/Grupo02_Relatorio.pdf](Etapa3/Grupo02_Relatorio.pdf) | Relatório técnico em português |
| [Etapa3/Grupo02_Testes.pdf](Etapa3/Grupo02_Testes.pdf) | Plano e resultados dos testes (T01 a T07), com métricas e análise |
| [Etapa3/evidencias/](Etapa3/evidencias/) | Capturas de tela dos testes, identificadas pelo número do teste |
| [Etapa3/codigo/](Etapa3/codigo/) | Código final do protótipo, instruções de execução e descrição da implementação |

**Resumo dos testes:** fluxo completo de envio e download (T01 e T02), acesso pelo celular na mesma rede (T03), tempo médio de resposta e disponibilidade de 100% (T04), falha do servidor com disponibilidade de 0% (T05), recuperação sem perda de arquivos (T06) e bloqueio de acesso fora da pasta compartilhada (T07).

### Etapa 2 – Diagramas técnicos

| Arquivo ou pasta | Conteúdo |
| --- | --- |
| [Etapa2/Grupo02_Etapa2_DiagramasTecnicos.pdf](Etapa2/Grupo02_Etapa2_DiagramasTecnicos.pdf) | Modelo de entrega preenchido (versão para leitura) |
| [Etapa2/Grupo02_Etapa2_DiagramasTecnicos.docx](Etapa2/Grupo02_Etapa2_DiagramasTecnicos.docx) | Modelo de entrega preenchido (versão editável) |
| [Etapa2/diagramas/](Etapa2/diagramas/) | Diagramas de rede e de arquitetura (.drawio e .png) |
| [Etapa2/simulacao/](Etapa2/simulacao/) | Versão do código usada na Etapa 2 |
| [Etapa2/evidencias/](Etapa2/evidencias/) | Capturas de tela do desenvolvimento (E01 a E08) |

---

## COMO EXECUTAR

1. Instale o Python 3 (python.org), marcando "Add python.exe to PATH".
2. Abra o terminal na pasta `Etapa3/codigo`.
3. Execute `python servidor.py`.
4. Abra `http://localhost:8000` no navegador. Para outro dispositivo da mesma rede, use o endereço exibido no terminal.

Passo a passo completo em [Etapa3/codigo/COMO_RODAR.md](Etapa3/codigo/COMO_RODAR.md).

---

## FERRAMENTAS UTILIZADAS

| Ferramenta | Uso no projeto |
| --- | --- |
| Python 3.14 (http.server) | Servidor de arquivos do protótipo |
| HTML, CSS e JavaScript | Interface web usada no navegador |
| Navegador web | Cliente do sistema no computador e no celular |
| curl e ping | Medição de tempo de resposta, disponibilidade e latência |
| Draw.io | Diagramas de rede e de arquitetura |
| GitHub | Repositório do código e da documentação |

---

## USO DE INTELIGÊNCIA ARTIFICIAL

| Informação solicitada | Resposta do grupo |
| --- | --- |
| Ferramenta utilizada e data de uso | Claude (Anthropic), utilizado entre 28/10/2026 e 18/11/2026 |
| Para que a ferramenta foi utilizada | Apoio no desenvolvimento do código do protótipo, na organização do repositório e na estruturação e formatação da documentação técnica, a partir do sistema desenvolvido e testado pelo grupo |
| O que o grupo revisou, corrigiu ou alterou | O grupo executou e testou cada versão do código, realizou os testes e registrou as evidências, conferiu se os textos correspondem ao funcionamento real do sistema, definiu o escopo e as decisões do projeto e elaborou os diagramas |
