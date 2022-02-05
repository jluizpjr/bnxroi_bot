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
        cursor.execute("CREATE TABLE " + str("contest"+str(message.chat.id)) + " (from_user TEXT, meme TEXT, votes INTEGER)")
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

    #Define who's voting
    if(message.from_user.username != None):
        user = str(message.from_user.username) 
    else:
        user = str(message.from_user.first_name)

    #Define who's being voted
    if(message.reply_to_message.from_user.username != None):
        from_user = message.reply_to_message.from_user.username       
    else:
        return "You cannot vote for yourself"

    #Define de content type
    if(message.reply_to_message.content_type == "sticker"): 
        meme = message.reply_to_message.sticker.file_id
    elif(message.reply_to_message.content_type == "animation"):
        meme = message.reply_to_message.animation.file_id
    else:
        return "Content not identified"
    
    print("vote")    
    try:
        f = open(str("contest"+str(message.chat.id)+".json"), "r")
        contest_dict = json.load(f)
        if(time.time() > (contest_dict['openTime']+contest_dict['duration']*60) ):
            f.close()
            return "Time's up"

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
            
            #Validate if MEME is already in DB
            cursor.execute("SELECT * FROM " + str("contest"+str(message.chat.id)) + ".db WHERE meme = ?", (meme,))
            if item := cursor.fetchone():
                cursor.execute("UPDATE " + str("contest"+str(message.chat.id)) + ".db SET votes = votes + 1 WHERE meme = ?", (meme,))
                print("Meme found, need to increment the votes")
            else:
                cursor.execute("INSERT INTO " + str("contest"+str(message.chat.id)) + ".db VALUES (?,?,?)", (from_user, meme, 0))
                print("Meme not found, need to include")


            ####################################



            f.seek(0,0)
            print(contest_dict)
            json.dump(contest_dict, f)
            f.close()
            return "Voted!"             
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return "There is no ongoing contest"

    finally:
        pass

# listParticipants() - List total participants already enrolled
# args: none
# return: str
# ADMIN_ONLY
def listParticipants(message):
    try:
        with open(str("contest"+str(message.chat.id)+".json"), "r") as f:
            contest_dict = json.load(f)
            lista = ""
            i = 1
            for key in contest_dict["users"]:
                lista += str(i) + " - " + key + "\n"
                i += 1
            f.close()
            return lista
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return "There is no ongoing raffle"

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