import os
import time
import configparser
import ast
from pathlib import Path
from typing import Tuple, Set, List

from pyrogram import Client  # type: ignore
from pyrogram.types import InputMediaPhoto, InputMediaVideo  # type: ignore
from tqdm import tqdm  # type: ignore
from halo import Halo  # type: ignore
import pyfiglet  # type: ignore

from banner import Banner
from log import logger
from schema import Settings


def get_config() -> Tuple[str, str]:
    """
    Lê as credenciais API do arquivo config.ini.
    """
    config = configparser.ConfigParser()
    config.read("config.ini")
    api_id = config.get("pyrogram", "api_id", fallback="")
    api_hash = config.get("pyrogram", "api_hash", fallback="")
    return api_id, api_hash


def get_api_credentials() -> Tuple[str, str]:
    """
    Solicita as credenciais API ao usuário e as salva no arquivo config.ini.
    """
    api_id = input("Digite o seu API_ID: ").strip()
    api_hash = input("Digite o seu API_HASH: ").strip()
    config = configparser.ConfigParser()
    config['pyrogram'] = {
        'api_id': api_id,
        'api_hash': api_hash
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    return api_id, api_hash


def carregar_arquivos_enviados(arquivo_registro: Path) -> Set[str]:
    """
    Carrega os nomes dos arquivos já enviados a partir do arquivo de registro.
    """
    if arquivo_registro.exists():
        with arquivo_registro.open("r", encoding="utf-8") as f:
            arquivos = f.read().splitlines()
        return set(arquivos)
    return set()


def salvar_arquivo_enviado(arquivo_registro: Path, arquivo: str) -> None:
    """
    Registra o arquivo enviado, adicionando-o ao arquivo de registro.
    """
    with arquivo_registro.open("a", encoding="utf-8") as f:
        f.write(arquivo + "\n")


def enviar_fotos_agrupadas(
    app: Client,
    channel_id: str,
    pasta_fotos: Path,
    arquivos_enviados: Set[str],
    arquivo_registro: Path,
) -> None:
    """
    Envia fotos e vídeos em grupos para um canal do Telegram.
    """
    try:
        settings = get_settings()

        print(f"Processando a pasta: {pasta_fotos}")
        TYPE_FILE = settings.get_type_file()

        # Lista e ordena os arquivos com as extensões permitidas

        # # Primeiro, converte todas as extensões válidas para minúsculas para comparação
        # extensoes_validas = [extensao.lower() for extensao in TYPE_FILE]
        
        # # Lista todos os itens na pasta
        # stodos_itens = list(pasta_fotos.iterdir())
        
        # # Filtra apenas os arquivos (exclui diretórios)
        # apenas_arquivos = [item for item in todos_itens if item.is_file()]
        
        # # Filtra arquivos que possuem extensões válidas
        # arquivos_validos = []
        # for arquivo in apenas_arquivos:
        #     extensao_arquivo = arquivo.suffix.lower().replace(".", "")
        #     if extensao_arquivo in extensoes_validas:
        #         arquivos_validos.append(arquivo.name)
        
        # # Ordena os nomes dos arquivos em ordem alfabética
        # fotos = sorted(arquivos_validos)
        fotos = sorted(
                [
                    f.name
                    for f in pasta_fotos.iterdir()
                    if f.is_file() and f.suffix.lower().replace(".", "") in [ext.lower() for ext in TYPE_FILE]
                ]
            )

        if not fotos:
            print("Nenhuma foto encontrada na pasta.")
            return

        total_fotos = len(fotos)
        # Divide a lista em grupos de até 10 arquivos
        fotos_agrupadas = [fotos[i : i + 10] for i in range(0, total_fotos, 10)]

        with tqdm(total=total_fotos, desc="Enviando fotos", unit="foto") as pbar:
            with app:
                # Caso não haja channel_id, cria um novo canal
                if not channel_id:
                    channel = app.create_channel(settings.channel_name)
                    channel_link = app.export_chat_invite_link(channel.id)
                    channel_id = channel.id
                    description = (
                        f"Sua coleção de fotos no Telegram\n\nID {channel_id}\nLink: {channel_link}"
                    )
                    app.set_chat_description(channel_id, description)

                folder_tag = f"#{pasta_fotos.name}"
                app.send_message(channel_id, folder_tag)

                for grupo in fotos_agrupadas:
                    media = []
                    novos_arquivos_enviados = []
                    for arquivo in grupo:
                        if arquivo in arquivos_enviados:
                            continue
                        caminho_arquivo = str(pasta_fotos / arquivo)
                        if arquivo.lower().endswith(tuple([ext.lower() for ext in settings.type_photo])):
                            media.append(InputMediaPhoto(caminho_arquivo))
                        elif arquivo.lower().endswith(tuple([ext.lower() for ext in settings.type_video])):
                            media.append(InputMediaVideo(caminho_arquivo))
                        novos_arquivos_enviados.append(arquivo)
                        arquivos_enviados.add(arquivo)
                    if media:
                        print("\tEnviando grupo de arquivos...")
                        app.send_media_group(channel_id, media)
                        pbar.update(len(grupo))
                        for arquivo in novos_arquivos_enviados:
                            salvar_arquivo_enviado(arquivo_registro, arquivo)
                        time.sleep(settings.pause)
    except Exception as e:
        logger.error("Erro ao enviar fotos agrupadas: %s", e)
        raise


def get_settings() -> Settings:
    """
    Lê as configurações do arquivo config.ini e retorna as extensões permitidas
    para fotos, vídeos e o tempo de pausa entre os envios.
    """
    config = configparser.ConfigParser()
    config.read("config.ini")
    # return settings
    # Utiliza ast.literal_eval para converter as strings de lista
    try:
        settings = Settings(
            ignore_folders = ast.literal_eval(config.get("settings", "IGNORE_FOLDERS", fallback="[]"))['ignore_folders'],
            type_photo = ast.literal_eval(config.get("settings", "TYPE_PHOTO", fallback="[]")),
            type_video = ast.literal_eval(config.get("settings", "TYPE_VIDEO", fallback="[]")),
            pause = int(config.get("settings", "PAUSE", fallback="1")),
            api_id = config.get("settings", "API_ID", fallback=""),
            api_hash = config.get("settings", "API_HASH", fallback=""),
            channel_name = config.get("settings", "CHANNEL_NAME", fallback="GalleryGram"),
        )
    except (ValueError, SyntaxError) as e:
        logger.error("Erro ao interpretar as configurações: %s", e)
        raise
    return settings



def main():
    os.system("clear")
    banner = Banner("GalleryGram")
    banner.print_banner()

    # Define o caminho do arquivo de registro
    temp_dir = Path("./temp")
    temp_dir.mkdir(exist_ok=True)
    arquivo_registro = temp_dir / "arquivos_enviados.txt"

    # Obtém as credenciais
    if Path("user.session").exists():
        api_id, api_hash = None, None
    elif Path("config.ini").exists():
        api_id, api_hash = get_config()
        if not api_id or not api_hash:
            api_id, api_hash = get_api_credentials()
    else:
        error_msg = "Arquivo config.ini não encontrado ou com valores de API vazios."
        logger.error(error_msg)
        raise Exception(error_msg)

    # Cria o cliente do Pyrogram
    app = Client("user", api_id=api_id, api_hash=api_hash)
    

    # Pergunta o ID do canal (se vazio, será criado um novo)
    channel_id = input("ID do canal de destino (vazio para criar um novo): ").strip()

    print("Insira o caminho das pastas (separado por vírgula):")
    while True:
        # str_pastas = input().strip()
        str_pastas = "/home/paulo/workspace/GalleryGram/photo"
        if not str_pastas:
            print("Insira um caminho válido!")
        else:
            break

    # Processa cada pasta informada
    pastas = [Path(pasta.strip()) for pasta in str_pastas.split(",")]
    for pasta in pastas:
        if not pasta.exists() or not pasta.is_dir():
            print(f"Pasta {pasta} inválida ou não encontrada.")
            continue
        arquivos_enviados = carregar_arquivos_enviados(arquivo_registro)
        try:
            enviar_fotos_agrupadas(
                app=app,
                channel_id=channel_id,
                pasta_fotos=pasta,
                arquivos_enviados=arquivos_enviados,
                arquivo_registro=arquivo_registro,
            )
        except Exception as e:
            logger.error("Erro ao enviar arquivos da pasta %s: %s", pasta, e)


if __name__ == "__main__":
    main()
