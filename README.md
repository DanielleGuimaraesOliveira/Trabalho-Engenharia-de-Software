# Trabalho Engenharia de Software

## Tecnologias

* Python 3.12
* Flask
* SQLAlchemy
* SQLite
* HTML, CSS e JavaScript

---

# Como rodar o projeto

## 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
```

---

## 2. Entrar na pasta do servidor

```bash
cd server
```

---

## 3. Criar ambiente virtual

### Linux / MacOS

```bash
python3 -m venv venv
```

### Windows

```bash
python -m venv venv
```

---

## 4. Ativar ambiente virtual

### Linux / MacOS

```bash
source venv/bin/activate
```

### Windows (CMD)

```bash
venv\Scripts\activate
```

### Windows (PowerShell)

```bash
venv\Scripts\Activate.ps1
```

---

## 5. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 6. Executar a API

```bash
python -m src.app.main
```

Ao iniciar a aplicação pela primeira vez, o SQLAlchemy criará automaticamente as tabelas do banco de dados.

A API ficará disponível em:

```text
http://localhost:5000
```

ou, em um Codespace:

```text
https://<nome-do-codespace>-5000.app.github.dev
```

---

## 7. Executar o Frontend

Abra um novo terminal e entre na pasta do frontend:

```bash
cd client
```

### Utilizando a extensão Live Server (VS Code)

Clique com o botão direito em `index.html` e selecione:

```text
Open with Live Server
```

### Utilizando Python

```bash
python -m http.server 5500
```

O frontend ficará disponível em:

```text
http://localhost:5500
```

ou, em um Codespace:

```text
https://<nome-do-codespace>-5500.app.github.dev
```

---

