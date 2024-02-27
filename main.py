# Imports para o projeto
from selenium import webdriver
import time

#Nomeando o driver do Chrome para utilização no código
nav = webdriver.Chrome()

#Navegando até o site do Mercado livre
nav.get("https://mercadolivre.com.br")

# Esperando alguns segundos para a página carregar completamente
time.sleep(2)

#Saindo do navegador
nav.quit()