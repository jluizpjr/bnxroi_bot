import telebot
import requests
import random
import os
import draw

from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError

print(os.getenv('telebot_key'))
print(os.environ.get('cmc_key'))

bot = telebot.TeleBot(os.getenv('telebot_key'))
cmc = CoinMarketCapAPI(os.environ.get('cmc_key'))

gold_mining_rate = {
    0.0040: "100%", 0.0039: "95.06%", 0.0038: "90.25%", 0.0037: "85.56%",
    0.0036: "81.00%", 0.0035: "76.56%", 0.0034: "72.25%",
    0.0033: "68.06%", 0.0032: "64.00%", 0.0031: "60.06%",
    0.0030: "56.25%", 0.0029: "52.56%", 0.0028: "49.00%",
    0.0027: "45.56%", 0.0026: "42.25%", 0.0025: "39.06%",
    0.0024: "36.00%", 0.0023: "33.06%", 0.0022: "30.25%",
    0.0021: "27.56%", 0.0020: "25.00%", 0.0019: "22.56%",
    0.0018: "20.25%", 0.0017: "18.06%", 0.0016: "16.00%",
    0.0015: "14.06%", 0.0014: "12.25%", 0.0013: "10.56%",
    0.0012: "9.00%" , 0.0011: "7.56%" , 0.0010: "6.25%" ,
    0.0009: "5.06%" , 0.0008: "4.00%" , 0.0007: "3.06%" ,
    0.0006: "2.25%" , 0.0005: "1.56%" , 0.0004: "1.00%" ,
    0.0003: "0.56%" , 0.0002: "0.25%" , 0.0001: "0.06%"
}

crystal_mining_rate = {
    0.30:  "0.10%", 0.31:  "3.54%", 0.32:  "7.08%", 0.33: "10.64%",
    0.34: "14.21%", 0.35: "17.82%", 0.36: "21.46%", 0.37: "25.15%",
    0.38: "28.89%", 0.39: "32.71%", 0.40: "36.60%", 0.41: "40.60%",
    0.42: "44.72%", 0.43: "49.00%", 0.44: "53.47%", 0.45: "58.19%",
    0.46: "63.25%", 0.47: "68.79%", 0.48: "75.11%", 0.49: "82.93%", 0.50: "100%"
}


# SimpleCustomFilter is for boolean values, such as is_admin=True
class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key='is_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        return bot.get_chat_member(message.chat.id,message.from_user.id).status in ['administrator','creator']


@bot.message_handler(commands=['start', 'help', 'ajuda'])
def send_welcome(message):
        bot.reply_to(message, "Bem vindo" +
        "\n   Digite /bnx para ver a cotação do BNX" +
        "\n   Digite /gold para ver a cotação do GOLD"
        )

@bot.message_handler(commands=['calculadora'])
def send_welcome(message):
        bot.reply_to(message, "!!EM CONSTRUÇÃO!!" +
        "\n   Digite: /calculadora [preço de compra] [atributo principal] ...."
        )

@bot.message_handler(commands=['tabelacristal'])
def send_welcome(message):
        bot.send_photo(message.chat.id, open('images/crystaltable.jpg', 'rb')
        )

@bot.message_handler(commands=['discord'])
def send_welcome(message):
        bot.reply_to(message, "Link para o discord oficial:" +
        "\nhttps://discord.gg/bWRr2D43"
        )

@bot.message_handler(commands=['bnx'])
def send_welcome(message):
        bnx = cmc.cryptocurrency_quotes_latest(id='9891') #BNX id 9891
        bnx_usd = bnx.data['9891']['quote']['USD']['price']
        print(bnx.data)
        bot.reply_to(message, "A cotação do BNX agora é = *${:,.4f}".format(bnx_usd) + "*"
        ,parse_mode = 'Markdown'
        )

@bot.message_handler(commands=['coins'])
def send_welcome(message):

        btc = requests.get("https://api.pancakeswap.info/api/v2/tokens/0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c").json()
        btc_usd = round(float(btc["data"]["price"]),6)

        bnb = requests.get("https://api.pancakeswap.info/api/v2/tokens/0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c").json()
        bnb_usd = round(float(bnb["data"]["price"]),6)

        bnx = requests.get("https://api.pancakeswap.info/api/v2/tokens/0x8C851d1a123Ff703BD1f9dabe631b69902Df5f97").json()
        bnx_usd = round(float(bnx["data"]["price"]),6)

        gold = requests.get("https://api.pancakeswap.info/api/v2/tokens/0xb3a6381070b1a15169dea646166ec0699fdaea79").json()
        gold_usd = round(float(gold["data"]["price"]),6)
 
        crystal = requests.get("https://api.pancakeswap.info/api/v2/tokens/0x6AD7e691f1d2723523e70751f82052A8A2C47726").json()
        crystal_usd = round(float(crystal["data"]["price"]),6)

        if(gold_usd < 0.004):
            gr = str(gold_mining_rate[round(gold_usd,4)])
        else:
            gr = "100%"

        if(crystal_usd < 0.50):
            cr = str(crystal_mining_rate[round(crystal_usd,2)])
        else:
            cr = "100%"

        bot.reply_to(message, "A cotação das principais moedas é:" +
        "\nBTC     \t*${:,.2f}".format(btc_usd) + "*" +
        "\nBNB     \t*${:,.2f}".format(bnb_usd) + "*" +
        "\nBNX     \t*${:,.2f}".format(bnx_usd) + "*" +
        "\nGold    \t*${:,.6f}".format(gold_usd) + "* Ratio *" + gr + "*" +
        "\nCrystal \t*${:,.6f}".format(crystal_usd) + "* Ratio *" + cr + "*" 
        ,parse_mode = 'Markdown'
        )    

@bot.message_handler(commands=['gold2'])
def send_welcome(message):
        gold = cmc.cryptocurrency_quotes_latest(id='12082') #gold id 12082
        gold_usd = gold.data['12082']['quote']['USD']['price']

        print(gold.data)
        if(gold_usd < 0.004):
            bot.reply_to(message, "A cotação do Gold agora é *${:,.6f}".format(gold_usd) + "*" +
            "\nPreço do CoinMarketCap!!" +
            "\nATENÇÃO: Com a cotação atual do gold o mining ratio é *" +
            str(gold_mining_rate[round(gold_usd,4)]) + "*" +
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
        print(gold)
        gold_usd = round(float(gold["data"]["price"]),6)

        if(gold_usd < 0.004):
            bot.reply_to(message, "A cotação do Gold agora é *${:,.6f}".format(gold_usd) + "*" +
            "\nPreço do Pancakeswap!!" +
            "\nATENÇÃO: Com a cotação atual do gold o mining ratio é *" +
            str(gold_mining_rate[round(gold_usd,4)]) + "*" +
            "\nO mining ratio só é atualizado às 9am BRT"
            ,parse_mode = 'Markdown'
        )    
        else:
            bot.reply_to(message, "A cotação do Gold agora é *${:,.6f}".format(gold_usd) + "*" +
            "\nPreço do Pancakeswap!!" +
            "\nATENÇÃO: Com a cotação atual do gold o mining ratio é *100%*" +
            "\nO mining ratio só é atualizado às 9am BRT"
            ,parse_mode = 'Markdown'
            )         


@bot.message_handler(commands=['crystal'])
def send_welcome(message):

        crystal = requests.get("https://api.pancakeswap.info/api/v2/tokens/0x6AD7e691f1d2723523e70751f82052A8A2C47726").json()
        print(crystal)
        crystal_usd = round(float(crystal["data"]["price"]),6)

        if(crystal_usd < 0.50):
            bot.reply_to(message, "A cotação do Crystal agora é *${:,.4f}".format(crystal_usd) + "*" +
            "\nPreço do Pancakeswap!!" +
            "\nATENÇÃO: Com a cotação do cristal atual o mining ratio é *" +
            str(crystal_mining_rate[round(crystal_usd,2)]) + "*" +
            "\nO mining ratio só é atualizado às 9am BRT"            
            ,parse_mode = 'Markdown'
            )
        else:
            bot.reply_to(message, "A cotação do Crystal agora é *${:,.4f}".format(crystal_usd) + "*" +
            "\nPreço do Pancakeswap!!" +
            "\nATENÇÃO: Com a cotação atual do cristal o mining ratio é *100%*" +
            "\nO mining ratio só é atualizado às 9am BRT"    
            ,parse_mode = 'Markdown'
            )

@bot.message_handler(commands=['goldhistory'])
def send_welcome(message):
        gold = cmc.cryptocurrency_quotes_latest(id='12082') #gold id 12082
        gold_usd = gold.data['12082']['quote']['USD']['price']
        print(gold.data)
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
        print(bnx.data)
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

################ GENERAL COMMANDS ##################

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
    bot.send_message(message.chat.id, draw.openDraw("Sorteio", 30))

@bot.message_handler(is_admin=True, commands=['listarparticipantes']) # Check if user is admin
def admin_rep(message):
    bot.send_message(message.chat.id, draw.listParticipants())

@bot.message_handler(is_admin=True, commands=['sortear']) # Check if user is admin
def admin_rep(message):
    bot.send_message(message.chat.id, draw.draw())

@bot.message_handler(is_admin=True, commands=['finalizarsorteio']) # Check if user is admin
def admin_rep(message):
    bot.send_message(message.chat.id, draw.closeDraw())


################ GENERAL COMMANDS ##################

@bot.message_handler(commands=['ticket'])
def send_welcome(message):
    if(message.from_user.username != None):
        bot.reply_to(message, draw.newTicket(message.from_user.username))
    else:
        bot.reply_to(message, draw.newTicket(message.from_user.first_name))

@bot.message_handler(commands=['tempo'])
def send_welcome(message):
        bot.reply_to(message, draw.checkTime())



#####################################################################################
# Filter Section
#
#####################################################################################

@bot.channel_post_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.add_custom_filter(IsAdmin())

bot.infinity_polling()

