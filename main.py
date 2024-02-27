# Imports para o projeto
from selenium import webdriver
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


for linha in ler_planilha(nome_arq):
    print(linha)

#Nomeando o driver do Chrome para utilização no código
nav = webdriver.Chrome()

#Navegando até o site do Mercado livre
nav.get("https://mercadolivre.com.br")

# Esperando alguns segundos para a página carregar completamente
time.sleep(2)

#Saindo do navegador
nav.quit()