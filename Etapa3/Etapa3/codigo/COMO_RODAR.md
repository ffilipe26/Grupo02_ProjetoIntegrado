# Como rodar o CompartilhaFATEC

Passo a passo para executar o protótipo.

## Requisitos

- Python 3.8 ou mais recente (testado com Python 3.14).
- Nenhuma biblioteca extra: o servidor usa só a biblioteca padrão do Python.
- Um navegador.

## Passo a passo

1. Instale o Python em python.org. No instalador, marque **"Add python.exe to PATH"**.
2. Confira a instalação: abra o terminal e rode `python --version`.
3. Abra o terminal dentro da pasta `codigo` (no Windows: abra a pasta, digite `cmd` na barra de endereço e dê Enter).
4. Rode:
   ```
   python servidor.py
   ```
5. O terminal mostra:
   ```
   Servidor rodando em http://localhost:8000  (neste computador)
   Outros dispositivos da mesma rede: http://192.168.x.x:8000
   Pasta compartilhada: ...\codigo\arquivos
   ```
6. No navegador do mesmo computador, abra `http://localhost:8000`.
7. Para acessar de outro dispositivo, ele precisa estar na mesma rede. Use o endereço da linha "Outros dispositivos da mesma rede". O firewall precisa permitir a porta 8000.
8. Para parar o servidor, aperte **Ctrl+C** no terminal.

## Como usar

- **Enviar:** clique em "Escolher arquivos" (ou arraste os arquivos para a área de envio) e depois em "Enviar". Dá para enviar vários de uma vez.
- **Listar:** a lista aparece na página principal, do mais recente para o mais antigo, com tipo, tamanho e data de envio.
- **Baixar:** clique em "Baixar" ou no nome do arquivo.

Os arquivos ficam na pasta `codigo/arquivos`, criada automaticamente.

## Como reproduzir o teste de falha

1. Com a página aberta no navegador, pare o servidor com **Ctrl+C**.
2. Tente enviar um arquivo: aparece "Erro: não foi possível conectar ao servidor".
3. Rode `python servidor.py` de novo e atualize a página: os arquivos continuam na lista.
