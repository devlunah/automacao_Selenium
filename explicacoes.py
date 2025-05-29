#conteudos aprendidos:

#PYAUTOGUI
# print(pyautogui.position()) - posição do mouse
# print(pyautogui.size()) - verificar o tamanho da tela no computador
# pyautogui.click() - clicar
# time.sleep(5) - esperar 5 segundos antes de clicar
# pyautogui.press('f5')
#pyautogui.PAUSE = 0.05


#SELENIUM
#colocar o navegador em tela cheia - navegador.maximize_window()
#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service

# Caminho para o ChromeDriver
#service = Service(executable_path="./chromedriver.exe")

# Opções padrão para automação segura
#options = webdriver.ChromeOptions()

# === PERFIL OPCIONAL ===
# Use apenas um dos dois blocos abaixo:

# 1. Para rodar com perfil isolado (limpo):
# options.add_argument(r"user-data-dir=C:\SeleniumProfiles\PerfilAutomacao")

# 2. Para rodar com Chrome "zerado" (sem histórico, extensões, cache, etc.)
#options.add_argument("--incognito")

# === ESTABILIDADE ===
#options.add_argument("--start-maximized")
#options.add_argument("--disable-extensions")
#options.add_argument("--disable-gpu")
#options.add_argument("--no-sandbox")
#options.add_argument("--disable-dev-shm-usage")
#options.add_argument("--disable-blink-features=AutomationControlled")  # esconde que é automação
#options.add_experimental_option("excludeSwitches", ["enable-automation"])
#options.add_experimental_option('useAutomationExtension', False)

# === INICIALIZA ===
#driver = webdriver.Chrome(service=service, options=options)
#driver.get("https://link")

#--disable-blink-features=AutomationControlled: ajuda a esconder que é o Selenium (alguns sites detectam).

#excludeSwitches: remove a mensagem "Chrome está sendo controlado por um software de teste automatizado".

#useAutomationExtension: desativa a extensão Selenium interna, que também pode denunciar a automação.