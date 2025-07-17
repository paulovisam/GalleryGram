import logging, os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not os.path.exists("./log"):
    os.makedirs("./log")

# Criando um handler para gravar em um arquivo de erros
error_handler = logging.FileHandler('./log/erros.txt')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(error_handler)

# Criando um handler para gravar em um arquivo de informações gerais
info_handler = logging.FileHandler('./log/info.txt')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(info_handler)

# Criando um handler para o terminal
terminal_handler = logging.StreamHandler()
terminal_handler.setLevel(logging.INFO)
terminal_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(terminal_handler)

log = logging