# PROJETO INTEGRADO – ETAPA 2: DIAGRAMAS TÉCNICOS

**FATEC FERRAZ DE VASCONCELOS | CENTRO PAULA SOUZA**

Curso: Tecnologia em Análise e Desenvolvimento de Sistemas
Projeto Interdisciplinar – Inglês, Redes de Computadores e Sistemas Distribuídos
Entrega: 04 e 05/11/2026

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

---

## DESCRIÇÃO DA SOLUÇÃO

O CompartilhaFATEC é um serviço de compartilhamento de arquivos em rede local. Um computador executa o servidor de arquivos, escrito em Python, e os usuários acessam o sistema pelo navegador para enviar arquivos, ver a lista dos arquivos disponíveis e baixá-los.

**Implementado:** servidor de arquivos (`servidor.py`), interface web, envio (upload), listagem e download, validação do nome do arquivo, tratamento de nomes repetidos, limite de 50 MB por arquivo, registro das requisições (log) e armazenamento em pasta local.

**Simulado:** nenhum componente do sistema é simulado; a topologia é a rede local real usada nos testes. O acesso a partir de outro dispositivo (celular) foi bloqueado pelo firewall do Windows no computador de desenvolvimento e será repetido em outro equipamento.

---

## ARQUIVOS DA ETAPA 2

| Arquivo ou pasta | Conteúdo |
| --- | --- |
| [Etapa2/Grupo02_Etapa2_DiagramasTecnicos.pdf](Etapa2/Grupo02_Etapa2_DiagramasTecnicos.pdf) | Modelo de entrega preenchido (versão para leitura) |
| [Etapa2/Grupo02_Etapa2_DiagramasTecnicos.docx](Etapa2/Grupo02_Etapa2_DiagramasTecnicos.docx) | Modelo de entrega preenchido (versão editável) |
| [Etapa2/diagramas/](Etapa2/diagramas/) | Arquivos-fonte dos diagramas (.drawio e .png) |
| [Etapa2/simulacao/](Etapa2/simulacao/) | Código do protótipo (`servidor.py`) e instruções de execução (`COMO_RODAR.md`) |
| [Etapa2/evidencias/](Etapa2/evidencias/) | Capturas de tela dos testes (E01 a E08) |

---

## FERRAMENTAS UTILIZADAS

| Ferramenta | Uso no projeto |
| --- | --- |
| Python 3.14 (http.server) | Servidor de arquivos do protótipo |
| HTML e JavaScript | Interface web usada no navegador |
| Navegador web | Cliente do sistema (envio, listagem e download) |
| Draw.io | Diagramas de rede e de arquitetura |
| GitHub | Repositório do código e da documentação |

---

## USO DE INTELIGÊNCIA ARTIFICIAL

| Informação solicitada | Resposta do grupo |
| --- | --- |
| Ferramenta utilizada e data de uso | Claude (Anthropic), utilizado entre 28/10/2026 e 04/11/2026 |
| Para que a ferramenta foi utilizada | Apoio no desenvolvimento do código do protótipo, na organização do repositório e na estruturação e formatação da documentação técnica, a partir do sistema desenvolvido e testado pelo grupo |
| O que o grupo revisou, corrigiu ou alterou | O grupo executou e testou cada versão do código, conferiu se os textos correspondem ao funcionamento real do sistema, definiu o escopo e as decisões do projeto e elaborou os diagramas |
