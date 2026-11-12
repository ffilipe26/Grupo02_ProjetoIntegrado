# Implementação do protótipo

Base para a seção "Ferramentas e procedimentos" do relatório (Etapa 3).

## Ferramentas

- **Python 3.14** com módulos da biblioteca padrão: `http.server` (servidor HTTP), `pathlib` (pastas e arquivos), `urllib.parse` (endereços), `html`, `mimetypes`, `datetime` e `socket` (descobrir o IP local).
- **Navegador web** como cliente (página HTML, CSS e JavaScript, nas cores da Fatec, que funciona no computador e no celular).
- **Terminal do Windows** para rodar o servidor e ver os logs.

## O que foi implementado (funcionando)

- **Listar** os arquivos da pasta compartilhada, do mais recente para o mais antigo, com tipo, tamanho e data (`GET /`).
- **Enviar** arquivos pelo navegador (`POST /enviar`), um ou vários de uma vez, escolhendo ou arrastando, com barra de progresso.
- **Baixar** arquivos pelo navegador (`GET /baixar`).
- **Validação do nome do arquivo:** remove caminhos como `../`, caracteres proibidos e de controle, trata nomes reservados do Windows (ex.: `CON`) e nomes muito longos, impedindo acesso fora da pasta compartilhada.
- **Nome repetido:** salva como `nome (1).ext` em vez de apagar o arquivo antigo.
- **Limite de tamanho:** 50 MB por arquivo (resposta 413 se passar).
- **Respostas de erro:** 400 (nome inválido ou envio interrompido), 404 (arquivo ou endereço inexistente), 411 (tamanho não informado), 413 (arquivo grande).
- **Envio interrompido:** se a conexão cai no meio do envio, o pedaço recebido é apagado, para não deixar arquivo corrompido na lista.
- **Envios simultâneos com o mesmo nome:** cada envio gera um arquivo diferente, sem um sobrescrever o outro.
- **Registro (log)** de cada requisição, com linhas `[UPLOAD]` e `[DOWNLOAD]` mostrando arquivo, tamanho e IP do cliente, e `[UPLOAD INTERROMPIDO]` e `[DOWNLOAD INTERROMPIDO]` quando a conexão cai.
- **Atendimento simultâneo** de vários clientes (`ThreadingHTTPServer`).
- O servidor mostra ao iniciar o endereço para acesso pela rede local.

Nada foi simulado: todas as funções acima rodam de verdade.

## O que ficou fora do escopo (possibilidade futura)

- contas de usuário e senha;
- HTTPS (criptografia);
- segundo servidor com cópia dos arquivos (replicação);
- excluir ou renomear arquivos pela página;
- uso pela internet.

## Decisões técnicas

- **Só biblioteca padrão:** basta ter o Python instalado, sem instalar pacotes.
- **Envio com JavaScript, com o arquivo direto no corpo da requisição:** evita o formato multipart, cujo módulo de leitura (`cgi`) foi removido das versões recentes do Python. É usado `XMLHttpRequest` para mostrar a barra de progresso.
- **Criação exclusiva do arquivo (modo `xb`):** como o servidor atende vários clientes ao mesmo tempo, dois envios com o mesmo nome poderiam gravar no mesmo arquivo; esse modo só cria o arquivo se ele ainda não existir.
- **Interface sem dependências externas:** todo o visual fica dentro do `servidor.py`, então funciona mesmo em rede sem internet.
- **Arquivos gravados e lidos em partes de 64 KB:** arquivos grandes não ocupam toda a memória.
- **`0.0.0.0` na porta 8000:** o servidor aceita conexões de qualquer dispositivo da rede.

## Dificuldades encontradas

- **Acesso de outro dispositivo bloqueado:** o celular não conseguiu acessar o servidor (erro `ERR_TOO_MANY_RETRIES`), tanto no Wi-Fi de casa quanto no hotspot do celular. Pelo próprio PC, o acesso funcionou por `localhost` e pelo IP da rede. A causa identificada foi o **firewall do Windows**: as regras de entrada do Python estavam desabilitadas para o perfil de rede privada. O teste deve ser repetido em outro equipamento.

## Desenvolvimento por etapas

1. Servidor básico respondendo uma página de teste.
2. Listagem dos arquivos da pasta.
3. Envio (upload) com validação de nome, nome repetido e limite de tamanho.
4. Download com a mesma validação.
5. Exibição do IP local para acesso por outros dispositivos.
6. Nova interface visual nas cores da Fatec, com arrastar e soltar, envio múltiplo e barra de progresso.
7. Tratamento de envios e downloads interrompidos, nomes inválidos e envios simultâneos.
