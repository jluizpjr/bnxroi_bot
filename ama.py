import time
import json
import random
import datetime
import os
import sqlite3
import shlex

amaOpen = False
openTime = 0
totalTime = 0
ama_dict = {}
global connection

# openAma(str minutes) - Opens the AMA Q&A
# args: str minutes
# return: str confirmation/error
def openAma(message):
    print("openAma")

    # Parse arguments
    # Expected: "String:details" int:time

    parsed = shlex.split(message.text)
    print(parsed)
    if not parsed[2].isdigit():
        return "Usage: /startama 'description' <hours>"

    try:
        f = open(str("ama"+str(message.chat.id)+".json"), "x")
    except:
        return "AMM Q&A in progress"
    else:
        ama_dict['description'] = parsed[1]
        ama_dict['openTime'] = time.time()
        ama_dict['duration'] = int(parsed[2])*60
        ama_dict['users'] = []
        json.dump(ama_dict, f)
        f.close()

        global connection
        connection = sqlite3.connect(str("ama"+str(message.chat.id)+".db"))
        cursor = connection.cursor()
        table = str("ama"+str(message.chat.id))  
        cursor.execute('CREATE TABLE ama (user text, question text, translated_question text, answer text)')
        connection.commit()
        connection.close()
        return "AMA Q&A  started \nYou may send your questions with /question [question]"


# closeAma(message) - End current AMA Q&A
# args: message
# return: str confirmation/error
def closeAma(message):
    print("closeAma")    
    if os.path.exists(str("ama"+str(message.chat.id)+".db")):
        os.remove(str("ama"+str(message.chat.id)+".db"))
    if os.path.exists(str("ama"+str(message.chat.id)+".json")):
        os.remove(str("ama"+str(message.chat.id)+".json"))
        return "AMA Q&A ended"
    else:
        print("The file does not exist")
        return "There is no ongoing AMA" 

# question(message) - Submits a question to AMA
# args: str user
# return: str confirmation/error
def question(message):

    msg = []
    print("ama") 

    #Define who's asking
    if(message.from_user.username != None):
        user = str(message.from_user.username) 
    else:
        user = str(message.from_user.first_name)

    print("User: "+user)

    try:
        f = open(str("ama"+str(message.chat.id)+".json"), "r")
        ama_dict = json.load(f)
        if(time.time() > (ama_dict['openTime']+ama_dict['duration']*60) ):
            f.close()
            return "Time's up"
        

        with open(str("ama"+str(message.chat.id)+".json"), "r+") as f:
            ama_dict = json.load(f)
            for key in ama_dict["users"]:
                if(key==user):
                    f.close()
                    return "User already sent question."
            
            ama_dict['users'].append(user)

            ########################################
            #Open database, include [from_user, meme, votes]
            connection = sqlite3.connect(str("ama"+str(message.chat.id)+".db"))
            cursor = connection.cursor()
            print("connection open")

            cursor.execute("INSERT INTO ama VALUES (?,?,?,?)" , (user , message.text[10:], None, None ))

            ############ TEST ###################
            cursor.execute("SELECT * FROM ama" )
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            connection.commit()
            connection.close()
            ####################################

            f.seek(0,0)
            json.dump(ama_dict, f)
            f.close()
            return "Question sent!"             
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return "Error processing question"

    finally:
        pass


# delQuestion(message) - Submits a question to AMA
# args: str user
# return: str confirmation/error
def delQuestion(message):

    msg = []
    print("ama") 

    #Define who's asking
    if(message.from_user.username != None):
        user = str(message.from_user.username) 
    else:
        user = str(message.from_user.first_name)

    print("User: "+user)

    try:
      

        with open(str("ama"+str(message.chat.id)+".json"), "r+") as f:
            ama_dict = json.load(f)
            ama_dict['users'].remove(user)
            
            ########################################
            #Open database, include [from_user, meme, votes]
            connection = sqlite3.connect(str("ama"+str(message.chat.id)+".db"))
            cursor = connection.cursor()
            print("connection open")

            cursor.execute("DELETE FROM ama WHERE user=?" , [user])

            ############ TEST ###################
            cursor.execute("SELECT * FROM ama" )
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            connection.commit()
            connection.close()
            ####################################

            f.seek(0,0)
            f.truncate()
            json.dump(ama_dict, f)
            f.close()
            return "Question deleted!"             
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return "Error processing question"

    finally:
        pass


# listQuestions() - List questions submitted
# args: message
# return: str
# ADMIN_ONLY
def listQuestions(message):
    print("listQuestions")
    try:
            connection = sqlite3.connect(str("ama"+str(message.chat.id)+".db"))
            cursor = connection.cursor()

            cursor.execute("SELECT user,question FROM ama")
            rows = cursor.fetchall()
            list = "*Questions already submitted*\n\n"
            for row in rows:
                print(row)
                list +=  "@"+row[0] + "\n " + str(row[1]) + "\n\n"
            list += "Just send your question with /question [question]"
            #print(list)
            return list

    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return "There is no ongoing AMA Q&A"


# checktime()
# args: none
# returns: str remaining time in hh:mm:ss format
def checkTime(message):
    try:
        f = open(str("ama"+str(message.chat.id)+".json"), "r")
        ama_dict = json.load(f)
        if(time.time() > (ama_dict['openTime']+ama_dict['duration']*60) ):
            f.close()
            return "Time's up"
        f.close()
        return "Remaining time " + str(datetime.timedelta(seconds=((ama_dict['openTime']+ama_dict['duration']*60) - time.time()))).split(".")[0]
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return "There is no ongoing AMA Q&A" 


#standalone tests
#
def main():
    print(checkTime())    

if __name__ == "__main__":
    main()