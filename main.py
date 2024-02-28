# Imports para o projeto
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import openpyxl

def ler_planilha(nome_arq):
    wb = openpyxl.load_workbook(nome_arq)

    planilha = wb.active

    items = []

    for linha in planilha.iter_rows(values_only=True):
        items.append(linha)

    return items

nome_arq = "Lista.xlsx"


# for linha in ler_planilha(nome_arq):
#     print(linha)

#Nomeando o driver do Chrome para utilização no código
nav = webdriver.Chrome()

#Navegando até o site do Mercado livre
nav.get("https://mercadolivre.com.br")

# Esperando alguns segundos para a página carregar completamente
time.sleep(3)

for item in ler_planilha(nome_arq):
    campo_de_busca = nav.find_element(By.TAG_NAME, "INPUT")
    campo_de_busca.send_keys(item)
    campo_de_busca.send_keys(Keys.ENTER)
    time.sleep(5)

    nome_produto = nav.find_element(By.XPATH, "//*[@id=*]/div[2]/div/div[2]/a")
    print(nome_produto.text)
    time.sleep(5)


    campo_de_busca = nav.find_element(By.TAG_NAME, "INPUT")
    campo_de_busca.send_keys(Keys.CONTROL + "a")
    campo_de_busca.send_keys(Keys.DELETE)
    time.sleep(3)

#Saindo do navegador
nav.quit()