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
def openDraw(prize, minutes):
    print("openDraw")
    try:
        f = open("draw.json", "x")
    except:
        return "Já existe um sorteio em andamento"
    else:
        draw_dict['prize'] = prize
        draw_dict['openTime'] = time.time()
        draw_dict['duration'] = minutes
        draw_dict['users'] = []
        json.dump(draw_dict, f)
        f.close()
        return "Sorteio aberto \nDigite /ticket para participar"

# closeDraw() - End current Draw
# args: none
# return: str confirmation/error
def closeDraw():
    if os.path.exists("draw.json"):
        os.remove("draw.json")
        return "Sorteio encerrado"
    else:
        print("The file does not exist")
        return "Não existe sorteio em andamento" 

# newTicket(user) - Issues a ticket to user
# args: str user
# return: str confirmation/error
def newTicket(user):
    if(user == None ):
        return "Usuário não identificado"
    print("newTicket")    
    try:
        f = open("draw.json", "r")
        draw_dict = json.load(f)
        if(time.time() > (draw_dict['openTime']+draw_dict['duration']*60) ):
            f.close()
            return "Tempo Esgotado"
        else:
            with open("draw.json", "r+") as f:
                draw_dict = json.load(f)
                for key in draw_dict["users"]:
                    if(key==user):
                        return "Ticket já cadastrado e concorrendo"
                draw_dict['users'].append(user)
                f.seek(0,0)
                json.dump(draw_dict, f)
                f.close()
                return "Ticket cadastrado"             
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return "Não existe sorteio em andamento"

    finally:
        pass

# listParticipants() - List total participants already enrolled
# args: none
# return: str
# ADMIN_ONLY
def listParticipants():
    try:
        with open("draw.json", "r") as f:
            draw_dict = json.load(f)
            lista = ""
            i = 1
            for key in draw_dict["users"]:
                lista += str(i) + " - " + key + "\n"
                i += 1
            f.close()
            return lista
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return "Não existe sorteio em andamento"

# draw() - Selects winner
# args: none
# return:  str 
# ADMIN_ONLY
def draw():
    try:
        with open("draw.json", "r") as f:
            draw_dict = json.load(f)
            if(len(draw_dict["users"]) < 2):
                return "O sorteio precisa ter no mínimo 2 participantes"
            winner = random.randrange(0,len(draw_dict["users"])-1)
            f.close()
            return "O vencedor é " + draw_dict["users"][winner]
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return "Não existe sorteio em andamento" 

# checktime()
# args: none
# returns: str remaining time in hh:mm:ss format
def checkTime():
    try:
        f = open("draw.json", "r")
        draw_dict = json.load(f)
        if(time.time() > (draw_dict['openTime']+draw_dict['duration']*60) ):
            f.close()
            return "Tempo Esgotado"
        f.close()
        return "Tempo restante " + str(datetime.timedelta(seconds=((draw_dict['openTime']+draw_dict['duration']*60) - time.time()))).split(".")[0]
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return "Não existe sorteio em andamento" 


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