# Django Application Setup Guide

Este guia descreve os passos necessários para configurar e rodar a aplicação Django.

## Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas em seu ambiente:

- [Python 3.8+](https://www.python.org/downloads/)
- [pip (Python package manager)](https://pip.pypa.io/en/stable/installation/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [Git](https://git-scm.com/)

## Passo a passo

### 1. Criar e ativar o ambiente virtual

Crie um ambiente virtual para garantir que as dependências da sua aplicação sejam isoladas:

```bash
# Crie o ambiente virtual
python3 -m venv env

# Ative o ambiente virtual
# No Windows:
env\Scripts\activate

# No macOS/Linux:
source env/bin/activate
```

### 2. Instalar as dependências do projeto

Com o ambiente virtual ativado, instale todas as dependências listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Configurar as variáveis de ambiente

Use o arquivo `.env.example` como base para configurar suas variáveis de ambiente. Faça uma cópia dele e renomeie para `.env`, ajustando os valores conforme necessário:

```bash
cp .env.example .env
```

Dentro do arquivo `.env`, configure os valores adequados para o banco de dados e outras variáveis necessárias.


### 4. Configurar o banco de dados

#### 4.1. Migrar as tabelas existentes para o banco de dados

Com o ambiente virtual ativado e as configurações ajustadas no arquivo `.env`, você precisará aplicar as migrações para criar as tabelas no banco de dados.

Primeiro, aplique as migrações já existentes:

```bash
python manage.py migrate
```

#### 4.2. Fazer migrações do modelo atual

Se houver alguma alteração no modelo de dados, crie novas migrações:

```bash
python manage.py makemigrations
```

Depois, aplique essas novas migrações com o comando:

```bash
python manage.py migrate
```

### 5. Executar o servidor de desenvolvimento

Agora que o banco de dados está configurado, você pode iniciar o servidor de desenvolvimento:

```bash
python manage.py runserver
```

O servidor estará rodando por padrão no endereço [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### 6. Criar superusuário (opcional)

Se precisar acessar o painel administrativo do Django, crie um superusuário com o comando:

```bash
python manage.py createsuperuser
```