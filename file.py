# automação para recarregar a página do SUAP automaticamente a cada 30 segundos
# e notificar quando tem um novo chamado

# x=1467, y=427 - medidas para a barra de login no meu computador no ifac
# x=1473, y=512 - medidas para a barra de senha no meu computador no ifac

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # função para fazer o navegador aguardar algo
from selenium.webdriver.support import expected_conditions as EC # função para determinar qual a condição esperada para que o navegador aguarde antes de fazer algo
from selenium.webdriver.chrome.service import Service #importa a classe Service da biblioteca do Selenium, usada para configurar como o ChromeDriver (o executável que controla o navegador Google Chrome) será inicializado.
import time
import pyautogui
import os
from dotenv import load_dotenv

load_dotenv("config.env")

usuario = os.environ["SUAP_USUARIO"]
senha = os.environ["SUAP_SENHA"]

if not usuario or not senha:
    raise ValueError("Usuário ou senha não definidos nas variáveis de ambiente.")

# conexão com o navegador - abre o navegador e já fecha

service = Service(executable_path='./chromedriver.exe') #esse arquivo é o driver que o Selenium usa para "conversar" com o navegador Google Chrome.

#esse trecho cria um objeto ChromeOptions, que permite configurar o navegador Chrome antes de abri-lo.
options = webdriver.ChromeOptions() 

#definir usuário para abrir o navegador
options.add_argument(r"user-data-dir=C:\SeleniumProfiles\Profile_Clone_Automacao")
options.add_argument("--disable-extensions") #Desativa todas as extensões do Chrome (como AdBlock, LastPass, etc.)
options.add_argument("--disable-gpu") #Desativa o uso da GPU (placa de vídeo) para aceleração gráfica no Chrome.
options.add_argument("--no-sandbox") #Desativa o "sandboxing" do Chrome (isolamento de processos por segurança).
options.add_argument("--disable-dev-shm-usage") #Evita que o Chrome use a pasta /dev/shm (shared memory) para armazenar dados temporários.

options.add_argument("--start-maximized")

#Essa é a linha que realmente inicializa o navegador Chrome com o Selenium. 
# Usa o chromedriver.exe configurado no Service;
# Aplica todas as options configuradas;
navegador = webdriver.Chrome(service=service, options=options) 

#definição da variável de tempo de espera
wait = WebDriverWait(navegador, 10)

try:
    # acessar um site:
    navegador.get("https://suap.ifac.edu.br")

    btSair = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.menu-logout")))
    btSair.click()

    # aguardar até o campo de usuário estar visível -> wait.until(EC.presence_of_element_located())
    inputUsuario = wait.until(EC.presence_of_element_located((By.ID, "id_username"))) 
    inputUsuario.send_keys(usuario)

    inputSenha = navegador.find_element(By.ID, "id_password")
    inputSenha.send_keys(senha)

    # aguardar até o botão "Acessar" estar clicável
    btAcessar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.success")))
    btAcessar.click()

    tempo2 = WebDriverWait(navegador, 10)
    menuPrincipal = tempo2.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul._main_menu")))
    menuChamados = tempo2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.menu-central-de-servicos")))
    menuChamados.click()

    acessoChamados= tempo2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#menu-item-centraldeserviços_chamados")))
    acessoChamados.click()

    input("Pressione Enter para encerrar...")

except:
    print("Erro durante a automação:")
    input("Pressione Enter para sair...")

finally:

    navegador.quit()
