
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

## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar instalar o requirements.txt no seu .env utilizando o comando:

pip install -r requirements.txt


Você vai precisar gerar uma `API_KEY` do Google Gemini AI, e inserir em client.py, para gerar as avaliações.

Poderá também utilizar com integração da API Openai.


## Stack utilizada

**Front-end:** HTML, CSS, JavaScript

**Back-end:** Python, Django

