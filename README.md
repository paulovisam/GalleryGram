# GalleryGram

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://telegram.org)

**GalleryGram** é uma ferramenta automatizada para upload e organização de fotos e vídeos em canais do Telegram. Desenvolvida para facilitar o gerenciamento de grandes coleções de mídia, a aplicação processa pastas locais e envia o conteúdo de forma organizada e eficiente para canais do Telegram.

## ✨ Características Principais

- 🚀 **Upload Automático**: Envia fotos e vídeos automaticamente para canais do Telegram
- 📁 **Organização por Pastas**: Cada pasta é marcada com hashtags para fácil navegação
- 🔄 **Controle de Duplicatas**: Registra arquivos já enviados para evitar uploads duplicados
- 📊 **Barra de Progresso**: Acompanhe o progresso dos uploads em tempo real
- 🎯 **Upload em Lotes**: Envia até 10 arquivos por grupo para otimizar a velocidade
- 🛠️ **Configurável**: Extensões de arquivo, tempos de pausa e outras configurações personalizáveis
- 📝 **Sistema de Logs**: Registro detalhado de operações e erros
- 🎨 **Interface Visual**: Banner colorido e interface amigável no terminal
- 🆕 **Criação Automática de Canais**: Cria automaticamente novos canais quando necessário

## 🎯 Casos de Uso

- **Backup de Fotos**: Faça backup automático de suas fotos pessoais no Telegram
- **Compartilhamento de Eventos**: Organize e compartilhe fotos de eventos, viagens ou projetos
- **Arquivamento Digital**: Mantenha suas coleções de mídia organizadas e acessíveis
- **Distribuição de Conteúdo**: Distribua conteúdo visual de forma eficiente para grupos ou canais

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta no Telegram
- API_ID e API_HASH do Telegram (obtidos em [my.telegram.org](https://my.telegram.org))

## 🚀 Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/paulovisam/GalleryGram.git
cd GalleryGram
```

2. **Crie um ambiente virtual (recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure suas credenciais:**
   - Execute o programa pela primeira vez
   - Digite seu API_ID e API_HASH quando solicitado
   - Ou edite manualmente o arquivo `config.ini`

## ⚙️ Configuração

### Arquivo config.ini

O arquivo `config.ini` contém todas as configurações personalizáveis:

```ini
[settings]
is_convert_video=True
IGNORE_FOLDERS=["pasta1", "ignore_path"]
TYPE_PHOTO=["jpg", "jpeg", "png", "aae"]
TYPE_VIDEO=["mp4", "mov", "avi", "mkv", "3gp"]
PAUSE=2
API_ID=seu_api_id
API_HASH=seu_api_hash
CHANNEL_NAME=GalleryGram
```

### Parâmetros de Configuração

| Parâmetro | Descrição | Valores Padrão |
|-----------|-----------|----------------|
| `is_convert_video` | Habilita conversão de vídeo | `True` |
| `IGNORE_FOLDERS` | Lista de pastas a ignorar | `["pasta1", "ignore_path"]` |
| `TYPE_PHOTO` | Extensões de foto suportadas | `["jpg", "jpeg", "png", "aae"]` |
| `TYPE_VIDEO` | Extensões de vídeo suportadas | `["mp4", "mov", "avi", "mkv", "3gp"]` |
| `PAUSE` | Pausa entre uploads (segundos) | `2` |
| `API_ID` | Seu API ID do Telegram | - |
| `API_HASH` | Seu API Hash do Telegram | - |
| `CHANNEL_NAME` | Nome padrão para novos canais | `GalleryGram` |

## 🎮 Como Usar

1. **Execute o programa:**
```bash
python main.py
```

2. **Siga as instruções interativas:**
   - Digite o ID do canal de destino (deixe vazio para criar um novo)
   - Insira o caminho das pastas a serem processadas
   - Acompanhe o progresso na barra de status

3. **Exemplo de uso:**
```
ID do canal de destino (vazio para criar um novo): 
Insira o caminho das pastas (separado por vírgula):
/home/usuario/fotos/viagem, /home/usuario/fotos/evento
```

### Obtendo API Credentials

1. Acesse [my.telegram.org](https://my.telegram.org)
2. Faça login com seu número de telefone
3. Vá para "API Development Tools"
4. Crie uma nova aplicação
5. Copie seu `API_ID` e `API_HASH`

## 📁 Estrutura do Projeto

```
GalleryGram/
├── main.py              # Arquivo principal
├── banner.py            # Geração do banner colorido
├── log.py               # Sistema de logging
├── schema.py            # Modelos de dados (Pydantic)
├── config.ini           # Arquivo de configurações
├── requirements.txt     # Dependências Python
├── README.md           # Documentação
├── temp/               # Pasta temporária (criada automaticamente)
│   └── arquivos_enviados.txt
└── log/                # Logs da aplicação (criado automaticamente)
    ├── erros.txt
    └── info.txt
```

## 🔧 Funcionalidades Técnicas

### Sistema de Logging
- **Logs de Erro**: Salvos em `log/erros.txt`
- **Logs de Info**: Salvos em `log/info.txt`
- **Console**: Exibição em tempo real no terminal

### Controle de Duplicatas
- Registra arquivos enviados em `temp/arquivos_enviados.txt`
- Evita reenvio de arquivos já processados
- Permite retomar uploads interrompidos

### Upload Otimizado
- Envia até 10 arquivos por grupo
- Pausa configurável entre uploads
- Suporte a fotos e vídeos
- Organização automática por pastas

## 🛠️ Dependências

| Biblioteca | Versão | Propósito |
|------------|---------|-----------|
| `pyrogram` | 2.0.106 | Cliente Telegram API |
| `pydantic` | - | Validação de dados |
| `tqdm` | 4.67.1 | Barra de progresso |
| `colorama` | 0.4.6 | Cores no terminal |
| `pyfiglet` | 1.0.2 | Banner ASCII |
| `halo` | 0.0.31 | Spinners de loading |
| `pillow` | 11.1.0 | Processamento de imagens |

## 🐛 Solução de Problemas

### Problemas Comuns

1. **Erro de autenticação:**
   - Verifique se API_ID e API_HASH estão corretos
   - Delete o arquivo `user.session` e tente novamente

2. **Arquivos não são enviados:**
   - Verifique as extensões em `TYPE_PHOTO` e `TYPE_VIDEO`
   - Confirme se as pastas existem e contêm arquivos válidos

3. **Erro de permissão no canal:**
   - Certifique-se de ter permissões de administrador no canal
   - Para canais novos, permissões são concedidas automaticamente

### Logs de Debug

Verifique os arquivos de log para mais informações:
- `log/erros.txt` - Erros detalhados
- `log/info.txt` - Informações de operação

## 🚧 Limitações Conhecidas

- Limite de 10 arquivos por grupo (limitação do Telegram)
- Tamanho máximo de arquivo: 2GB (limitação do Telegram)
- Rate limiting automático para evitar spam

## 🔮 Roadmap

- [ ] Interface gráfica (GUI)
- [ ] Suporte a mais formatos de arquivo
- [ ] Compressão automática de vídeos
- [ ] Agendamento de uploads
- [ ] Sincronização bidirecional
- [ ] Suporte a múltiplos perfis de configuração

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Paulo Visam** - *Desenvolvedor Principal*

- GitHub: [@paulovisam](https://github.com/paulovisam)
- Telegram: [@paulovisam](https://t.me/paulovisam)

## 🙏 Agradecimentos

- [Pyrogram](https://pyrogram.org/) - Excelente cliente Python para Telegram
- [Telegram](https://telegram.org/) - Pela API robusta e bem documentada
- Comunidade Python - Pelas bibliotecas incríveis

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!** ⭐
