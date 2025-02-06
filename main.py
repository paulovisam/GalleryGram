import os
import time
import configparser
from pyrogram import Client # type: ignore
from pyrogram.types import InputMediaPhoto, InputMediaVideo # type: ignore
from tqdm import tqdm # type: ignore
from halo import Halo # type: ignore
import pyfiglet # type: ignore
from banner import Banner
from log import logger

def get_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    api_id = config.get("pyrogram", "api_id")
    api_hash = config.get("pyrogram", "api_hash")
    return api_id, api_hash

def get_api_credentials():
    api_id = input("Digite o seu API_ID: ")
    api_hash = input("Digite o seu API_HASH: ")
    config = configparser.ConfigParser()
    config['pyrogram'] = {
        'api_id': api_id,
        'api_hash': api_hash
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    return api_id, api_hash

def carregar_arquivos_enviados():
    # Função para carregar os arquivos enviados previamente
    if os.path.exists(ARQUIVOS_ENVIADOS):
        with open(ARQUIVOS_ENVIADOS, "r", encoding="utf-8") as f:
            arquivos = f.read().splitlines()  # Carrega os nomes dos arquivos enviados
        return set(arquivos)  # Retorna como um conjunto para facilitar a busca
    return set()

def salvar_arquivo_enviado(arquivo):
    # Função para salvar os arquivos enviados
    with open(ARQUIVOS_ENVIADOS, "a", encoding="utf-8") as f:
        f.write(arquivo + "\n")

def enviar_fotos_agrupadas(app, channel_id, pasta_fotos, arquivos_enviados):
    print(pasta_fotos)
    # Lista todos os arquivos de imagem na pasta e ordena alfabeticamente
    fotos = [f for f in os.listdir(pasta_fotos) if f.lower().endswith(tuple(TYPE_FILE))]
    fotos.sort()  # Ordena os arquivos de imagem em ordem alfabética

    # Se não houver fotos na pasta
    if not fotos:
        print("Nenhuma foto encontrada na pasta.")
        return

    total_fotos = len(fotos)
    fotos_agrupadas = [fotos[i:i + 10] for i in range(0, total_fotos, 10)]  # Divide as fotos em grupos de até 10 fotos

    # Usando tqdm para mostrar o progresso
    with tqdm(total=total_fotos, desc="Enviando fotos", unit="foto") as pbar:
        with app:
            if not channel_id:
                #Criar canal
                channel = app.create_channel("GalleryGram")
                channel_link = app.export_chat_invite_link(channel.id)
                channel_id = channel.id
                description = f"Sua coleção de fotos no Telegram\n\nID {channel_id}\nLink: {channel_link}"
                app.set_chat_description(channel_id, description)

            folder = pasta_fotos.split('\\')[-1]
            app.send_message(channel_id, f"#{folder}")  # Envia o nome da pasta como tag
            for grupo in fotos_agrupadas:
                media = []
                novos_arquivos_enviados = []
                for arquivo in grupo:
                    # Verifica se o arquivo já foi enviado
                    if arquivo in arquivos_enviados:
                        continue
                    caminho_arquivo = os.path.join(pasta_fotos, arquivo)
                    if arquivo.lower().endswith(tuple(TYPE_PHOTO)):  # Se for uma foto
                        media.append(InputMediaPhoto(caminho_arquivo))
                    elif arquivo.lower().endswith(tuple(TYPE_VIDEO)):  # Se for um vídeo
                        media.append(InputMediaVideo(caminho_arquivo))
                    # Registra o arquivo como enviado
                    novos_arquivos_enviados.append(arquivo)
                    arquivos_enviados.add(arquivo)
                if media:
                    print("\tEnviando grupo de arquivos...")
                    app.send_media_group(channel_id, media)  # Envia o grupo de arquivos (fotos e vídeos)
                    pbar.update(len(grupo))  # Atualiza a barra de progresso com a quantidade de arquivos enviados
                    for arquivo in novos_arquivos_enviados:
                        salvar_arquivo_enviado(arquivo)
                    time.sleep(PAUSE)  # Pausa para evitar spams ou bloqueios


os.system('clear')
banner = Banner('GalleryGram')
banner.print_banner()

# Configurações do bot e credenciais
channel_id = input("ID do canal de destino (vazio para criar um novo):")  # Substitua pelo seu ID ou nome de usuário do canal

spinner = Halo(text='Verificando vídeos para conversão...', spinner='dots')

def get_settings():
    global TYPE_FILE, TYPE_PHOTO, TYPE_VIDEO, IGNORE_FOLDERS, PAUSE
    config = configparser.ConfigParser()
    config.read("config.ini")
    IGNORE_FOLDERS = eval(config.get("settings", "IGNORE_FOLDERS"))
    TYPE_PHOTO = eval(config.get("settings", "TYPE_PHOTO"))
    TYPE_VIDEO = eval(config.get("settings", "TYPE_VIDEO"))
    PAUSE = int(config.get("settings", "PAUSE"))
    TYPE_FILE = TYPE_PHOTO + TYPE_VIDEO

# Arquivo de registro dos arquivos enviados
if not os.path.exists("./temp"):
    os.makedirs("./temp")
ARQUIVOS_ENVIADOS = "./temp/arquivos_enviados.txt"

if os.path.exists('user.session'):
    api_id, api_hash = None, None
elif os.path.exists('config.ini'):
    api_id, api_hash = get_config()
    if api_id == '' or api_hash == '':
        get_api_credentials()
else:
    spinner.error("Arquivo config.ini não encontrado")
    raise Exception("Valores de API vazios")

app = Client("user", api_id=api_id, api_hash=api_hash)
get_settings()

if __name__ == "__main__":
    print('Insira o caminho das pastas\n(separado por virgula)')
    while True:
        str_pastas = input()
        if not str_pastas:
            print('Insira um caminho válido')
        else:
            break

    pastas = [pasta.strip() for pasta in str_pastas.split(',')]
    for pasta in pastas:
        arquivos_enviados = carregar_arquivos_enviados()
        enviar_fotos_agrupadas(app=app, channel_id=channel_id, pasta_fotos=pasta, arquivos_enviados=arquivos_enviados)