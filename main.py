# importações
import requests
from pypdf import PdfReader
import os
import time


# Pegar todos arquivos PDF's dentro da pasta e inserir na lista de arquivos PFD's
lista_nomes = []
lista_numeros = []
lista_pdfs = []
caminho = os.getcwd()
# Esse for percorre a lista de arquivos no diretório do executável
for arq in os.listdir(caminho):
    # O if verifica se o arquivo é PDF, se for adiciona na lista de PDF's
    if arq.lower().endswith(".pdf"):
        lista_pdfs.append(arq)


# Extrair Nome e Telefone para o dicionário de candidatos
#inicializando a varíavel nome que é utilizada para guardar o nome do candidato
nome = ""
# Esse for percorre a lista de arquivos PDF's
for pdf in lista_pdfs:
    #lê o arquivo PDF
    reader = PdfReader(pdf)
    #pega o número de páginas do arquivo pdf
    number_pages = len(reader.pages)
    # Esse for percorre as páginas do arquivo
    for i in range(number_pages):
        # Lê a página atual e extrai as informações para variável texto
        pagina = reader.pages[i]
        texto = pagina.extract_text()
        """Se dentro da das informações for encontrada a palavra Telefone(s):
        # significa que temos telefone para extrair, então a extração acontece"""
        if texto.find("Telefone(s):") != -1:
            pos = texto.find("Telefone(s):")
            lista_numeros.append(texto[pos + 13:pos + 28])
        """o mesmo processo para extrair o telefone, porém agora para pegar o nome do candidato
        o que temos a mais nesse caso é a extração apenas do primeiro nome, então ele verificar o nome
        letra por letra e quando encontra o espaço para o for"""
        if texto.find("Nome:") != -1:
            pos = texto.find("Nome:")
            for letra in texto[pos + 5:pos + 50]:
                if letra != " ":
                    nome += letra
                else:
                    break
            lista_nomes.append(nome)
        nome = ""

"""Esse for foi utilizado, pois estávamos utilizando uma integração com o BotConversa
Então após extrair os candidatos já cadastramos eles no BotConversa e já estava tudo pronto
para entrar em contato com eles"""
for i, candidato in enumerate(lista_nomes):
    caminho = "LinkdoSeuWebhook"
    requisicao =  requests.post(caminho, data={"Nome": candidato, "Telefone": lista_numeros[i]})
    time.sleep(15)