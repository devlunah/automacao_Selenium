# automação para recarregar a página do SUAP automaticamente a cada 30 segundos
# e notificar quando tem um novo chamado

# print(pyautogui.position()) - posição do mouse
# print(pyautogui.size()) - verificar o tamanho da tela no computador
# pyautogui.click() - clicar
# time.sleep(5) - esperar 5 segundos antes de clicar
# pyautogui.press('f5')

from selenium import webdriver
import time
import pyautogui

pyautogui.PAUSE = 0.05

navegador = webdriver.Chrome() # conexão com o navegador - abre o navegador e já fecha

# acessar um site:
navegador.get("https://suap.ifac.edu.br")

pyautogui.click(x=895, y=13)
time.sleep(3)
pyautogui.click(x=1467, y=427)
pyautogui.write("3466829")

time.sleep(3)
pyautogui.click(x=1473, y=512)
pyautogui.write("221205#Lua")

pyautogui.press("enter")

time.sleep(20)
