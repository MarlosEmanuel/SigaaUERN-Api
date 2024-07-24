from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge import options
from bs4 import BeautifulSoup
import pandas as pd
import time
from io import StringIO
import json
navegador = webdriver.Edge()



usuario = "NOME DO SEU USUARIO"
senha = "SUA SENHA"



navegador.get("https://sigaa.uern.br/sigaa/verTelaLogin.do")

navegador.find_element('xpath','//*[@id="conteudo"]/div[4]/form/table/tbody/tr[1]/td/input').send_keys(usuario)
navegador.find_element('xpath','//*[@id="conteudo"]/div[4]/form/table/tbody/tr[2]/td/input').send_keys(senha)
time.sleep(1)
navegador.find_element('xpath','//*[@id="conteudo"]/div[4]/form/table/tfoot/tr/td/input').click()
time.sleep(1)
navegador.find_element('xpath','//*[@id="menu_form_menu_discente_j_id_jsp_340461267_98_menu"]/table/tbody/tr/td[1]').click()
time.sleep(1)
navegador.find_element('xpath','//*[@id="cmSubMenuID1"]/table/tbody/tr[1]/td[2]').click()
time.sleep(1)

#Trabalhando com Tabela
tableTicket = navegador.find_element('xpath','//*[@id="relatorio"]/div/table[1]')
htmlContent = tableTicket.get_attribute("outerHTML") #Pegando todo o html da tabela 2024.1
soup = BeautifulSoup(htmlContent,"html.parser")

tickets = soup.find(name="table")
sio = StringIO(str(tickets))
df = pd.read_html(sio)[0]

df.to_json(f"tabela_{usuario}.json", orient="records", force_ascii=False)

with open(f'tabela_{usuario}.json','r',encoding='UTF-8') as arquivo_json:
    dados = json.load(arquivo_json)

for item in dados:
    if item is not None:
        if 'Unidade. 1' in item and item['Unidade. 1'] is not None:
            item['Unidade. 1'] = item['Unidade. 1'] / 10
        if 'Unidade. 2' in item and item['Unidade. 2'] is not None:
            item['Unidade. 2'] = item['Unidade. 2'] / 10
        if 'Unidade. 3' in item and item['Unidade. 3'] is not None:
            item['Unidade. 3'] = item['Unidade. 3'] / 10

with open(f'tabela_{usuario}.json','w',encoding='UTF-8') as arquivo_alterado:
    json.dump(dados, arquivo_alterado, ensure_ascii=False, indent=4)