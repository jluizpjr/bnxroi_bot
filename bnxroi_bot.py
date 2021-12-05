import telebot

from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError


# AdvancedCustomFilter is for list, string filter values
class MainFilter(telebot.custom_filters.AdvancedCustomFilter):
    key='text'
    @staticmethod
    def check(message, text):
        return message.text in text

# SimpleCustomFilter is for boolean values, such as is_admin=True
class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key='is_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        return bot.get_chat_member(message.chat.id,message.from_user.id).status in ['administrator','creator']



bot = telebot.TeleBot("2106071420:AAHGbrl8rUMAf9J0IYwnyTGoIRsPTmqeAtU")
cmc = CoinMarketCapAPI('563ee76c-4d7c-496f-99bf-96cadc3995d8')
 
mining_rate = {
    0.0040: "100%", 0.0039: "95.06%", 0.0038: "90.25%", 0.0037: "85.56%",
    0.0036: "81.00%", 0.0035: "76.56%", 0.0034: "72.25%",
    0.0033: "68.06%", 0.0032: "64.00%", 0.0031: "60.06%",
    0.0030: "56.25%", 0.0029: "52.56%", 0.0028: "49.00%",
    0.0027: "45.56%", 0.0026: "42.25%", 0.0025: "39.06%",
    0.0024: "36.00%", 0.0023: "33.06%", 0.0022: "30.25%"
}


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

@bot.message_handler(commands=['socorro'])
def send_welcome(message):
        bot.send_message(message.chat.id, "Relaxa, você não está sozinho(a)" +
        "\nO mercado de crypto é extremamente volátil. Essas variações são normais. Se você acredita no projeto, vamos seguir juntos!"
        )

@bot.message_handler(commands=['bnx'])
def send_welcome(message):
        bnx = cmc.cryptocurrency_quotes_latest(id='9891') #BNX id 9891
        bnx_usd = bnx.data['9891']['quote']['USD']['price']
        print(bnx.data)
        bot.send_message(message.chat.id, "A cotação do BNX agora é = $" + str(round(bnx_usd,2)))

@bot.message_handler(commands=['gold'])
def send_welcome(message):
        gold = cmc.cryptocurrency_quotes_latest(id='12082') #gold id 12082
        gold_usd = gold.data['12082']['quote']['USD']['price']

        print(gold.data)
        if(gold_usd < 0.004):
            bot.send_message(message.chat.id, "A cotação do Gold agora é = $" + str(round(gold_usd,6)) +
            "\nATENÇÃO: Com a cotação do gold atual o mining rate é " +
            str(mining_rate[round(gold_usd,4)]) +
            "\nO mining rate só é atualizado às 9am BRT"
            )   
        else:
            bot.reply_to(message, "A cotação do Gold agora é = $" + str(round(gold_usd,6)))

@bot.message_handler(commands=['goldhistory'])
def send_welcome(message):
        gold = cmc.cryptocurrency_quotes_latest(id='12082') #BNX id 9891
        gold_usd = gold.data['12082']['quote']['USD']['price']
        print(gold.data)
        bot.send_message(message.chat.id, "A cotação do Gold agora é = $" + str(round(gold_usd,6)) +
            "\nA variação nas últimas 24 horas foi de " + str(round(gold.data['12082']['quote']['USD']['percent_change_24h'],2)) + "%" +
            "\nA variação nos últimos 7 dias foi de " + str(round(gold.data['12082']['quote']['USD']['percent_change_7d'],2)) + "%" +
            "\nA variação nos últimos 30 dias foi de " + str(round(gold.data['12082']['quote']['USD']['percent_change_30d'],2)) + "%" +
            "\nA variação nos últimos 60 dias foi de " + str(round(gold.data['12082']['quote']['USD']['percent_change_60d'],2)) + "%" + 
            "\nA variação nos últimos 90 dias foi de " + str(round(gold.data['12082']['quote']['USD']['percent_change_90d'],2)) + "%"                                    
            )

#@bot.message_handler(func=lambda message: True)
#def echo_all(message):
#    bot.reply_to(message, message.text)


@bot.channel_post_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.add_custom_filter(MainFilter())
bot.add_custom_filter(IsAdmin())

bot.infinity_polling()

