# Imports para o projeto
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from utils.funcs.ler_lista import ler_planilha
from utils.funcs.escrever_report import criar_tabela
from utils.funcs.envio_email import enviar_email

# Nome de arquivo com lista de produtos a serem pesquisados
nome_arq = "Lista.xlsx"

ler_planilha(nome_arq)

lista_item = []
lista_preco = []
lista_link = []
lista_orcamento = []

msg_erro_pesquisa = "Produto não encontrado!"
msg_erro = "Erro ao pesquisar item!"


#Nomeando o driver do Chrome para utilização no código
nav = webdriver.Chrome()

#Navegando até o site do Mercado livre
try:
    nav.get("https://mercadolivre.com.br")

    # Esperando alguns segundos para a página carregar completamente
    time.sleep(3)

except Exception as erro_navegar:
    print(f"Erro ao navegar a página do site: {erro_navegar}")


try:
    lista_itens = ler_planilha(nome_arq)
    print(f"Lista de produtos lida com sucesso!\n")
except Exception as err:
    print(f"Erro ao ler lista de produtos a serem pesquisados: {err}")

# Iterando por cada item da lista de produtos a serem pesquisados
for item in lista_itens:
    # Formatando texto de item para log
    item_format = str(item).replace("(", "").replace(")", "").replace(",", "").replace("'", "")

    # Fazendo a pesquisa do produto
    campo_de_busca = nav.find_element(By.TAG_NAME, "INPUT")
    campo_de_busca.send_keys(item)
    campo_de_busca.send_keys(Keys.ENTER)
    time.sleep(5)

    try:
        # Buscando o primeiro item na query de resultados de pesquisa de produto
        nome_produto = nav.find_element(By.CSS_SELECTOR, "a[class='ui-search-item__group__element ui-search-link__title-card ui-search-link']")
        # print(nome_produto.text)
        lista_item.append(nome_produto.text)

        # Acessando a página do produto
        nome_produto.click()
        time.sleep(5)

    # Excceção caso item pesquisado não seja encontrado
    except NoSuchElementException as err:
        try:
            pesquisa_erro = nav.find_element(By.CSS_SELECTOR, "h3[class='ui-search-rescue__title']")
            print(f"Item {item_format} não encontrado!")
            lista_item.append(item_format)
            lista_preco.append(msg_erro_pesquisa)
            lista_link.append(msg_erro_pesquisa)
            print(f"Item - {item_format}\nPreço - {msg_erro_pesquisa}\n")
            continue
        # Excceção caso haja algum erro na pesquisa do item    
        except NoSuchElementException as err:
            print(f"Erro ao pesquisar item {item}.\nErro: {err}.")
            lista_item.append(item_format)
            lista_preco.append(msg_erro)
            lista_link.append(msg_erro)
            print(f"Item - {item_format}\nPreço - {msg_erro}\n")
            continue

    # Após o acesso a página, buscando o valor do item pesquisado
    preco_produto = nav.find_element(By.XPATH, "//meta[@itemprop='price']").get_attribute("content")
    lista_preco.append(preco_produto)
    time.sleep(3)

    link_produto = nav.current_url
    lista_link.append(link_produto)

    # Limpando o campo de pesquisa de produtos
    campo_de_busca = nav.find_element(By.TAG_NAME, "INPUT")
    campo_de_busca.send_keys(Keys.CONTROL + "a")
    campo_de_busca.send_keys(Keys.DELETE)
    time.sleep(3)

    print(f"Item - {item_format}\nPreço - R${preco_produto}\n")

orcamento = 0
for preco in lista_preco:
    if preco == msg_erro_pesquisa or preco == msg_erro:
        preco = 0
    orcamento += float(preco)

lista_orcamento.append(round(orcamento, 2))

print(f"Valor de orçamento previsto na lista - R${round(orcamento, 2)}\n")


#Saindo do navegador
nav.quit()

try:
    criar_tabela(lista_item, lista_preco, lista_link, lista_orcamento)
    print(f"Report criado e salvo com sucesso!")
except Exception as err:
    print (f"Erro ao compor relatório: {err}")

try:
    enviar_email()
    print(f"Email de relatório final enviado com sucesso!")
except Exception as err:
    print (f"Erro no envio de email do relatório: {err}")