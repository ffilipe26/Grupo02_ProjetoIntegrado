# CompartilhaFATEC - servidor de arquivos
# Versão 7 (final): lista, envia (upload) e baixa (download) arquivos pelo navegador,
#           mostra o endereço para outros dispositivos da rede, tem a interface
#           nas cores da Fatec e trata envios interrompidos e nomes inválidos

import html
import mimetypes
import socket
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs, quote
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORTA = 8000  # porta onde o servidor fica "escutando" as requisições
LIMITE_MB = 50  # tamanho máximo de arquivo aceito no envio

# Pasta compartilhada (o "armazenamento" do diagrama de blocos).
# Fica ao lado deste arquivo: codigo/arquivos
PASTA_ARQUIVOS = Path(__file__).parent / "arquivos"

# Modelo da página. Os trechos {{...}} são trocados pelos dados reais.
# Todo o visual (CSS) e o comportamento da página (JavaScript) ficam aqui dentro,
# sem depender de internet: funciona mesmo em rede sem acesso externo.
PAGINA = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CompartilhaFATEC</title>
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%23B3121B'/%3E%3Cpath d='M11 8h11v4h-7v3h6v4h-6v6h-4z' fill='white'/%3E%3C/svg%3E">
  <style>
    :root {
      --grafite: #33434D;       /* cinza do logotipo da Fatec */
      --grafite-suave: #66757F;
      --vermelho: #B3121B;      /* vermelho Fatec / Centro Paula Souza */
      --vermelho-escuro: #8E0E15;
      --fundo: #F3F5F6;
      --superficie: #FFFFFF;
      --linha: #DCE1E4;
      --sucesso: #1D7148;
      --fonte: "Segoe UI Variable Text", "Segoe UI", system-ui, -apple-system, Roboto, "Helvetica Neue", Arial, sans-serif;
      --fonte-titulo: "Segoe UI Variable Display", "Segoe UI", system-ui, -apple-system, Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    * { box-sizing: border-box; }
    html { -webkit-text-size-adjust: 100%; }
    body {
      margin: 0;
      background: var(--fundo);
      color: var(--grafite);
      font-family: var(--fonte);
      font-size: 16px;
      line-height: 1.5;
    }
    .pagina { max-width: 760px; margin: 0 auto; padding: 56px 24px 40px; }

    /* Marca: mesma lógica do logotipo da Fatec (nome em grafite, unidade em vermelho) */
    .marca { border-left: 4px solid var(--vermelho); padding-left: 16px; margin-bottom: 40px; }
    .marca h1 {
      font-family: var(--fonte-titulo);
      font-size: 2.25rem; line-height: 1.1; font-weight: 700;
      letter-spacing: -0.02em; margin: 0;
    }
    .marca .unidade { color: var(--vermelho); font-weight: 600; font-size: 0.95rem; margin: 4px 0 0; }
    .marca .descricao { color: var(--grafite-suave); margin: 14px 0 0; }

    /* Área de envio */
    .envio {
      background: var(--superficie);
      border: 1.5px dashed #AEB8BE;
      border-radius: 10px;
      padding: 32px 24px;
      text-align: center;
      transition: border-color .15s, background-color .15s;
    }
    .envio.arrastando { border-color: var(--vermelho); background: #FBF3F3; }
    .envio p { margin: 0; }
    .envio .instrucao { font-size: 1.05rem; font-weight: 600; }
    .envio .limite { color: var(--grafite-suave); font-size: .875rem; margin-top: 6px; }
    .envio input[type=file] { position: absolute; width: 1px; height: 1px; opacity: 0; }
    .escolher {
      display: inline-block; margin-top: 18px;
      color: var(--grafite); font-weight: 600; font-size: .95rem;
      border: 1.5px solid var(--grafite); border-radius: 8px;
      padding: 9px 18px; cursor: pointer; background: var(--superficie);
    }
    .escolher:hover { background: var(--fundo); }
    .selecionados { margin-top: 14px; font-size: .9rem; color: var(--grafite-suave); word-break: break-word; }
    .botao-enviar {
      display: block; width: 100%; margin-top: 16px;
      font: inherit; font-weight: 600; font-size: 1rem;
      color: #fff; background: var(--vermelho);
      border: 0; border-radius: 8px; padding: 13px 18px; cursor: pointer;
    }
    .botao-enviar:hover:not(:disabled) { background: var(--vermelho-escuro); }
    .botao-enviar:disabled { background: #C9CFD3; cursor: not-allowed; }

    .progresso { height: 4px; background: var(--linha); border-radius: 2px; margin-top: 16px; overflow: hidden; display: none; }
    .progresso.ativo { display: block; }
    .progresso div { height: 100%; width: 0; background: var(--vermelho); transition: width .1s linear; }
    .status { min-height: 1.5em; margin: 10px 0 0; font-size: .95rem; font-weight: 600; }
    .status.ok { color: var(--sucesso); }
    .status.erro { color: var(--vermelho); }

    /* Lista de arquivos */
    .cabecalho-lista { display: flex; justify-content: space-between; align-items: baseline; margin: 44px 0 10px; }
    .cabecalho-lista h2 { font-family: var(--fonte-titulo); font-size: 1.25rem; font-weight: 700; margin: 0; letter-spacing: -0.01em; }
    .cabecalho-lista span { color: var(--grafite-suave); font-size: .9rem; }
    .lista { list-style: none; margin: 0; padding: 0; background: var(--superficie); border: 1px solid var(--linha); border-radius: 10px; }
    .arquivo {
      display: grid; grid-template-columns: 48px 1fr auto auto; gap: 16px; align-items: center;
      padding: 14px 18px; border-top: 1px solid var(--linha);
    }
    .arquivo:first-child { border-top: 0; }
    .tipo {
      width: 48px; height: 48px; border-radius: 8px;
      background: #EEF1F3; color: var(--grafite);
      display: grid; place-items: center;
      font-size: .7rem; font-weight: 700; letter-spacing: .02em;
    }
    .tipo.pdf { background: #F7E4E5; color: var(--vermelho); }
    .info { min-width: 0; }
    .nome { display: block; font-weight: 600; color: var(--grafite); text-decoration: none; overflow-wrap: anywhere; }
    .nome:hover { color: var(--vermelho); }
    .data { color: var(--grafite-suave); font-size: .85rem; }
    .tamanho { color: var(--grafite-suave); font-size: .9rem; white-space: nowrap; }
    .baixar {
      color: var(--grafite); font-weight: 600; font-size: .9rem; text-decoration: none;
      border: 1.5px solid #C3CBD0; border-radius: 8px; padding: 7px 14px; white-space: nowrap;
    }
    .baixar:hover { border-color: var(--vermelho); color: var(--vermelho); }
    .vazio { padding: 36px 18px; text-align: center; color: var(--grafite-suave); }

    .rodape { margin-top: 40px; font-size: .875rem; color: var(--grafite-suave); }
    .rodape strong { color: var(--grafite); font-weight: 600; }

    a:focus-visible, button:focus-visible, .escolher:focus-within {
      outline: 3px solid #E7A1A5; outline-offset: 2px;
    }
    @media (max-width: 560px) {
      .pagina { padding-top: 36px; }
      .marca h1 { font-size: 1.85rem; }
      .arquivo { grid-template-columns: 40px 1fr auto; gap: 12px; padding: 12px 14px; }
      .tipo { width: 40px; height: 40px; }
      .tamanho { display: none; }
    }
    .so-toque { display: none; }
    @media (pointer: coarse) {
      .so-mouse { display: none; }
      .so-toque { display: inline; }
    }
    @media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
  </style>
</head>
<body>
  <main class="pagina">
    <header class="marca">
      <h1>CompartilhaFATEC</h1>
      <p class="unidade">Fatec Ferraz de Vasconcelos</p>
      <p class="descricao">Envie e baixe arquivos com quem está na mesma rede.</p>
    </header>

    <section class="envio" id="envio">
      <p class="instrucao"><span class="so-mouse">Arraste arquivos para cá</span><span class="so-toque">Escolha os arquivos para enviar</span></p>
      <p class="limite"><span class="so-mouse">ou escolha no computador. </span>Até {{LIMITE}} MB por arquivo.</p>
      <label class="escolher">
        Escolher arquivos
        <input type="file" id="arquivo" multiple>
      </label>
      <p class="selecionados" id="selecionados"></p>
      <button class="botao-enviar" id="botao-enviar" disabled>Enviar</button>
      <div class="progresso" id="progresso"><div></div></div>
      <p class="status" id="status" role="status"></p>
    </section>

    <div class="cabecalho-lista">
      <h2>Arquivos disponíveis</h2>
      <span id="total">{{TOTAL}}</span>
    </div>
    <div id="lista">{{LISTA}}</div>

    <p class="rodape">{{ENDERECO}}</p>
  </main>

  <script>
    const LIMITE_BYTES = {{LIMITE}} * 1024 * 1024;
    const area = document.getElementById("envio");
    const input = document.getElementById("arquivo");
    const botao = document.getElementById("botao-enviar");
    const selecionados = document.getElementById("selecionados");
    const status = document.getElementById("status");
    const progresso = document.getElementById("progresso");
    const barra = progresso.querySelector("div");
    let fila = [];

    function mostrarStatus(texto, tipo) {
      status.textContent = texto;
      status.className = "status " + (tipo || "");
    }

    function escolher(arquivos) {
      fila = Array.from(arquivos);
      selecionados.textContent = fila.length === 1
        ? fila[0].name
        : fila.length + " arquivos selecionados";
      botao.disabled = fila.length === 0;
      mostrarStatus("");
    }

    input.addEventListener("change", () => escolher(input.files));

    // Arrastar e soltar arquivos na área de envio
    ["dragenter", "dragover"].forEach(ev => area.addEventListener(ev, e => {
      e.preventDefault(); area.classList.add("arrastando");
    }));
    ["dragleave", "drop"].forEach(ev => area.addEventListener(ev, e => {
      e.preventDefault(); area.classList.remove("arrastando");
    }));
    area.addEventListener("drop", e => escolher(e.dataTransfer.files));

    // Envia um arquivo (requisição POST) e acompanha o progresso
    function enviarUm(arquivo) {
      return new Promise((resolve, reject) => {
        const req = new XMLHttpRequest();
        req.open("POST", "/enviar?nome=" + encodeURIComponent(arquivo.name));
        req.upload.onprogress = e => {
          if (e.lengthComputable) barra.style.width = (e.loaded / e.total * 100) + "%";
        };
        req.onload = () => (req.status === 200 ? resolve(req.responseText) : reject(req.responseText));
        req.onerror = () => reject("Erro: não foi possível conectar ao servidor.");
        req.send(arquivo);
      });
    }

    // Busca a página de novo e troca só a lista, sem recarregar tudo
    async function atualizarLista() {
      const resposta = await fetch("/");
      const doc = new DOMParser().parseFromString(await resposta.text(), "text/html");
      document.getElementById("lista").innerHTML = doc.getElementById("lista").innerHTML;
      document.getElementById("total").textContent = doc.getElementById("total").textContent;
    }

    botao.addEventListener("click", async () => {
      const grande = fila.find(a => a.size > LIMITE_BYTES);
      if (grande) {
        mostrarStatus("O arquivo " + grande.name + " passa do limite de {{LIMITE}} MB.", "erro");
        return;
      }
      botao.disabled = true;
      progresso.classList.add("ativo");
      let enviados = 0;
      try {
        for (const arquivo of fila) {
          barra.style.width = "0";
          mostrarStatus("Enviando " + arquivo.name + "...");
          await enviarUm(arquivo);
          enviados++;
        }
        mostrarStatus(enviados === 1 ? "Arquivo enviado com sucesso." : enviados + " arquivos enviados com sucesso.", "ok");
        await atualizarLista();
      } catch (erro) {
        mostrarStatus(erro, "erro");
      } finally {
        progresso.classList.remove("ativo");
        fila = [];
        input.value = "";
        selecionados.textContent = "";
      }
    });
  </script>
</body>
</html>"""


def listar_arquivos():
    """Devolve os arquivos da pasta compartilhada, do mais recente para o mais antigo."""
    arquivos = [p for p in PASTA_ARQUIVOS.iterdir() if p.is_file()]
    return sorted(arquivos, key=lambda p: p.stat().st_mtime, reverse=True)


def tamanho_legivel(num_bytes):
    """Converte bytes em texto fácil de ler: 830 B, 197,7 KB, 2,3 MB."""
    if num_bytes < 1024:
        return f"{num_bytes} B"
    if num_bytes < 1024 * 1024:
        return f"{num_bytes / 1024:.1f} KB".replace(".", ",")
    return f"{num_bytes / (1024 * 1024):.1f} MB".replace(".", ",")


def montar_pagina():
    """Monta a página HTML com a lista de arquivos disponíveis."""
    arquivos = listar_arquivos()

    if arquivos:
        itens = ""
        for arq in arquivos:
            info = arq.stat()
            link = "/baixar?nome=" + quote(arq.name)  # endereço de download do arquivo
            nome = html.escape(arq.name)  # protege a página caso o nome tenha símbolos como < >
            extensao = arq.suffix[1:].upper()[:4] or "ARQ"
            classe_tipo = "tipo pdf" if extensao == "PDF" else "tipo"
            data = datetime.fromtimestamp(info.st_mtime).strftime("%d/%m/%Y às %H:%M")
            itens += f"""
        <li class="arquivo">
          <span class="{classe_tipo}">{html.escape(extensao)}</span>
          <div class="info">
            <a class="nome" href="{link}">{nome}</a>
            <span class="data">Enviado em {data}</span>
          </div>
          <span class="tamanho">{tamanho_legivel(info.st_size)}</span>
          <a class="baixar" href="{link}" aria-label="Baixar {nome}">Baixar</a>
        </li>"""
        lista = f'<ul class="lista">{itens}\n      </ul>'
        total = "1 arquivo" if len(arquivos) == 1 else f"{len(arquivos)} arquivos"
    else:
        lista = ('<div class="lista"><p class="vazio">Nenhum arquivo por aqui ainda. '
                 'Envie o primeiro pela área acima.</p></div>')
        total = "0 arquivos"

    ip_local = descobrir_ip_local()
    if ip_local:
        endereco = f"Para acessar de outro dispositivo da mesma rede, use <strong>http://{ip_local}:{PORTA}</strong>"
    else:
        endereco = "Servidor em execução neste computador."

    return (PAGINA.replace("{{LISTA}}", lista)
                  .replace("{{TOTAL}}", total)
                  .replace("{{ENDERECO}}", endereco)
                  .replace("{{LIMITE}}", str(LIMITE_MB)))


# Nomes que o Windows reserva para dispositivos e não aceita como nome de arquivo
NOMES_RESERVADOS = {"CON", "PRN", "AUX", "NUL",
                    *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}


def nome_seguro(nome):
    """
    Limpa o nome do arquivo enviado para evitar acesso fora da pasta compartilhada.
    Ex.: "../../Windows/teste.txt" vira só "teste.txt".
    Devolve None se o nome for inválido.
    """
    nome = nome.replace("\\", "/").split("/")[-1]  # fica só com o nome, sem caminho
    nome = "".join(c for c in nome if ord(c) >= 32)  # remove caracteres de controle
    for caractere in '<>:"|?*':  # caracteres proibidos em nomes de arquivo no Windows
        nome = nome.replace(caractere, "_")
    nome = nome.strip().rstrip(". ")  # o Windows não aceita nome terminando em ponto ou espaço
    if nome in ("", ".", ".."):
        return None
    if Path(nome).stem.upper() in NOMES_RESERVADOS:
        nome = "_" + nome
    if len(nome) > 200:  # nomes muito longos dão erro no sistema de arquivos
        nome = Path(nome).stem[:190] + Path(nome).suffix[:10]
    return nome


def criar_arquivo_livre(nome):
    """
    Cria o arquivo na pasta compartilhada sem sobrescrever nenhum outro.
    Se o nome já existir, tenta 'nome (1).ext', 'nome (2).ext'...
    O modo "xb" só cria o arquivo se ele ainda não existir: assim, dois envios
    simultâneos com o mesmo nome nunca gravam no mesmo arquivo.
    Devolve o caminho criado e o arquivo aberto para escrita.
    """
    numero = 0
    while True:
        if numero == 0:
            caminho = PASTA_ARQUIVOS / nome
        else:
            caminho = PASTA_ARQUIVOS / f"{Path(nome).stem} ({numero}){Path(nome).suffix}"
        try:
            return caminho, open(caminho, "xb")
        except FileExistsError:
            numero += 1


def descobrir_ip_local():
    """
    Descobre o IP deste computador na rede local (ex.: 192.168.0.15).
    Truque: "conecta" um socket UDP a um endereço externo só para o sistema escolher
    a placa de rede certa. Nenhum dado é enviado de verdade.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return None


class Servidor(BaseHTTPRequestHandler):
    # Roda toda vez que o navegador faz uma requisição GET (pedir uma página)
    def do_GET(self):
        endereco = urlparse(self.path)
        if endereco.path == "/":
            # Página principal: formulário de envio + lista de arquivos
            self.responder(montar_pagina(), tipo="text/html")
        elif endereco.path == "/baixar":
            # Download de um arquivo da pasta compartilhada
            self.baixar(parse_qs(endereco.query).get("nome", [""])[0])
        else:
            self.send_error(404)

    def baixar(self, nome_pedido):
        """Envia para o navegador o arquivo pedido, se ele existir na pasta compartilhada."""
        nome = nome_seguro(nome_pedido)
        caminho = PASTA_ARQUIVOS / nome if nome else None
        if caminho is None or not caminho.is_file():
            self.responder("Arquivo não encontrado.", status=404)
            return

        tamanho = caminho.stat().st_size
        tipo = mimetypes.guess_type(caminho.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(tamanho))
        # "attachment" faz o navegador baixar o arquivo em vez de abrir na tela
        self.send_header("Content-Disposition", f"attachment; filename*=UTF-8''{quote(caminho.name)}")
        self.end_headers()

        # Envia o arquivo em partes, para não carregar tudo na memória de uma vez
        try:
            with open(caminho, "rb") as entrada:
                while pedaco := entrada.read(65536):
                    self.wfile.write(pedaco)
        except (ConnectionError, TimeoutError):
            # O cliente cancelou o download ou a conexão caiu no meio
            print(f"[DOWNLOAD INTERROMPIDO] {caminho.name} para {self.client_address[0]}")
            return

        print(f"[DOWNLOAD] {caminho.name} ({tamanho} bytes) enviado para {self.client_address[0]}")

    # Roda toda vez que o navegador faz uma requisição POST (enviar dados)
    def do_POST(self):
        endereco = urlparse(self.path)
        if endereco.path != "/enviar":
            self.send_error(404)
            return

        # Pega o nome do arquivo que veio no endereço (?nome=...)
        nome = nome_seguro(parse_qs(endereco.query).get("nome", [""])[0])
        if nome is None:
            self.responder("Nome de arquivo inválido.", status=400)
            return

        # Confere o tamanho antes de receber (Content-Length = tamanho do conteúdo enviado)
        try:
            tamanho = int(self.headers.get("Content-Length", ""))
        except ValueError:
            self.responder("Tamanho do arquivo não informado.", status=411)
            return
        if tamanho < 0:
            self.responder("Tamanho do arquivo inválido.", status=400)
            return
        if tamanho > LIMITE_MB * 1024 * 1024:
            self.responder(f"Arquivo muito grande (limite: {LIMITE_MB} MB).", status=413)
            return

        # Recebe o conteúdo em partes e grava na pasta compartilhada
        try:
            destino, saida = criar_arquivo_livre(nome)
        except OSError:
            self.responder("Não foi possível gravar o arquivo com esse nome.", status=400)
            return

        restante = tamanho
        try:
            with saida:
                while restante > 0:
                    pedaco = self.rfile.read(min(65536, restante))
                    if not pedaco:
                        break  # a conexão terminou antes de o arquivo chegar inteiro
                    saida.write(pedaco)
                    restante -= len(pedaco)
        except (ConnectionError, TimeoutError):
            pass  # tratado logo abaixo como envio incompleto

        if restante > 0:
            # Envio interrompido: apaga o pedaço recebido para não deixar arquivo corrompido
            destino.unlink(missing_ok=True)
            print(f"[UPLOAD INTERROMPIDO] {nome} de {self.client_address[0]}: arquivo incompleto descartado")
            try:
                self.responder("Envio interrompido. O arquivo não foi salvo.", status=400)
            except (ConnectionError, TimeoutError):
                pass
            return

        print(f"[UPLOAD] {destino.name} ({tamanho} bytes) recebido de {self.client_address[0]}")
        self.responder(f"Arquivo '{destino.name}' enviado com sucesso!")

    def responder(self, texto, status=200, tipo="text/plain"):
        """Envia uma resposta (página ou mensagem) para o navegador."""
        corpo = texto.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{tipo}; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)


if __name__ == "__main__":
    PASTA_ARQUIVOS.mkdir(exist_ok=True)  # cria a pasta "arquivos" se ainda não existir

    # "0.0.0.0" = aceita conexões de qualquer dispositivo da rede (PC, celular...)
    servidor = ThreadingHTTPServer(("0.0.0.0", PORTA), Servidor)
    ip_local = descobrir_ip_local()
    print(f"Servidor rodando em http://localhost:{PORTA}  (neste computador)")
    if ip_local:
        print(f"Outros dispositivos da mesma rede: http://{ip_local}:{PORTA}")
    print(f"Pasta compartilhada: {PASTA_ARQUIVOS}")
    print("Para parar, aperte Ctrl+C")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
