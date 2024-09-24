
# PSQI-IA-integrada

Teste PSQI, com avaliação gerada por IA Gemini

A aplicação web foi desenvolvida em Python, utilizando o Django e integrando a API de IA do Google Gemini e Plotly.

A aplicação é simples e possui uma home page com explicação simples sobre o teste e sua utilidade, login, registro de usuário;
Realização de teste com formulário padrão, após o envio do teste o usuário é redirecionado para a visualização das notas,
as notas são calculadas pelas respostas fornecidas, com base no modelo de avaliação padrão, divididas em componentes,
cada componente faz o cálculo de campos pré-determinados para gerar a pontuação de cada componente e sobre este cálculo
é feito o cálculo da pontuação global.

Após a pontuação global, entra a API de IA do Gemini, ela verifica as notas, e gera uma avaliação levando em conta cada nota
e seu impacto na nota geral e retorna recomendações para o paciente.

Há também endereço de visualização do histórico de testes com gráfico gerado utilizando Plotly, para acompanhamento de evolução.

## Etiquetas
![Static Badge](https://img.shields.io/badge/License-MIT-yellow?style=flat)
![Static Badge](https://img.shields.io/badge/Framework-Django-green?style=flat)
![Static Badge](https://img.shields.io/badge/Language-Python-blue?style=flat)
![Static Badge](https://img.shields.io/badge/IA-Gemini-purple?style=flat)

<h4 align="center"> 
    :construction:  Projeto em construção  :construction:
</h4>

## Stack utilizada

O projeto foi desenvolvido utilizando as seguintes Stacks:

**Front-end:** HTML, CSS, JavaScript

**Back-end:** Python v2024.14.1, Django v5.1.1

**IA:** Google Gemini API v0.6.9

## Features

- [x] Cadastro de usuário
- [x] Questionário de teste
- [x] Lista de testes com visualização de histórico das notas de avaliação
- [X] Detalhe de avaliação de teste realizado

## Instalação via download ZIP

Após descompactar o arquivo ZIP no local desejado
<p>1- Abra seu editor</p>
<p>2- Vá em arquivo</p>
<p>3- Abrir pasta</p>
<p>4- Escolha a pasta do projeto (PSQI-IA-integrada)</p>
<p>5- Crie seu ambiente virtual utilizando o comando:<br>
    python -m venv "nome do ambiente de sua escolha"</p>
<p>6- Acesse seu ambiente virtual criado através do comando:<br>
    .\"nome do ambiente de sua escolha"\Scripts\activate<br>
Você verá que o seu terminal ficara com o nome do seu ambiente entre parênteses e na cor verde, à esquerda do endereço do seu terminal.</p>
<p>7- Instale as dependencias através do comando:<br>
    pip install -r requirements.txt</p>
<p>8- Após o final da instalação, para rodar a aplicação será necessário executar o comando:<br>
    python manage.py runserver</p>

## Instalação via clonagem

Para rodar esse projeto, você vai precisar ter instalado em sua máquina as seguintes ferramentas:
[Git](https://git-scm.com)

Além disto é bom ter um editor para trabalhar com o código como [VSCode](https://code.visualstudio.com/)

<p>1- Abra o Git Bash</p>
<p>2- Altere o diretório de trabalho atual para o local do diretório desejado</p>
<p>3- Digite git clone https://github.com/JG-Erbes-dev/PSQI-IA-integrada.git</p>
<p>4- Aperte ENTER e aguarde o final da clonagem</p>
<p>5- Siga os passos da instalação via download ZIP</p>


## Ajustando integração da IA:

Será necessário gerar uma `API_KEY` do Google Gemini AI, e inserir no arquivo client.py, localizado na pasta gemini_api para gerar as avaliações.

O código também poderá ser utilizado com integração da API Openai.
