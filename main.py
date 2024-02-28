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
lista_itens = []
lista_preco = []
lista_link = []
lista_orcamento = []


# for linha in ler_planilha(nome_arq):
#     print(linha)

#Nomeando o driver do Chrome para utilização no código
nav = webdriver.Chrome()

#Navegando até o site do Mercado livre
nav.get("https://mercadolivre.com.br")

# Esperando alguns segundos para a página carregar completamente
time.sleep(3)

# Iterando por cada item da lista de produtos a serem pesquisados
for item in ler_planilha(nome_arq):
    # Fazendo a pesquisa do produto
    campo_de_busca = nav.find_element(By.TAG_NAME, "INPUT")
    campo_de_busca.send_keys(item)
    campo_de_busca.send_keys(Keys.ENTER)
    time.sleep(5)

    # Buscando o primeiro item na query de resultados de pesquisa de produto
    # nome_produto = nav.find_element(By.XPATH, "//*[@*]/div[2]/div/div[*]/a")
    nome_produto = nav.find_element(By.CSS_SELECTOR, "a[class='ui-search-item__group__element ui-search-link__title-card ui-search-link']")
    # print(nome_produto.text)
    lista_itens.append(nome_produto.text)

    # Acessando a página do produto
    nome_produto.click()
    time.sleep(5)

    # Após o acesso a página, buscando o valor do item pesquisado
    # preco_produto = nav.find_element(By.XPATH, "//*[@*]/div[2]/div/div[2]/div/div/div/span[1]")
    preco_produto = nav.find_element(By.XPATH, "//meta[@itemprop='price']").get_attribute("content")
    # print(preco_produto)
    lista_preco.append(preco_produto)
    time.sleep(5)

    link_produto = nav.current_url
    lista_link.append(link_produto)

    # Limpando o campo de pesquisa de produtos
    campo_de_busca = nav.find_element(By.TAG_NAME, "INPUT")
    campo_de_busca.send_keys(Keys.CONTROL + "a")
    campo_de_busca.send_keys(Keys.DELETE)
    time.sleep(3)

orcamento = 0
for preco in lista_preco:
    orcamento += float(preco)

lista_orcamento.append(round(orcamento, 2))

# print(lista_itens)
# print(lista_preco)
# print(lista_link)
# print(lista_orcamento)

#Saindo do navegador
nav.quit()