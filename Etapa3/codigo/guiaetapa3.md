# Guia completo – Etapa 3 (prazo: 17/11 às 23:59)

O que precisa ser entregue: **o sistema funcionando (já pronto), os testes e o relatório**.
Este guia explica tudo, passo a passo, para ninguém ficar perdido.

- **Parte A – Protótipo/Sistema:** ✅ já está pronto, na pasta `Etapa3/codigo` do repositório.
- **Parte B – Testes:** fazer os testes, tirar os prints e montar o arquivo `Grupo02_Testes.pdf`.
- **Parte C – Relatório:** escrever o `Grupo02_Relatorio.pdf`, seguindo o exemplo da professora.

---

## 0. Divisão sugerida

| Quem | Faz o quê |
|---|---|
| Pessoa 1 | Parte B: testes, prints e `Grupo02_Testes.pdf` (passos 1, 2 e 3) |
| Pessoa 2 | Parte C: seções 1, 2, 3, 4 e 8 do relatório (passo 4) |
| Pessoa 3 | Parte C: seções 5, 6 e 7 do relatório, juntar tudo em PDF e entregar (passos 4 e 5) |

Todos precisam ler o relatório no final: na apresentação a professora pode perguntar qualquer coisa para qualquer um.

---

## 1. Preparar o computador (Pessoa 1)

1. Confira se tem Python: aperte **Win + R**, digite `cmd`, dê Enter e digite `python --version`.
   - Se aparecer `Python 3...`, está certo.
   - Se não, baixe em **python.org**. Na primeira tela do instalador, marque **"Add python.exe to PATH"** antes de clicar em Install Now.
2. Acesse o repositório **Grupo02_ProjetoIntegrado** no GitHub, clique no botão verde **Code** e depois em **Download ZIP**.
3. Extraia o ZIP e abra a pasta **Etapa3 › codigo**.
4. Clique na barra de endereço da pasta (onde aparece o caminho), apague tudo, digite `cmd` e dê Enter. O terminal abre já na pasta certa.
5. Digite `python servidor.py` e dê Enter.
6. Se o Windows perguntar sobre o Firewall, clique em **Permitir acesso**.
7. No navegador, abra `http://localhost:8000`. Tem que aparecer a página do CompartilhaFATEC.

Para parar o servidor: clique no terminal e aperte **Ctrl + C**.

**Dica para os prints:** use **Win + Shift + S** e salve cada print com o nome do teste (ex.: `T01-a.png`). Guarde todos numa pasta chamada `evidencias`.

---

## 2. Fazer os testes (Pessoa 1)

Faça os testes **na ordem**. Para cada um, anote o que aconteceu de verdade (vai na coluna "Resultado observado") e tire os prints indicados.

### T01 – Envio e listagem (funcionamento normal)
1. Com o servidor rodando, abra `http://localhost:8000`.
2. Clique em **Escolher arquivos**, escolha um PDF qualquer e clique em **Enviar**.
3. Esperado: mensagem "Arquivo enviado com sucesso." e o arquivo aparece no topo da lista.
4. Prints:
   - `T01-a.png`: página com a mensagem de sucesso e o arquivo na lista
   - `T01-b.png`: terminal mostrando a linha `[UPLOAD]`

### T02 – Download (funcionamento normal)
1. Na lista, clique em **Baixar** no arquivo enviado no T01.
2. Esperado: o arquivo baixa e abre normalmente.
3. Prints:
   - `T02-a.png`: download concluído no navegador
   - `T02-b.png`: terminal mostrando a linha `[DOWNLOAD]`

### T03 – Acesso de outro dispositivo (requisito principal do tema!)
O mínimo exigido para o nosso tema é **enviar e acessar arquivos a partir de dispositivos diferentes**.
1. No terminal, anote o endereço da linha **"Outros dispositivos da mesma rede: http://192.168.x.x:8000"** (aparece também no rodapé da página).
2. No celular, **desligue os dados móveis** e conecte no **mesmo Wi-Fi** do computador.
3. No navegador do celular, digite esse endereço (com `http://` no começo e `:8000` no final).
4. No celular: baixe o arquivo do T01 e envie uma foto.
5. No computador, atualize a página: a foto do celular tem que aparecer na lista.
6. Esperado: as linhas `[UPLOAD]` e `[DOWNLOAD]` no terminal mostram o **IP do celular** (diferente de 127.0.0.1).
7. Prints:
   - `T03-a.png`: print da tela do celular com a página aberta
   - `T03-b.png`: terminal com as linhas mostrando o IP do celular
   - `T03-c.png`: página no computador com a foto do celular na lista

**Se o celular não conseguir abrir:** não mexa no firewall. Anote o erro que apareceu e tire print. Isso também é resultado e vai para o relatório.

### T04 – Métricas: tempo de resposta, disponibilidade e latência
Com o servidor rodando, abra **outro** terminal (Win + R › `cmd`) e rode os comandos abaixo.

**Tempo de resposta (10 requisições):**
```
for /L %i in (1,1,10) do @curl -o NUL -s -w "%{time_total}\n" http://localhost:8000/
```
- Aparecem 10 números em segundos (ex.: `0.004` = 4 ms). Some os 10, divida por 10 e converta para ms. Esse é o **tempo de resposta médio**.

**Disponibilidade (10 requisições):**
```
for /L %i in (1,1,10) do @curl -o NUL -s -w "%{http_code}\n" http://localhost:8000/
```
- Cada `200` é uma resposta com sucesso. Ex.: 10 de 10 = **100% de disponibilidade**.

**Latência e perda de pacotes até o celular (se o T03 funcionou):**
```
ping -n 10 IP-DO-CELULAR
```
- Troque `IP-DO-CELULAR` pelo IP que apareceu no terminal no T03.
- No final aparece a **média em ms** e a **% de perda**.

Prints:
- `T04-a.png`: tempos de resposta
- `T04-b.png`: códigos 200 (disponibilidade)
- `T04-c.png`: resultado do ping (se fez)

### T05 – Falha: servidor fora do ar
1. Deixe a página aberta no navegador.
2. No terminal do servidor, aperte **Ctrl + C**. Aparece "Servidor encerrado.".
3. Na página, escolha um arquivo e clique em **Enviar**.
4. Esperado: aparece **"Erro: não foi possível conectar ao servidor."**
5. No outro terminal, rode de novo o comando de **disponibilidade** do T04.
6. Esperado: aparecem `000` em vez de `200`, ou seja, **0% de disponibilidade**.
7. Prints:
   - `T05-a.png`: página mostrando a mensagem de erro
   - `T05-b.png`: terminal do servidor com "Servidor encerrado."
   - `T05-c.png`: comando de disponibilidade mostrando `000`

### T06 – Recuperação depois da falha
1. No terminal do servidor, rode `python servidor.py` de novo.
2. Atualize a página no navegador.
3. Esperado: todos os arquivos enviados antes continuam na lista, porque ficam salvos no disco.
4. Rode de novo o comando de disponibilidade: tem que voltar a dar `200`.
5. Prints:
   - `T06-a.png`: página com os arquivos ainda na lista
   - `T06-b.png`: disponibilidade de volta a `200`

### T07 – Segurança: nome de arquivo malicioso (opcional, mas vale nota)
1. Crie um arquivo `teste.txt` qualquer dentro da pasta `codigo`.
2. No outro terminal, entre na pasta `codigo` e rode:
```
curl -X POST --data-binary @teste.txt "http://localhost:8000/enviar?nome=..%2F..%2Fteste.txt"
```
3. Esperado: o arquivo é salvo **dentro** da pasta `arquivos`, com o nome `teste.txt`, e nunca fora dela.
4. Agora tente baixar o próprio código do servidor:
```
curl -i "http://localhost:8000/baixar?nome=..%2Fservidor.py"
```
5. Esperado: resposta **404**, ou seja, ninguém consegue pegar arquivos fora da pasta compartilhada.
6. Prints:
   - `T07-a.png`: resultado dos dois comandos
   - `T07-b.png`: pasta `arquivos` mostrando o `teste.txt` lá dentro

---

## 3. Montar o `Grupo02_Testes.pdf` (Pessoa 1)

1. Abra um documento novo (Word ou Google Docs).
2. Título: **Plano e resultados dos testes – Grupo 2 – CompartilhaFATEC**
3. Coloque a tabela abaixo, preenchendo a coluna **"Resultado observado"** e a coluna **"Métrica"** com o que aconteceu **de verdade**:

| ID | Condição inicial | Ação realizada | Resultado esperado | Resultado observado | Métrica | Evidência |
|---|---|---|---|---|---|---|
| T01 – Normal | Servidor em execução | Enviar um PDF pela página | Mensagem de sucesso, arquivo na lista e `[UPLOAD]` no log | | Tempo de resposta (ver T04) | T01-a, T01-b |
| T02 – Normal | Arquivo do T01 na lista | Clicar em Baixar | Download concluído e `[DOWNLOAD]` no log | | – | T02-a, T02-b |
| T03 – Normal (rede) | Servidor em execução; celular no mesmo Wi-Fi | Acessar pelo celular, baixar um arquivo e enviar uma foto | Página abre no celular e o log mostra o IP do celular | | Latência e perda (ping) | T03-a, T03-b, T03-c |
| T04 – Métricas | Servidor em execução | 10 requisições com curl e ping até o celular | Tempo de resposta baixo e 100% de disponibilidade | | Tempo médio (ms), disponibilidade (%), latência (ms), perda (%) | T04-a, T04-b, T04-c |
| T05 – Falha | Servidor encerrado (Ctrl+C) | Tentar enviar arquivo e repetir as 10 requisições | Erro de conexão no navegador e 0% de disponibilidade | | Disponibilidade (%) | T05-a, T05-b, T05-c |
| T06 – Recuperação | Servidor reiniciado | Atualizar a página e repetir as 10 requisições | Arquivos continuam na lista e disponibilidade volta a 100% | | Disponibilidade (%) | T06-a, T06-b |
| T07 – Segurança | Servidor em execução | Enviar nome com `../` e tentar baixar o `servidor.py` | Arquivo salvo dentro da pasta `arquivos` e resposta 404 | | – | T07-a, T07-b |

4. Abaixo da tabela, escreva a **análise** (5 a 10 linhas). Modelo para adaptar com os números reais:

> Os testes T01 e T02 confirmaram o fluxo completo de comunicação: o arquivo saiu do navegador, foi gravado pelo servidor e voltou ao usuário no download. No T03, o acesso pelo celular mostrou a comunicação entre dispositivos diferentes da rede local [ou: foi bloqueado pelo firewall, mostrando que...]. O tempo de resposta médio foi de X ms, com 100% de disponibilidade. No teste de falha (T05), com o servidor encerrado, nenhum cliente conseguiu enviar ou baixar arquivos e a disponibilidade caiu para 0%, o que confirma que o servidor é um ponto único de falha. Após reiniciar (T06), os arquivos continuaram disponíveis, pois ficam armazenados em disco. [Dizer se algum resultado foi diferente do esperado e por quê.]

5. Depois da análise, coloque todos os prints, cada um com uma legenda embaixo. Exemplo: **"Evidência T01-a – Página após o envio, com mensagem de sucesso e arquivo na lista."**
6. Salve em PDF com o nome **`Grupo02_Testes.pdf`**.

---

## 4. Escrever o relatório (Pessoas 2 e 3)

Sigam o **exemplo de relatório da professora** (o modelo do Grupo 4): mesma estrutura, mesmo tipo de capa, figuras e quadros numerados.

**Regras de formatação do exemplo:**
- Figuras com título em cima e fonte embaixo. Ex.: **"Figura 1 – Diagrama de rede do CompartilhaFATEC"** e embaixo **"Fonte: Elaborado pelos autores (2026)."**
- Tabelas chamadas de **Quadro** (Quadro 1, Quadro 2...), com a mesma regra.
- No texto, citar cada figura e quadro (ex.: "conforme a Figura 1").

### 1 Identificação: capa e resumo (Pessoa 2)
- Faculdade, curso, título **"COMPARTILHAFATEC: PROTÓTIPO DE COMPARTILHAMENTO DE ARQUIVOS EM REDE"**, nomes dos 5 integrantes, "Relatório técnico apresentado às disciplinas de Redes de Computadores, Sistemas Distribuídos e Inglês, como parte do Projeto Integrado – Grupo 2", "Ferraz de Vasconcelos, 2026".
- **Resumo** de um parágrafo e palavras-chave (ex.: sistemas distribuídos; redes de computadores; compartilhamento de arquivos; tolerância a falhas).

- Indicar o tema (Compartilhamento distribuído de arquivos), o número do grupo e os integrantes, com **líder (Filipe Acierno)** e **gestor (Michael Coutinho)**.

### 2 Contexto, justificativa e objetivos (Pessoa 2)
- Fonte: **plano de projeto** (seções Motivação, Introdução, Objetivos).
- Incluir: o problema (troca de arquivos por pendrive e mensagens), quem usa (alunos e equipes), objetivo geral e os objetivos específicos.
- Dizer o escopo: o que foi feito e o que ficou para o futuro (está no `IMPLEMENTACAO.md`, parte "fora do escopo").

### 3 Fundamentação teórica (Pessoa 2)
Um ou dois parágrafos para cada conceito, sempre citando uma referência da lista da seção 8 (Referências):
- **3.1 Modelo TCP/IP e endereçamento:** camadas, endereço IP, rede local, máscara /24, gateway e DHCP.
- **3.2 HTTP e modelo cliente-servidor:** requisição e resposta, métodos GET e POST, códigos 200/400/404/413, porta 8000.
- **3.3 Sistemas distribuídos e tolerância a falhas:** componentes que se comunicam por mensagens, ponto único de falha, disponibilidade.
- **3.4 Métricas:** latência, tempo de resposta, disponibilidade e perda de pacotes.

### 4 Topologia e arquitetura (Pessoa 2)
- Fonte: **documento da Etapa 2** (seções 1.1 a 1.5) e os diagramas da pasta `Etapa2/diagramas`.
- Colocar o diagrama de rede (Figura) e a tabela de endereçamento (Quadro).
- Colocar o diagrama da arquitetura (Figura) e explicar os componentes.
- Copiar e adaptar o **fluxo de comunicação** (seção 1.3) e a **falha** (seção 1.7).

### 5 Ferramentas e procedimentos (Pessoa 3)
- Fonte: **`codigo/IMPLEMENTACAO.md`** e **`codigo/COMO_RODAR.md`**.
- Quadro de ferramentas com versões (Python 3.14, navegador, draw.io, GitHub...).
- Passos para rodar o protótipo (do COMO_RODAR).
- **Quadro implementado × simulado**. Modelo:

| Componente | Situação | Como foi feito |
|---|---|---|
| Servidor de arquivos | Implementado | Programa em Python (`servidor.py`) com `http.server` |
| Interface web | Implementado | Página HTML, CSS e JavaScript servida pelo próprio servidor |
| Armazenamento | Implementado | Pasta `arquivos` no disco do PC Servidor |
| Rede local | Real (não simulada) | Rede Wi-Fi doméstica com roteador |
| Clientes | Implementado | Navegador do computador e do celular |

- **Dificuldades e decisões:** o bloqueio do firewall no PC de desenvolvimento (está no IMPLEMENTACAO.md) e como foi resolvido no teste T03.

### 6 Testes e resultados (Pessoa 3)
- Copiar a tabela e a análise do `Grupo02_Testes.pdf`.
- Colocar os prints principais como figuras (ex.: T01-a, T03-a, T05-a, T06-a), cada um citado no texto.

### 7 Limitações, melhorias e conclusão (Pessoa 3)
- **Limitações:** um único servidor (ponto único de falha), sem login e senha, sem HTTPS, depende do firewall liberar a porta 8000.
- **Melhorias:** segundo servidor com cópia dos arquivos (replicação), login de usuários, HTTPS.
- **Conclusão:** dizer se os objetivos foram atingidos, com base nos testes.

**Uso de IA:** se usarem IA para escrever ou revisar o relatório, declarem no final, igual foi feito na Etapa 2.

Salvar em PDF com o nome **`Grupo02_Relatorio.pdf`**.

---

## 5. Montar a entrega no GitHub (Pessoa 3)

A pasta `Etapa3/codigo` já está no repositório. Faltam os PDFs e as evidências.

1. Abra o repositório **Grupo02_ProjetoIntegrado** e entre na pasta **Etapa3**.
2. Clique em **Add file › Upload files**.
3. Arraste: `Grupo02_Relatorio.pdf`, `Grupo02_Testes.pdf` e a **pasta `evidencias`** (com os prints T01-a, T01-b...).
4. Clique em **Commit changes**.
5. Confira se a pasta Etapa3 ficou assim:

```
Etapa3/
├── Grupo02_Relatorio.pdf
├── Grupo02_Testes.pdf
├── evidencias/
│   ├── T01-a.png
│   ├── T01-b.png
│   └── ...
└── codigo/
    ├── servidor.py
    ├── COMO_RODAR.md
    └── IMPLEMENTACAO.md
```

6. Abra o link do repositório numa **aba anônima** para confirmar que abre sem login.
7. Cole o link na tarefa da Etapa 3 nas **três equipes do Teams**: Redes de Computadores, Sistemas Distribuídos e Inglês.
8. Avise no grupo que entregou.

**Atenção:** não coloquem a pasta `arquivos` (a que guarda os arquivos enviados nos testes) no GitHub, nem senhas ou dados pessoais.

---

## Checklist final (conferir antes de enviar)

- [ ] Testes T01 a T06 feitos (T07 opcional), com resultado observado preenchido
- [ ] Teste com outro dispositivo (T03) feito, ou o erro registrado
- [ ] Métricas preenchidas (tempo de resposta, disponibilidade e, se possível, latência)
- [ ] Todos os prints com nome do teste e legenda
- [ ] `Grupo02_Testes.pdf` com tabela, análise e evidências
- [ ] `Grupo02_Relatorio.pdf` com as 8 partes na ordem e referências em ABNT
- [ ] Quadro implementado × simulado no relatório
- [ ] Tudo na pasta `Etapa3` do repositório
- [ ] Link testado em aba anônima
- [ ] Link enviado nas 3 equipes
- [ ] Todo mundo leu o relatório
