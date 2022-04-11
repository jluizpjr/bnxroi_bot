import time
import json
import random
import datetime
import os


drawOpen = False
openTime = 0
totalTime = 0
draw_dict = {}


# openDraw(str prize, str minutes) - Opens the draw
# args: str prize, str minutes
# return: str confirmation/error
def openDraw(prize, minutes,message):
    print("openDraw")
    try:
        f = open(str("draw"+str(message.chat.id)+".json"), "x")
    except:
        return "Raffle in progress"
    else:
        draw_dict['prize'] = prize
        draw_dict['openTime'] = time.time()
        draw_dict['duration'] = minutes
        draw_dict['users'] = []
        json.dump(draw_dict, f)
        f.close()
        return "Raffle started \nType /ticket to join"

# closeDraw() - End current Draw
# args: none
# return: str confirmation/error
def closeDraw(message):
    print("closeDraw")    
    if os.path.exists(str("draw"+str(message.chat.id)+".json")):
        os.remove(str("draw"+str(message.chat.id)+".json"))
        return "Raffle ended"
    else:
        print("The file does not exist")
        return "There is no ongoing raffle" 

# newTicket(user) - Issues a ticket to user
# args: str user
# return: str confirmation/error
def newTicket(message):

    msg = []

    if(message.from_user.username != None):
        user = str(message.from_user.username) 
    else:
        user = str(message.from_user.first_name)

    print("newTicket")    
    try:
        f = open(str("draw"+str(message.chat.id)+".json"), "r")
        draw_dict = json.load(f)
        if(time.time() > (draw_dict['openTime']+draw_dict['duration']*60) ):
            f.close()
            return "Time's up"
        else:
            with open(str("draw"+str(message.chat.id)+".json"), "r+") as f:
                draw_dict = json.load(f)
                for key in draw_dict["users"]:
                    if(key[0]==user):
                        return "Ticket already issued for user"
                draw_dict['users'].append([user,message.from_user.id])
                f.seek(0,0)
                print(draw_dict)
                json.dump(draw_dict, f)
                f.close()
                return "Ticket issued"             
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return "There is no ongoing raffle"

    finally:
        pass

# listParticipants() - List total participants already enrolled
# args: none
# return: str
# ADMIN_ONLY
def listParticipants(message):
    try:
        with open(str("draw"+str(message.chat.id)+".json"), "r") as f:
            draw_dict = json.load(f)
            lista = ""
            i = 1
            for key in draw_dict["users"]:
                lista += str(i) + " - " + key[0] + " UID="+str(key[1]) +"\n"
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
        with open(str("draw"+str(message.chat.id)+".json"), "r") as f:
            draw_dict = json.load(f)
            if(len(draw_dict["users"]) < 1):
                return "This raffle needs at least 2 participants"
            winner = random.randrange(0,len(draw_dict["users"]))
            f.close()
            return "The winner is " + draw_dict["users"][winner][0] + " UID=" + str(draw_dict["users"][winner][1]) , draw_dict["users"][winner][2]
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return "There is no ongoing raffle" 

# checktime()
# args: none
# returns: str remaining time in hh:mm:ss format
def checkTime(message):
    try:
        f = open(str("draw"+str(message.chat.id)+".json"), "r")
        draw_dict = json.load(f)
        if(time.time() > (draw_dict['openTime']+draw_dict['duration']*60) ):
            f.close()
            return "Time's up"
        f.close()
        return "Remaining time " + str(datetime.timedelta(seconds=((draw_dict['openTime']+draw_dict['duration']*60) - time.time()))).split(".")[0]
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