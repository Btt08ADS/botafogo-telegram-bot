import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time

# === CONFIGURAÇÕES === #
TOKEN = '7729205757:AAE_gT-Q5VyoiTaUgwOqSuqbrE-b6h1Uo40'  
CANAL_ID = '@BotaESPN Tudo a Ver'     

URL = 'https://www.espn.com.br/futebol/time/_/id/345/botafogo'  # Página da ESPN do Botafogo
ULTIMA_NOTICIA = ''  

# Criação do bot com o token
bot = Bot(token=TOKEN)

def buscar_noticia():
    global ULTIMA_NOTICIA

    # Acessa a página da ESPN
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Pega todos os links da página
    noticias = soup.find_all('a', href=True)

    for link in noticias:
        titulo = link.get_text(strip=True)
        url = link['href']

        # Filtra notícias que mencionam Botafogo, são novas e não estão vazias
        if 'botafogo' in titulo.lower() and titulo != '' and titulo != ULTIMA_NOTICIA:
            # Completa o link se estiver incompleto
            if not url.startswith('http'):
                url = 'https://www.espn.com.br' + url

            mensagem = f'📰 {titulo}\n🔗 {url}'

            # Envia a mensagem para o canal
            bot.send_message(chat_id=CANAL_ID, text=mensagem)

            # Atualiza a última notícia para evitar repetições
            ULTIMA_NOTICIA = titulo
            break  

# Loop infinito 
while True:
    try:
        buscar_noticia()
    except Exception as e:
        print(f"Erro: {e}")
    time.sleep(1200)