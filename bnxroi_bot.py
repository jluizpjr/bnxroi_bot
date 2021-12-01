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
    0.0036: "81.00%", 0.0035: "76.56%", 0.0034: "72.25%"

}

@bot.message_handler(commands=['start', 'help', 'ajuda'])
def send_welcome(message):
        print(bnx.data)
        bot.reply_to(message, "Bem vindo" +
        "\n   Digite /bnx para ver a cotação do BNX" +
        "\n   Digite /gold para ver a cotação do GOLD"
        )

@bot.message_handler(commands=['bnx'])
def send_welcome(message):
        bnx = cmc.cryptocurrency_quotes_latest(id='9891') #BNX id 9891
        bnx_usd = bnx.data['9891']['quote']['USD']['price']
        print(bnx.data)
        bot.reply_to(message, "A cotação do *BNX* agora é = $" + str(round(bnx_usd,2)))

@bot.message_handler(commands=['gold'])
def send_welcome(message):
        gold = cmc.cryptocurrency_quotes_latest(id='12082') #gold id 12082
        gold_usd = gold.data['12082']['quote']['USD']['price']

        print(gold.data)
        if(gold_usd < 0.004):
            bot.reply_to(message, "A cotação do Gold agora é = $" + str(round(gold_usd,6)) +
            "\nATENÇÃO: Como a cotação do gold atual o mining rate é " +
            str(mining_rate[round(gold_usd,4)]) +
            "\nO mining rate só é atualizado às 9am BRT"
            )   
        else:
            bot.reply_to(message, "A cotação do Gold agora é = $" + str(round(gold_usd,6)))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


@bot.channel_post_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.add_custom_filter(MainFilter())
bot.add_custom_filter(IsAdmin())

bot.infinity_polling()

