from selenium import webdriver
from selenium.webdriver.chrome.service import service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.opera import OperaDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
from io import StringIO
import json
import os

usuario = "DIGITE O SEU USUARIO"
senha = "DIGITE A SUA SENHA"

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

webdriver_service = service.Service(OperaDriverManager().install())
webdriver_service.start()

#iniciando...
navegador = webdriver.Remote(webdriver_service.service_url, webdriver.DesiredCapabilities.OPERA,options=options)

try:
    navegador.get("https://sigaa.uern.br/sigaa/verTelaLogin.do")

    navegador.find_element('xpath', '//*[@id="conteudo"]/div[4]/form/table/tbody/tr[1]/td/input').send_keys(usuario)
    navegador.find_element('xpath', '//*[@id="conteudo"]/div[4]/form/table/tbody/tr[2]/td/input').send_keys(senha)
    time.sleep(1)
    navegador.find_element('xpath', '//*[@id="conteudo"]/div[4]/form/table/tfoot/tr/td/input').click()
    time.sleep(1)

    try:
        navegador.find_element('xpath', '//*[@id="menu_form_menu_discente_j_id_jsp_340461267_98_menu"]/table/tbody/tr/td[1]').click()
        time.sleep(1)
        navegador.find_element('xpath', '//*[@id="cmSubMenuID1"]/table/tbody/tr[1]/td[2]').click()
        time.sleep(1)
    except Exception as e:
        print("Erro ao tentar navegar pelos menus: ", e)
        navegador.quit()
        exit()

    # Trabalhando com Tabela
    try:
        tableTicket = navegador.find_element('xpath', '//*[@id="relatorio"]/div/table[1]')
        htmlContent = tableTicket.get_attribute("outerHTML")  # Pegando todo o HTML da tabela 2024.1
    except Exception as e:
        print("Erro ao localizar a tabela: ", e)
        navegador.quit()
        exit()

    soup = BeautifulSoup(htmlContent, "html.parser")
    tickets = soup.find(name="table")
    sio = StringIO(str(tickets))
    df = pd.read_html(sio)[0]

    # Diretório onde deseja salvar o arquivo JSON
    diretorio = r"SigaaUERN-Api\Results"  # Use a string bruta para evitar problemas com escape sequence

    # Verifica se o diretório existe, se não, cria-o
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    # Caminho completo para o arquivo JSON
    caminho_arquivo = os.path.join(diretorio, f"tabela_{usuario}.json")

    # Salvando o DataFrame como JSON com indentação
    json_str = df.to_json(orient="records", force_ascii=False, indent=4)

    with open(caminho_arquivo, 'w', encoding='UTF-8') as arquivo_json:
        arquivo_json.write(json_str)

    # Carregando e modificando os dados
    with open(caminho_arquivo, 'r', encoding='UTF-8') as arquivo_json:
        dados = json.load(arquivo_json)

    for item in dados:
        if item is not None:
            if 'Unidade. 1' in item and item['Unidade. 1'] is not None:
                item['Unidade. 1'] = item['Unidade. 1'] / 10
            if 'Unidade. 2' in item and item['Unidade. 2'] is not None:
                item['Unidade. 2'] = item['Unidade. 2'] / 10
            if 'Unidade. 3' in item and item['Unidade. 3'] is not None:
                item['Unidade. 3'] = item['Unidade. 3'] / 10
            if 'Resultado' in item and item['Resultado'] not in (None, "--"):
                try:
                    item['Resultado'] = float(item['Resultado']) / 10
                except ValueError:
                    pass

    # Salvando as alterações com indentação
    with open(caminho_arquivo, 'w', encoding='UTF-8') as arquivo_alterado:
        json.dump(dados, arquivo_alterado, ensure_ascii=False, indent=4)

finally:
    navegador.quit()
