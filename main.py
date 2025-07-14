from playwright.sync_api import sync_playwright
import os

pasta_texto = r"C:\Users\User\Desktop\Processo_automatizado_de_criacao_de_video\pasta_texto"
os.makedirs(pasta_texto, exist_ok=True)

with sync_playwright() as p:
    try:
        # Tenta usar o primeiro caminho
        browser = p.chromium.launch(channel="chrome", headless=False,
                                    executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe')
    except Exception as e:
        try:
            # Tenta usar o segundo caminho se o primeiro falhar
            browser = p.chromium.launch(channel="chrome", headless=False,
                                        executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
        except Exception as e:
            browser = None

    if browser:
        pass


    # Criar uma nova página
    context = browser.new_context()
    page = context.new_page()
    page.set_viewport_size({"width": 1366, "height": 768})
    page.wait_for_timeout(1000)

    # Primeira URL
    url = "https://novelmania.com.br/novels/contra-os-deuses/capitulos/volume-1-arco-1-prologo"
    while True:
        page.goto(url)
        page.wait_for_timeout(2000)

        # Pega o título
        page.wait_for_selector(".mt-0.mb-3.text-center")
        titulo = page.inner_text(".mt-0.mb-3.text-center").strip()
        print(f"Coletando: {titulo}")

        # Gera nome de arquivo seguro
        nome_arquivo = "".join(c for c in f"{titulo}.txt" if c not in r'\/:*?"<>|')
        caminho_arquivo = os.path.join(pasta_texto, nome_arquivo)

        # Pega os parágrafos
        elements = page.query_selector_all("#chapter-content > *")
        paragraphs = []
        for el in elements:
            tag_name = el.evaluate("e => e.tagName.toLowerCase()")
            if tag_name == "div":
                id_attr = el.get_attribute("id")
                if id_attr == "reactions-component":
                    break
            if tag_name == "p":
                paragraphs.append(el.inner_text().strip())

        # Salva no arquivo
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(titulo + "\n\n")
            for p in paragraphs:
                f.write(p + "\n\n")

        print(f"Arquivo salvo em: {caminho_arquivo}")

        pageLuvvoice = context.new_page()
        pageLuvvoice.goto("https://luvvoice.com/")

        #clica no botão conecte-se para fazer login
        page.click("button:has-text('Conecte-se')")

        # Verifica se existe botão Próximo
        proximo = page.query_selector('a[title="Próximo capítulo"]')
        if proximo:
            url = proximo.get_attribute("href")
            # Ajusta para URL completa se necessário
            if url.startswith("/"):
                url = "https://novelmania.com.br" + url
            page.wait_for_timeout(1000)
        else:
            print("Não há mais capítulos. Processo finalizado.")
            break

    #testando o site de transformação de texto em áudio

    page.wait_for_timeout(20000)
