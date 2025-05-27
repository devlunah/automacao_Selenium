# automação para recarregar a página do SUAP automaticamente a cada 30 segundos
# e notificar quando tem um novo chamado

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # função para fazer o navegador aguardar algo
from selenium.webdriver.support import expected_conditions as EC # função para determinar qual a condição esperada para que o navegador aguarde antes de fazer algo
from selenium.webdriver.chrome.service import Service #importa a classe Service da biblioteca do Selenium, usada para configurar como o ChromeDriver (o executável que controla o navegador Google Chrome) será inicializado.
from dotenv import load_dotenv
from winotify import Notification, audio
import time
import os
import threading
import re

load_dotenv("config.env")

usuario = os.environ["SUAP_USUARIO"]
senha = os.environ["SUAP_SENHA"]

if not usuario or not senha:
    raise ValueError("Usuário ou senha não definidos nas variáveis de ambiente.")



service = Service(executable_path='./chromedriver.exe') #esse arquivo é o driver que o Selenium usa para "conversar" com o navegador Google Chrome.

#esse trecho cria um objeto ChromeOptions, que permite configurar o navegador Chrome antes de abri-lo.
options = webdriver.ChromeOptions() 

#definir usuário para abrir o navegador
options.add_argument(r"user-data-dir=C:/SeleniumProfiles/UserData_Clone")
options.add_argument("profile-directory=Default")
options.add_argument("--disable-extensions") #Desativa todas as extensões do Chrome (como AdBlock, LastPass, etc.)
options.add_argument("--disable-gpu") #Desativa o uso da GPU (placa de vídeo) para aceleração gráfica no Chrome.
options.add_argument("--no-sandbox") #Desativa o "sandboxing" do Chrome (isolamento de processos por segurança).
options.add_argument("--disable-dev-shm-usage") #Evita que o Chrome use a pasta /dev/shm (shared memory) para armazenar dados temporários.

# Não exibe o Navegador
options.add_argument("--headless=new")  # novo modo headless do Chrome 109+
options.add_argument("--window-size=1920,1080")  # evita erros de resolução

# Exibe o Navegador
# options.add_argument("--start-maximized")

#Essa é a linha que realmente inicializa o navegador Chrome com o Selenium. 
# Usa o chromedriver.exe configurado no Service;
# Aplica todas as options configuradas;
navegador = webdriver.Chrome(service=service, options=options) 

#definição da variável de tempo de espera
wait = WebDriverWait(navegador, 10)

parar = False

def finalizar_Enter():
    global parar
    while not parar:
        time.sleep(1)
    print("Thread finalizada.")

t = threading.Thread(target=finalizar_Enter).start()

try:
    # acessar um site:
    navegador.get("https://suap.ifac.edu.br") # conexão com o navegador - abre o navegador e já fecha

    #btSair = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.menu-logout")))
    #btSair.click()

    # aguardar até o campo de usuário estar visível -> wait.until(EC.presence_of_element_located())
    inputUsuario = wait.until(EC.presence_of_element_located((By.ID, "id_username"))) 
    inputUsuario.send_keys(usuario)

    inputSenha = navegador.find_element(By.ID, "id_password")
    inputSenha.send_keys(senha)

    #aguardar até o botão "Acessar" estar clicável
    btAcessar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.success")))
    btAcessar.click()

    tempo2 = WebDriverWait(navegador, 10)
    menuPrincipal = tempo2.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul._main_menu")))
    menuChamados = tempo2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.menu-central-de-servicos")))
    menuChamados.click()

    acessoChamados= tempo2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#menu-item-centraldeserviços_chamados")))
    acessoChamados.click()
    x_path_total_chamados = ''

    #atualização da página e checar se há novo chamado
    elemento_total = navegador.find_element(By.XPATH, "//li[@class='disabled' and contains(text(),'Total de')]")
    texto_anterior = elemento_total.text.strip()
    print(f"texto_anterior = {texto_anterior}")

    numeroAnt = re.search(r'\d+', texto_anterior)

    numero_anterior = None
    if numeroAnt:
        numero_anterior = int(numeroAnt.group())


    print(numero_anterior)
    
    while True:
        time.sleep(120)
        navegador.refresh()
        time.sleep(2)  # espera rápida para o site recarregar

        elemento_total = tempo2.until(EC.presence_of_element_located((By.XPATH, "//li[@class='disabled' and contains(text(),'Total de')]")))
        texto_atual = elemento_total.text.strip()


        
        numeroAtual = re.search(r'\d+', texto_atual)
        numero_atual = None
        if numeroAtual:
            numero_atual = int(numeroAtual.group())

        print(f"numero_atual = {numero_atual}")

        if numero_anterior and numero_atual and numero_atual != numero_anterior:
            toast = Notification(app_id="SUAP",
                                title="Novo chamado detectado!",
                                msg="Verifique o SUAP agora.")  
            toast.set_audio(audio.Default, loop=False)
            toast.show()
            #print(f"Novo chamado detectado! Anterior: {texto_anterior} → Atual: {texto_atual}")
            texto_anterior = texto_atual 

        else:
            toast = Notification(app_id="SUAP",
                                title="Nada novo :)",
                                msg="Nenhum novo chamado foi localizado!")  
            toast.set_audio(audio.Default, loop=False)
            toast.show()
            texto_anterior = texto_atual 
            #print("Nenhum novo chamado.")

except KeyboardInterrupt:
    print("Finalizando o programa...")
    parar = True
    
except Exception as e:
    print(f"Erro durante a automação: {e}")
    input("Pressione Enter para sair...")
    parar = True

finally:
    btSair = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.menu-logout")))
    btSair.click()
    navegador.quit()
