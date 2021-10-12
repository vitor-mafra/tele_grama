import configparser
from operator import itemgetter
import pandas as pd

import telethon
from telethon import TelegramClient, events, sync

# Lendo as credenciais unicas
config = configparser.ConfigParser()
config.read("./config.ini")

api_id = config["Telegram"]["api_id"]
api_hash = config["Telegram"]["api_hash"]
api_hash = str(api_hash)

phone = config["Telegram"]["phone"]
username = config["Telegram"]["username"]

# Adicionando as credenciais unicas
client = TelegramClient(username, api_id, api_hash)
client.start()

# Autorizando o login
if not client.is_user_authorized():
    client.send_code_request(phone)  # autenticacao de 2 fatores
    try:
        client.sign_in(phone, input("Enter the code: "))
    except telethon.errors.SessionPasswordNeededError:
        client.sign_in(password=input("Password: "))


async def main():
    # aqui vamos pegar como exemplo o canal do presidente do Brasil. Somente um exemplo.
    jairmbolsonaro1_channel = await client.get_entity("jairbolsonarobrasil")
    # participantes = jairmbolsonaro1_channel.GetParticipantsRequest()
    # stats = await client.GetBroadcastStatsRequest(jairmbolsonaro1_channel)
    mensagens = client.iter_messages(jairmbolsonaro1_channel)

    alcance_mensagens = []

    info_mensagem = {
        "id": None,
        "text": None,
        "data": None,
        "hora": None,
        "views": None,
        "encaminhamentos": None,
    }

    async for mensagem in mensagens:
        info_mensagem["id"] = mensagem.id
        info_mensagem["text"] = mensagem.text
        info_mensagem["data"] = mensagem.date.strftime("%Y-%m-%d")
        info_mensagem["hora"] = mensagem.date.strftime("%H:%M:%S")
        info_mensagem["views"] = mensagem.views
        info_mensagem["encaminhamentos"] = mensagem.forwards

        alcance_mensagens.append(info_mensagem)

        info_mensagem = {}

    alcance_mensagens_filtrada = sorted(alcance_mensagens, key=itemgetter("id"))

    for item in alcance_mensagens_filtrada:
        if item["views"] == None:
            alcance_mensagens_filtrada.remove(item)

    for item in alcance_mensagens_filtrada:
        print(item)

    df = pd.DataFrame(alcance_mensagens_filtrada)
    df.to_csv("./mensagens_jairmbolsonaro1_channel_metadata.csv", index=False)


with client:
    client.loop.run_until_complete(main())
