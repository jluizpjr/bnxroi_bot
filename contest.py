import time
import json
import random
import datetime
import os
import sqlite3

contestpen = False
openTime = 0
totalTime = 0
contest_dict = {}
global connection

# openContest(str minutes) - Opens the contest
# args: str minutes
# return: str confirmation/error
def openContest(minutes,message):
    print("openContest")
    try:
        f = open(str("contest"+str(message.chat.id)+".json"), "x")
    except:
        return "Contest in progress"
    else:
        contest_dict['openTime'] = time.time()
        contest_dict['duration'] = minutes
        contest_dict['users'] = []
        json.dump(contest_dict, f)
        f.close()

        global connection
        connection = sqlite3.connect(str("contest"+str(message.chat.id)+".db"))
        cursor = connection.cursor()
        table = str("contest"+str(message.chat.id))  
        cursor.execute('CREATE TABLE meme (from_user text, meme text, votes integer, chat_id integer, msg_id integer)')
        connection.commit()
        connection.close()
        return "Meme Contest started \nReply with /vote on the meme (picture) you like"


# closeContest(message) - End current Contest
# args: message
# return: str confirmation/error
def closeContest(message):
    print("closeContest")    
    if os.path.exists(str("contest"+str(message.chat.id)+".db")):
        os.remove(str("contest"+str(message.chat.id)+".db"))
    if os.path.exists(str("contest"+str(message.chat.id)+".json")):
        os.remove(str("contest"+str(message.chat.id)+".json"))
        return "Contest ended"
    else:
        print("The file does not exist")
        return "There is no ongoing contest" 

# vote(message) - Issues a ticket to user
# args: str user
# return: str confirmation/error
def vote(message):

    msg = []
    print("vote") 

    #Define who's voting
    if(message.from_user.username != None):
        user = str(message.from_user.username) 
    else:
        user = str(message.from_user.first_name)

    print("User: "+user)

    #Define who's being voted
    if(message.reply_to_message.from_user.username != None):
        from_user = message.reply_to_message.from_user.username       
        print("From_User: "+from_user)
    else:
        return "Content not supported"

    print(message.reply_to_message)

    #Define de content type
    if(message.reply_to_message.content_type == "sticker"): 
        meme = message.reply_to_message.sticker.file_id
    elif(message.reply_to_message.content_type == "animation"):
        meme = message.reply_to_message.animation.file_id
    elif(message.reply_to_message.content_type == "photo"):
        meme = message.reply_to_message.photo[0].file_id
    else:
        return "Content not identified"
    
    print("Meme: "+meme)
   
    try:
        f = open(str("contest"+str(message.chat.id)+".json"), "r")
        contest_dict = json.load(f)
        '''if(time.time() > (contest_dict['openTime']+contest_dict['duration']*60) ):
            f.close()
            return "Time's up"
        '''

        with open(str("contest"+str(message.chat.id)+".json"), "r+") as f:
            contest_dict = json.load(f)
            for key in contest_dict["users"]:
                if(key==user):
                    f.close()
                    return "User already voted"
            
            contest_dict['users'].append(user)

            ########################################
            #Open database, include [from_user, meme, votes]
            connection = sqlite3.connect(str("contest"+str(message.chat.id)+".db"))
            cursor = connection.cursor()
            print("connection open")

            #Validate if MEME is already in DB, othrwise add it
            cursor.execute('SELECT * FROM meme WHERE meme=?', (meme,))

            if item := cursor.fetchone():
                cursor.execute('UPDATE meme SET votes = votes + 1 WHERE meme=?', (meme,))
                print("Meme found, need to increment the votes")
            else:
                cursor.execute('INSERT INTO meme VALUES (?,?,?,?,?)', (from_user, meme, 1, message.reply_to_message.chat.id, message.reply_to_message.id ))
                print("Meme not found, need to include")

            ############ TEST ###################
            cursor.execute("SELECT * FROM meme" )
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            connection.commit()
            connection.close()
            ####################################

            f.seek(0,0)
            json.dump(contest_dict, f)
            f.close()
            return "Voted!"             
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return "Error processing meme"

    finally:
        pass

# listMeme() - List total participants already enrolled
# args: none
# return: str
# ADMIN_ONLY
def listMemes(message):
    print("listMeme")
    try:
            connection = sqlite3.connect(str("contest"+str(message.chat.id)+".db"))
            cursor = connection.cursor()

            cursor.execute("SELECT from_user,votes, msg_id FROM meme ORDER BY votes desc")
            rows = cursor.fetchall()
            list = "Username | Votes | Link to Meme\n"
            for row in rows:
                print(row)
                list +=  "@"+row[0] + ": " + str(row[1]) + \
                " <a href='https://t.me/" + str(message.chat.username) + \
                "/" + str(row[2]) + \
                "'> Meme </a>" + "\n"
            list += "Just reply with /vote on you favorite meme"
            #print(list)
            return list

    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return "There is no ongoing contest"

# draw() - Selects winner
# args: none
# return:  str 
# ADMIN_ONLY
def draw(message):
    try:
        with open(str("contest"+str(message.chat.id)+".json"), "r") as f:
            contest_dict = json.load(f)
            if(len(contest_dict["users"]) < 1):
                return "This raffle needs at least 2 participants"
            winner = random.randrange(0,len(contest_dict["users"]))
            f.close()
            return "The winner is " + contest_dict["users"][winner]
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return "There is no ongoing raffle" 

# checktime()
# args: none
# returns: str remaining time in hh:mm:ss format
def checkTime(message):
    try:
        f = open(str("contest"+str(message.chat.id)+".json"), "r")
        contest_dict = json.load(f)
        if(time.time() > (contest_dict['openTime']+contest_dict['duration']*60) ):
            f.close()
            return "Time's up"
        f.close()
        return "Remaining time " + str(datetime.timedelta(seconds=((contest_dict['openTime']+contest_dict['duration']*60) - time.time()))).split(".")[0]
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return "There is no ongoing raffle" 


#standalone tests
#
def main():
    print(openDraw("3 BNX", 10))
    print(checkTime())    
    print(newTicket("Joao"))
    print(newTicket("Jose"))
    print(newTicket("Maria"))
    print(listParticipants())
    print(draw())
    print(checkTime())
    print(closeDraw())

if __name__ == "__main__":
    main()