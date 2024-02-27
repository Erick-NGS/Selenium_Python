from selenium import webdriver
import time


nav = webdriver.Chrome()

nav.get("https://mercadolivre.com.br")

# Esperando alguns segundos para a página carregar completamente
time.sleep(2)

# Exibindo o título da página para verificar se a navegação foi bem-sucedida
print("Título da página:", nav.title)

nav.quit()