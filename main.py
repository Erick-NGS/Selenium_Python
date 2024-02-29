# Imports para o projeto
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import time
from utils.funcs.ler_lista import ler_planilha
from utils.funcs.escrever_report import criar_tabela
from utils.funcs.envio_email import enviar_email

nome_arq = "Lista.xlsx"

ler_planilha(nome_arq)

lista_item = []
lista_preco = []
lista_link = []
lista_orcamento = []

msg_erro_pesquisa = "Produto não encontrado!"
msg_erro = "Erro ao pesquisar item!"


# for linha in ler_planilha(nome_arq):
#     print(linha)

#Nomeando o driver do Chrome para utilização no código
nav = webdriver.Chrome()

#Navegando até o site do Mercado livre
try:
    nav.get("https://mercadolivre.com.br")

    # Esperando alguns segundos para a página carregar completamente
    time.sleep(3)

except Exception as erro_navegar:
    print(f"Erro ao navegar a página do site: {erro_navegar}")

# Iterando por cada item da lista de produtos a serem pesquisados
for item in ler_planilha(nome_arq):
    # Fazendo a pesquisa do produto
    campo_de_busca = nav.find_element(By.TAG_NAME, "INPUT")
    campo_de_busca.send_keys(item)
    campo_de_busca.send_keys(Keys.ENTER)
    time.sleep(5)

    try:
        # Buscando o primeiro item na query de resultados de pesquisa de produto
        # nome_produto = nav.find_element(By.XPATH, "//*[@*]/div[2]/div/div[*]/a")
        nome_produto = nav.find_element(By.CSS_SELECTOR, "a[class='ui-search-item__group__element ui-search-link__title-card ui-search-link']")
        # print(nome_produto.text)
        lista_item.append(nome_produto.text)

        # Acessando a página do produto
        nome_produto.click()
        time.sleep(5)

    except NoSuchElementException as err:
        try:
            pesquisa_erro = nav.find_element(By.CSS_SELECTOR, "h3[class='ui-search-rescue__title']")
            print(f"Item {item} não encontrado.")
            lista_item.append(str(item).replace("(", "").replace(")", "").replace(",", ""))
            lista_preco.append(msg_erro_pesquisa)
            lista_link.append(msg_erro_pesquisa)
            continue

        except NoSuchElementException as err:
            print(f"Erro ao pesquisar item {item}.\nErro: {err}.")
            lista_item.append(str(item).replace("(", "").replace(")", "").replace(",", ""))
            lista_preco.append(msg_erro)
            lista_link.append(msg_erro)
            continue

    # Após o acesso a página, buscando o valor do item pesquisado
    # preco_produto = nav.find_element(By.XPATH, "//*[@*]/div[2]/div/div[2]/div/div/div/span[1]")
    preco_produto = nav.find_element(By.XPATH, "//meta[@itemprop='price']").get_attribute("content")
    # print(preco_produto)
    lista_preco.append(preco_produto)
    time.sleep(3)

    link_produto = nav.current_url
    lista_link.append(link_produto)

    # Limpando o campo de pesquisa de produtos
    campo_de_busca = nav.find_element(By.TAG_NAME, "INPUT")
    campo_de_busca.send_keys(Keys.CONTROL + "a")
    campo_de_busca.send_keys(Keys.DELETE)
    time.sleep(3)

orcamento = 0
for preco in lista_preco:
    if preco == msg_erro_pesquisa or preco == msg_erro:
        preco = 0
    orcamento += float(preco)

lista_orcamento.append(round(orcamento, 2))

# print(lista_item)
# print(lista_preco)
# print(lista_link)
# print(lista_orcamento)

#Saindo do navegador
nav.quit()

try:
    criar_tabela(lista_item, lista_preco, lista_link, lista_orcamento)
except Exception as err:
    print (f"Erro ao compor relatório: {err}")

try:
    enviar_email()
except Exception as err:
    print (f"Erro no envio de email do relatório: {err}")