# automação para recarregar a página do SUAP automaticamente a cada 30 segundos
# e notificar quando tem um novo chamado

# print(pyautogui.position()) - posição do mouse
# print(pyautogui.size()) - verificar o tamanho da tela no computador
# pyautogui.click() - clicar
# time.sleep(5) - esperar 5 segundos antes de clicar
# pyautogui.press('f5')

# x=1467, y=427 - medidas para a barra de login no meu computador no ifac
# x=1473, y=512 - medidas para a barra de senha no meu computador no ifac
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui

pyautogui.PAUSE = 0.05

navegador = webdriver.Chrome() # conexão com o navegador - abre o navegador e já fecha

# acessar um site:
navegador.get("https://suap.ifac.edu.br")

#colocar o navegador em tela cheia 
navegador.maximize_window()

# aguardar até o campo de usuário estar visível
wait = WebDriverWait(navegador, 10)

inputUsuario = wait.until(EC.presence_of_element_located((By.ID, "id_username"))) 

inputUsuario.send_keys("3466829")

inputSenha = navegador.find_element(By.ID, "id_password")
inputSenha.send_keys("221205#Lua")

# aguardar até o botão "Acessar" estar clicável
btAcessar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.success")))
btAcessar.click()

time.sleep(230)


