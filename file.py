# automação para recarregar a página do SUAP automaticamente a cada 2 minutos
# e notificar quando tem um novo chamado

# bibliotecas:
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.chrome.service import Service 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
from winotify import Notification, audio
from flask import Flask, redirect
import threading
import time
import os
import re

# importação do usuário e senha definido no arquivo .env
load_dotenv("config.env")

usuario = os.environ["SUAP_USUARIO"]
senha = os.environ["SUAP_SENHA"]

if not usuario or not senha:
    raise ValueError("Usuário ou senha não definidos nas variáveis de ambiente.")

# configurações do chromedriver 
service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions() 

options.add_argument(r"user-data-dir=C:/SeleniumProfiles/UserData_Clone")
options.add_argument("profile-directory=Default")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
#options.add_argument("--start-maximized")
navegador = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(navegador, 10)

# thread para finalizar com enter
parar = False
def finalizar_Enter():
    global parar
    while not parar:
        time.sleep(1)
    print("Thread finalizada.")

t = threading.Thread(target=finalizar_Enter).start()

# Flask App para capturar clique
app = Flask(__name__)
clique_na_notificacao = False

@app.route("/notificacao-clicada")
def notificacao_clicada():
    global clique_na_notificacao
    clique_na_notificacao = True
    print("🟢 O botão da notificação foi clicado!")
    return redirect("https://suap.ifac.edu.br/centralservicos/listar_chamados_suporte/")

def iniciar_flask():
    app.run(port=5000)

threading.Thread(target=iniciar_flask, daemon=True).start()

#inicio da automação
try:
    navegador.get("https://suap.ifac.edu.br")
    
    inputUsuario = wait.until(EC.presence_of_element_located((By.ID, "id_username"))) 
    inputUsuario.send_keys(usuario)
    inputSenha = navegador.find_element(By.ID, "id_password")
    inputSenha.send_keys(senha)

    btAcessar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.success")))
    btAcessar.click()

    tempo2 = WebDriverWait(navegador, 10)
    menuPrincipal = tempo2.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul._main_menu")))
    menuChamados = tempo2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.menu-central-de-servicos")))
    menuChamados.click()

    acessoChamados= tempo2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#menu-item-centraldeserviços_chamados")))
    acessoChamados.click()
    x_path_total_chamados = ''
    
    try:
        elemento_total = navegador.find_element(By.XPATH, "//li[@class='disabled' and contains(text(),'Total de')]")
        texto_anterior = elemento_total.text.strip()

    except NoSuchElementException:
        texto_anterior = "Total de 0 item"
        numero_anterior = 0

    print(f"texto_anterior = {texto_anterior}")

    numeroAnt = re.search(r'\d+', texto_anterior)

    numero_anterior = None
    if numeroAnt:
        numero_anterior = int(numeroAnt.group())
    print(numero_anterior)
    
    while True:
        time.sleep(30)
        navegador.refresh()
        time.sleep(2)  # espera rápida para o site recarregar

        try:
            elemento_total = tempo2.until(EC.presence_of_element_located((By.XPATH, "//li[@class='disabled' and contains(text(),'Total de')]")))
            texto_atual = elemento_total.text.strip()
        except TimeoutException:
            texto_atual = "Total de 0 item"
            numero_atual = 0
        
        numeroAtual = re.search(r'\d+', texto_atual)
        numero_atual = None
        if numeroAtual:
            numero_atual = int(numeroAtual.group())
        print(f"numero_atual = {numero_atual}")

        print(texto_atual)

        if numero_anterior is not None and numero_atual is not None and numero_atual != numero_anterior and numero_atual > numero_anterior:
            notificacao = Notification(app_id="SUAP",
                                title="Novo chamado detectado!",
                                msg="Verifique o SUAP agora.")  
            notificacao.set_audio(audio.Default, loop=False)
            notificacao.add_actions(label="Ir para SUAP", launch="http://localhost:5000/notificacao-clicada")
            notificacao.show()

            if clique_na_notificacao == True:
                texto_anterior = texto_atual 
                numero_anterior = numero_atual

        else:
            texto_anterior = texto_atual 
            numero_anterior = numero_atual

except KeyboardInterrupt:
    print("Finalizando o programa...")
    parar = True
    
except Exception as e:
    notificacao = Notification(app_id="Python",
                    title="Erro na automação",
                    msg="Verificar")  
    notificacao.set_audio(audio.Default, loop=False)
    notificacao.show()
    print(f"Erro durante a automação: {e}")
    input("Pressione Enter para sair...")
    parar = True

finally:
    btSair = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.menu-logout")))
    btSair.click()
    navegador.quit()

    #msg_semChamados = navegador.find_element(By.XPATH, "//*[@id='content']/div[5]/div/p") 
            # if msg_semChamados:
            #     print("Não há chamados")
            #     texto_anterior = "Total de 0 item"
            #     numero_anterior = 0
