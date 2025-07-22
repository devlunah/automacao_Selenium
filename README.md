# 🛠️ Automação SUAP - Gerenciamento de Chamados

Este projeto realiza uma automação com **Python + Selenium + Flask**, que acessa o SUAP - sistema do IFAC -, realiza login automático e monitora continuamente a Central de Chamados a cada 30 segundos. Quando um novo chamado é detectado, o sistema emite uma **notificação no Windows** com som e botão de ação.

Ao clicar no botão, o navegador é redirecionado ao SUAP via um servidor Flask local, e o clique também é detectado pelo Python.

---

## 🚀 Funcionalidades

- Login automático no SUAP
- Navegação até a Central de Chamados
- Verificação periódica por novos chamados
- Notificações sonoras e visuais no Windows
- Detecção de cliques via servidor Flask
- Encerramento seguro pressionando `Enter`

---

## ⚙️ Requisitos

- Python 3.8+
- Google Chrome instalado
- ChromeDriver compatível com a versão do navegador

---

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/devlunah/automacaoSUAP.git
cd automacaoSUAP
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` com suas credenciais:
```
SUAP_USUARIO=seu_usuario
SUAP_SENHA=sua_senha
```

---

## ▶️ Execução

```bash
python automacao.py
```

---

## 📝 Licença

Distribuído sob a licença MIT.
