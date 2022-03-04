import telebot
import requests
import random
import os
import draw
import contest
import ama
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
        telebot.types.BotCommand("ajudasorteio", "submenu de sorteio")
    ],
)

whats_up = [
    "dungeon level 2 deu profit hoje", 
    "perdi uma dungeon por causa da bsc", 
    "o que salvou a dungeon foi o item que dropou", 
    "não sei se faço saque ou reinvisto", 
    "esperando preço do bnx baixar pra colocar mais em staking",
    "procurando item no market pra matar o senator",
    "fazendo a limpa nos mão de alface", 
    "só de olho no grupo esperando os sorteios",
    "esperando pix cair na binance",
    "lá vou eu reinvestir no jogo",
    "calma, to lendo os fixados"
]

# SimpleCustomFilter is for boolean values, such as is_admin=True
class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key='is_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        return bot.get_chat_member(message.chat.id,message.from_user.id).status in ['administrator','creator']


@bot.message_handler(commands=['start', 'help', 'ajuda'])
def send_welcome(message):
        schedule.every(3600).seconds.do(send_bora_s, message.chat.id).tag(message.chat.id)
        bot.reply_to(message, "Bem vindo" +
        "\n   Digite /bnx para ver a cotação do BNX" +
        "\n   Digite /gold para ver a cotação do GOLD"
        )


@bot.message_handler(commands=['discord'])
def send_welcome(message):
        bot.reply_to(message, "Link para o discord oficial:" +
        "\nhttps://discord.gg/bQ8R4WUxZN"
        )

@bot.message_handler(commands=['fixados'])
def send_welcome(message):
        bot.reply_to(message.reply_to_message, "👆🏻Isso aí já foi respondido e está nos fixados do canal👆🏻"
        )

@bot.message_handler(commands=['bora'])
def send_bora(message):
        bot.reply_to(message, whats_up[random.randrange(0, len(whats_up))]
        )

def send_bora_s(message_chat_id) -> None:
        print("Random message time")
        bot.send_message(message_chat_id, whats_up[random.randrange(0, len(whats_up))]
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


#        btc = requests.get("https://api.pancakeswap.info/api/v2/tokens/0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c").json()
#        btc_usd = round(float(btc["data"]["price"]),6)

#        bnb = requests.get("https://api.pancakeswap.info/api/v2/tokens/0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c").json()
#        bnb_usd = round(float(bnb["data"]["price"]),6)

#        bnx = requests.get("https://api.pancakeswap.info/api/v2/tokens/0x8C851d1a123Ff703BD1f9dabe631b69902Df5f97").json()
#        bnx_usd = round(float(bnx["data"]["price"]),6)

#        gold = requests.get("https://api.pancakeswap.info/api/v2/tokens/0xb3a6381070b1a15169dea646166ec0699fdaea79").json()
#        gold_usd = round(float(gold["data"]["price"]),6)
 
#        crystal = requests.get("https://api.pancakeswap.info/api/v2/tokens/0x6AD7e691f1d2723523e70751f82052A8A2C47726").json()
#        crystal_usd = round(float(crystal["data"]["price"]),6)

        btc = cmc.cryptocurrency_quotes_latest(id='1') #btc id 1
        btc_usd = btc.data['1']['quote']['USD']['price']

        bnb = cmc.cryptocurrency_quotes_latest(id='1839') #bnb id 1839
        bnb_usd = bnb.data['1839']['quote']['USD']['price']

        bnx = cmc.cryptocurrency_quotes_latest(id='9891') #bnx id 9891
        bnx_usd = bnx.data['9891']['quote']['USD']['price']

        gold = cmc.cryptocurrency_quotes_latest(id='12082') #gold id 12082
        gold_usd = gold.data['12082']['quote']['USD']['price']            

        crystal = cmc.cryptocurrency_quotes_latest(id='17356') #gold id 17356
        crystal_usd = crystal.data['17356']['quote']['USD']['price']   

        bot.reply_to(message, "A cotação das principais moedas é:" +
        "\nBTC     \t*${:,.2f}".format(btc_usd) + "*" +
        "\nBNB     \t*${:,.2f}".format(bnb_usd) + "*" +
        "\nBNX     \t*${:,.2f}".format(bnx_usd) + "*" +
        "\nGold    \t*${:,.6f}".format(gold_usd) + "*" +
        "\nCrystal \t*${:,.6f}".format(crystal_usd) + "*" 
        ,parse_mode = 'Markdown'
        )    

@bot.message_handler(commands=['gold2'])
def send_welcome(message):
        gold = cmc.cryptocurrency_quotes_latest(id='12082') #gold id 12082
        gold_usd = gold.data['12082']['quote']['USD']['price']

        if(gold_usd < 0.004):
            bot.reply_to(message, "A cotação do Gold agora é *${:,.6f}".format(gold_usd) + "*" +
            "\nPreço do CoinMarketCap!!" +
            "\nATENÇÃO: Com a cotação atual do gold o mining ratio é *" +
            str(gold_mining_rate[truncate(gold_usd,4)]) + "*" +
            "\nO mining ratio só é atualizado às 9am BRT"
            ,parse_mode = 'Markdown'
            )    
        else:
            bot.reply_to(message, "A cotação do Gold agora é *${:,.6f}".format(gold_usd) + "*" +
            "\nPreço do CoinMarketCap!!" +
            "\nATENÇÃO: Com a cotação atual do gold o mining ratio é *100%*" +
            "\nO mining ratio só é atualizado às 9am BRT"
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


@bot.message_handler(commands=['crystal'])
def send_welcome(message):

        crystal = requests.get("https://api.pancakeswap.info/api/v2/tokens/0x6AD7e691f1d2723523e70751f82052A8A2C47726").json()
        crystal_usd = round(float(crystal["data"]["price"]),6)


        bot.reply_to(message, "A cotação do Crystal agora é *${:,.4f}".format(crystal_usd) + "*" +
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

@bot.message_handler(commands=['market'])
def send_welcome(message):

        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

        try:
            promo = requests.get("https://market.binaryx.pro/getSales?page=1&page_size=1&status=selling&name=&sort=price&direction=asc&career=&value_attr=&start_value=&end_value=&pay_addr=", headers=header).json()
        except:
            bot.reply_to(message, "O market está fechado agora") 
        else: 
            promo_bnx =  int(promo["data"]["result"]["items"][0]["price"]) / 1000000000000000000
            bot.reply_to(message, "O menor preço de lv1 no market agora é *" + "{:.4f}".format(promo_bnx) + "* BNX"
            ,parse_mode = 'Markdown')        

@bot.message_handler(commands=['boladecristal'])
def send_welcome(message):

        gold = requests.get("https://api.pancakeswap.info/api/v2/tokens/0xb3a6381070b1a15169dea646166ec0699fdaea79").json()
        gold_usd = round(float(gold["data"]["price"]),6) 
        bot.reply_to(message, "Consultando os astros..... consultando os exús.... " +
            "\nA cotação do Gold daqui 15 dias será = $" + "{:.6f}".format(round(gold_usd,6)*random.randrange(1,10)))    




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
# Contest Section
#
#####################################################################################

################ ADMIN COMMANDS ##################
@bot.message_handler(is_admin=True, commands=['startcontest']) # Check if user is admin
def admin_rep(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        duration = int(args[1])
        bot.send_message(message.chat.id, contest.openContest(duration ,message))
    else:
        bot.send_message(message.chat.id, "Usage: /startcontest <minutes>")      

@bot.message_handler(is_admin=True, commands=['endcontest']) # Check if user is admin
def admin_rep(message):
    bot.send_message(message.chat.id, contest.closeContest(message))

@bot.message_handler(is_admin=True, commands=['listmeme']) # Check if user is admin
def admin_rep(message):
    bot.send_message(message.chat.id, contest.listMemes(message),  parse_mode = 'HTML', disable_web_page_preview=True)


################ GENERAL COMMANDS ##################

@bot.message_handler(commands=['vote'])
def send_welcome(message):
    bot.reply_to(message, contest.vote(message))



#####################################################################################
# AMA Section
#
#####################################################################################

################ ADMIN COMMANDS ##################

@bot.message_handler(is_admin=True, commands=['helpama']) # Check if user is admin
def admin_rep(message):
        bot.reply_to(message, "Bem vindo" +
        "\n   /startama Start AMA Q&A session <comment> <hours>*(ADM)*" +
        "\n   /question Send question to AMA Q&A" +
        "\n   /delquestion Delete question sent to AMA Q&A" +
        "\n   /admdelquestion [user] Delete question from user *(ADM)*" +      
        "\n   /listquestions List all questions *(ADM)*" +
        "\n   /endama End AMA Q&A session *(ADM)*"                         
        ,parse_mode = 'Markdown')   

@bot.message_handler(is_admin=True, commands=['startama']) # Check if user is admin
def admin_rep(message):
    args = message.text.split()
    if len(args) > 1 :
        bot.send_message(message.chat.id, ama.openAma(message))
    else:
        bot.send_message(message.chat.id, "Usage: /startama 'description' <hours>")      

@bot.message_handler(is_admin=True, commands=['endama']) # Check if user is admin
def admin_rep(message):
    bot.send_message(message.chat.id, ama.closeAma(message))

@bot.message_handler(is_admin=True, commands=['listquestions']) # Check if user is admin
def admin_rep(message):
    bot.send_message(message.chat.id, ama.listQuestions(message))   

@bot.message_handler(is_admin=True, commands=['admdelquestion']) # Check if user is admin
def admin_rep(message):
    bot.send_message(message.chat.id, ama.admdelQuestion(message))  

################ GENERAL COMMANDS ##################
@bot.message_handler(commands=['question'])
def send_welcome(message):
    bot.reply_to(message, ama.question(message))

@bot.message_handler(commands=['delquestion'])
def send_welcome(message):
    bot.reply_to(message, ama.delQuestion(message))
'''
@bot.message_handler(commands=['listquestions'])
def send_welcome(message):
    bot.send_message(message.chat.id, ama.listQuestions(message))
'''
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
