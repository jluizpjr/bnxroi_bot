import telebot
import requests
import os
import math
import draw
import womtable
import time, threading, schedule
from utils import truncate
from telebot import types


from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError

print(os.getenv('telebot_key'))
print(os.environ.get('cmc_key'))

bot = telebot.TeleBot(os.getenv('telebot_key'))
cmc = CoinMarketCapAPI(os.environ.get('cmc_key'))

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("fixados", "resposta apontando para fixados"),
        telebot.types.BotCommand("coins", "cotação das moedas"),
        telebot.types.BotCommand("discord", "link para o discord"),
        telebot.types.BotCommand("bnx", "cotação do BNX"),                
        telebot.types.BotCommand("gold", "cotação do GOLD"),         
        telebot.types.BotCommand("crystal", "cotação do Crystal"),    
        telebot.types.BotCommand("ajudasorteio", "submenu de sorteio"),
        telebot.types.BotCommand("wom", "retorna o WOM das DGs")
    ],
)

# SimpleCustomFilter is for boolean values, such as is_admin=True
class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key='is_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        return bot.get_chat_member(message.chat.id,message.from_user.id).status in ['administrator','creator']


@bot.message_handler(commands=['discord'])
def send_welcome(message):
        bot.reply_to(message, "Link para o discord oficial:" +
        "\nhttps://discord.gg/bQ8R4WUxZN"
        )

@bot.message_handler(commands=['fixados'])
def send_welcome(message):
        bot.reply_to(message.reply_to_message, "👆🏻Isso aí já foi respondido e está nos fixados do canal👆🏻"
        )

@bot.message_handler(commands=['bnx'])
def send_welcome(message):
        bnx = cmc.cryptocurrency_quotes_latest(id='9891') #BNX id 9891
        bnx_usd = bnx.data['9891']['quote']['USD']['price']
        bot.reply_to(message, "A cotação do BNX agora é = *${:,.4f}".format(bnx_usd) + "*"
        ,parse_mode = 'Markdown'
        )   

@bot.message_handler(commands=['coins'])
def send_welcome(message):
        cmc_data = cmc.cryptocurrency_quotes_latest(id='1,1839,9891,12082,17356') #btc id 1
        btc_usd = cmc_data.data['1']['quote']['USD']['price']
        bnb_usd = cmc_data.data['1839']['quote']['USD']['price']
        bnx_usd = cmc_data.data['9891']['quote']['USD']['price']
        gold_usd = cmc_data.data['12082']['quote']['USD']['price']            
        crystal_usd = cmc_data.data['17356']['quote']['USD']['price']   

        bot.reply_to(message, "A cotação das principais moedas é:" +
        "\nBTC     \t*${:,.2f}".format(btc_usd) + "*" +
        "\nBNB     \t*${:,.2f}".format(bnb_usd) + "*" +
        "\nBNX     \t*${:,.2f}".format(bnx_usd) + "*" +
        "\nGold    \t*${:,.6f}".format(gold_usd) + "*" +
        "\nCrystal \t*${:,.6f}".format(crystal_usd) + "*" 
        ,parse_mode = 'Markdown'
        )    


@bot.message_handler(commands=['gold'])
def send_welcome(message):

        gold = requests.get("https://api.pancakeswap.info/api/v2/tokens/0xb3a6381070b1a15169dea646166ec0699fdaea79").json()
        gold_usd = round(float(gold["data"]["price"]),6)


        bot.reply_to(message, "A cotação do Gold agora é *${:,.6f}".format(gold_usd) + "*" +
        "\nPreço do Pancakeswap!!"
        ,parse_mode = 'Markdown'
        )    

@bot.message_handler(commands=['goldhistory'])
def send_welcome(message):
        gold = cmc.cryptocurrency_quotes_latest(id='12082') #gold id 12082
        gold_usd = gold.data['12082']['quote']['USD']['price']
        bot.reply_to(message, "A cotação do Gold agora é = $" + str(round(gold_usd,6)) +
            "\nA variação nas últimas 24 horas foi de " + str(round(gold.data['12082']['quote']['USD']['percent_change_24h'],2)) + "%" +
            "\nA variação nos últimos 7 dias foi de " + str(round(gold.data['12082']['quote']['USD']['percent_change_7d'],2)) + "%" +
            "\nA variação nos últimos 30 dias foi de " + str(round(gold.data['12082']['quote']['USD']['percent_change_30d'],2)) + "%" +
            "\nA variação nos últimos 60 dias foi de " + str(round(gold.data['12082']['quote']['USD']['percent_change_60d'],2)) + "%" + 
            "\nA variação nos últimos 90 dias foi de " + str(round(gold.data['12082']['quote']['USD']['percent_change_90d'],2)) + "%"                                    
            )

@bot.message_handler(commands=['bnxhistory'])
def send_welcome(message):
        bnx = cmc.cryptocurrency_quotes_latest(id='9891') #BNX id 9891
        bnx_usd = bnx.data['9891']['quote']['USD']['price']
        bot.reply_to(message, "A cotação do BNX agora é = $" + str(round(bnx_usd,2)) +
            "\nA variação nas últimas 24 horas foi de " + str(round(bnx.data['9891']['quote']['USD']['percent_change_24h'],2)) + "%" +
            "\nA variação nos últimos 7 dias foi de " + str(round(bnx.data['9891']['quote']['USD']['percent_change_7d'],2)) + "%" +
            "\nA variação nos últimos 30 dias foi de " + str(round(bnx.data['9891']['quote']['USD']['percent_change_30d'],2)) + "%" +
            "\nA variação nos últimos 60 dias foi de " + str(round(bnx.data['9891']['quote']['USD']['percent_change_60d'],2)) + "%" + 
            "\nA variação nos últimos 90 dias foi de " + str(round(bnx.data['9891']['quote']['USD']['percent_change_90d'],2)) + "%"                                    
            )  

@bot.message_handler(commands=['wom'])
def send_welcome(message):

        levels = [1,2,3,4,5,6]
        headers = { 
            'Accept' : '*/*', 
            'Content-Type' : 'application/x-www-form-urlencoded', 
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        }
        
        resp = [0]

        for level in levels:

            payload = {'Id':math.ceil(level/3), 'DungeonLv':level, 'lang':'en'}
            #print(payload)
            resp.append(requests.post("https://game.binaryx.pro/v1/dungeon/getlvratio", data=payload, headers=headers).json())
            #print(resp[level])


        bot.reply_to(message, "*Wealth of Monsters:* " +
            "\nDG LV1 = " + moon_phases(resp[1]["data"]["lv_ratio_point"]) +
            "\nDG LV2 = " + moon_phases(resp[2]["data"]["lv_ratio_point"]) + 
            "\nDG LV3 = " + moon_phases(resp[3]["data"]["lv_ratio_point"]) + 
            "\nDG LV4 = " + moon_phases(resp[4]["data"]["lv_ratio_point"]) + 
            "\nDG LV5 = " + moon_phases(resp[5]["data"]["lv_ratio_point"]) + 
            "\nDG LV6 = " + moon_phases(resp[6]["data"]["lv_ratio_point"]) +
            "\nQuanto maior a lua, melhor para fazer DG!!!"
            ,parse_mode = 'Markdown') 

def moon_phases(value):
    moon_phases = ["\U0001F311", "\U0001F318", "\U0001F317", "\U0001F316", "\U0001F315"]
    return moon_phases[value-1]

@bot.message_handler(commands=['womtable'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id,"Preparando dados... " )
    bot.last_message_sent = msg.chat.id, msg.message_id
    womtable.womtable()
    bot.delete_message(*bot.last_message_sent)
    bot.send_photo(message.chat.id, open('table.png', 'rb'))

#####################################################################################
# Draw Section
#
#####################################################################################

################ ADMIN COMMANDS ##################

@bot.message_handler(is_admin=True, commands=['ajudasorteio']) # Check if user is admin
def admin_rep(message):
        bot.reply_to(message, "Bem vindo" +
        "\n   /iniciarsorteio Iniciar um sorteio *(ADM)*" +
        "\n   /ticket Cadastrar no sorteio" +
        "\n   /listarparticipantes Ver participantes *(ADM)*" +
        "\n   /sortear Sortear *(ADM)*" + 
        "\n   /finalizarsorteio Encerrar *(ADM)*"                         
        ,parse_mode = 'Markdown')   

@bot.message_handler(is_admin=True, commands=['iniciarsorteio']) # Check if user is admin
def admin_rep(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        duration = int(args[1])
        bot.send_message(message.chat.id, draw.openDraw("Raffle", duration ,message))
    else:
        bot.send_message(message.chat.id, "Usage: /iniciarsorteio <minutes>")      

@bot.message_handler(is_admin=True, commands=['listarparticipantes']) # Check if user is admin
def admin_rep(message):
    bot.send_message(message.chat.id, draw.listParticipants(message))

@bot.message_handler(is_admin=True, commands=['sortear']) # Check if user is admin
def admin_rep(message):
    bot.send_message(message.chat.id, draw.draw(message))


@bot.message_handler(is_admin=True, commands=['finalizarsorteio']) # Check if user is admin
def admin_rep(message):
    bot.send_message(message.chat.id, draw.closeDraw(message))


################ GENERAL COMMANDS ##################

@bot.message_handler(commands=['ticket'])
def send_welcome(message):
    bot.reply_to(message, draw.newTicket(message))


@bot.message_handler(commands=['tempo'])
def send_welcome(message):
        bot.reply_to(message, draw.checkTime(message))



#####################################################################################
# Filter Section
#
#####################################################################################

@bot.channel_post_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.add_custom_filter(IsAdmin())

if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
