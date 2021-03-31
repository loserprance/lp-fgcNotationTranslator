# packages/dependancies
from PIL import Image, ImageFont, ImageDraw
import sys, json

# NEXT STEPS:
# translating notation other than numpad (cr.mk...)
# custom translating ("shoryuken" -> "623P"...)
# repair image function/incorporate into wiki function

# different "languages" of fg notation exist...capcom (jab,short,fierce), numpad, snk?
# numpad notation is used as a base for directions and motions
notation = {
    "directions": {
        "1" : {
            "full" : "down-back",
            "abbreviation": "d/b",
            "state": "crouching",
            "stateAbv": "cr.",
        },
        "2" : {
            "full" : "down",
            "abbreviation": "d",
            "state": "crouching",
            "stateAbv": "cr.",
        },
        "3" : {
            "full" : "down-forward",
            "abbreviation": "d/f",
            "state": "crouching",
            "stateAbv": "cr.",
        },
        "4" : {
            "full" : "back",
            "abbreviation": "b",
            "state": "back",
            "stateAbv": "b.",
        },
        "5" : {
            "full" : "neutral",
            "abbreviation": "n",
            "state": "standing",
            "stateAbv": "st.",
        },
        "6" : {
            "full" : "forward",
            "abbreviation": "f",
            "state": "towards",
            "stateAbv": "f.",
        },
        "7" : {
            "full" : "up-back",
            "abbreviation": "u/b",
            "state": "jumping",
            "stateAbv": "j.",
        },
        "8" : {
            "full" : "up",
            "abbreviation": "u",
            "state": "neutral jumping",
            "stateAbv": "nj.",
        },
        "9" : {
            "full" : "up-forward",
            "abbreviation": "u/f",
            "state": "jumping",
            "stateAbv": "j.",
        }
    },
    "motions": {
        "236": {
            "abbreviation": "qcf",
            "full" : "Quarter-Circle Forward"
        },
        "214": {
            "abbreviation": "qcb",
            "full" : "Quarter-Circle Back"
        },
        "41236": {
            "abbreviation": "hcf",
            "full" : "Half-Circle Forward"
        },
        "63214": {
            "abbreviation": "hcb",
            "full" : "Half-Circle Back"
        },
        "623": {
            "abbreviation": "dp",
            "full" : "Dragon Punch"
        },
        "421": {
            "abbreviation": "rdp",
            "full" : "Reverse Dragon Punch"
        },
        "6321478": {
            "abbreviation": "360",
            "full" : "360"
        },
        "2369": {
            "abbreviation": "tk",
            "full" : "Tiger Knee"
        },
        "412": {
            "abbreviation": "bdbd",
            "full" : "Back, Down-Back, Down"
        },
        "632": {
            "abbreviation": "fdfd",
            "full" : "Forward, Down-Forward, Down"
        }
    },
    "buttons": {
        "sf": {
            "LP": {
                "boomer": "Jab",
                "strength" : "Light",
                "attack" : "Punch"
            },
            "MP": {
                "boomer": "Strong",
                "strength" : "Medium",
                "attack" : "Punch"
            },
            "HP": {
                "boomer": "Fierce",
                "strength" : "Heavy",
                "attack" : "Punch"
            },
            "LK": {
                "boomer": "Short",
                "strength" : "Light",
                "attack" : "Kick"
            },
            "MK": {
                "boomer": "Forward",
                "strength" : "Medium",
                "attack" : "Kick"
            },
            "HK": {
                "boomer": "Roundhouse",
                "strength" : "Heavy",
                "attack" : "Kick"
            },
            "PP": {
                "strength" : "EX",
                "attack" : "Punch"
            },
            "KK": {
                "strength" : "EX",
                "attack" : "Kick"
            }
        }
    }
}


def getNextMove():
    try:
        # print("    Current move: " + moveArr[moveArrCurrentIndex])
        # print("    Next move: " + moveArr[moveArrCurrentIndex+1])
        return(moveArr[moveArrCurrentIndex+1])
    except:
        return(None)

def wikiMarkdownCreation(input):
    moveArr = []
    inputContentsArr = []
    moveArrCurrentIndex = 0
    inputContentsArrCurrentIndex = 0
    result = ""

    print("Input: " + str(input))
    syntaxChecking(input)

    input = input.replace(",", " ,")
    # input contents array population
    split = input.split(" ")
    for move in split:
        moveArr.append(move)
        inputContentsArr.append(parseMoveType(move))

        # print("\"" + move + "\"")
        # print("return data: " + str(moveTranslation(move)))
        # print("move is: " + str(parseMoveType(move)))
        # print(" ")

    print("moveArr: " + str(moveArr))
    print("inputContentsArr: " + str(inputContentsArr) + "\n----")

    for move in split:
        nextMove = getNextMove()
        currentMoveType = parseMoveType(move)
        nextMoveType = parseMoveType(nextMove)

        if (currentMoveType == None):
            pass
        elif (currentMoveType == "button"):
            validDirections = moveTranslation(move)["directions"]

            if isinstance(validDirections, list):
                if (validDirections == ["1", "2", "3"]):
                    direction = "2"
                elif (len(validDirections) == 1):
                    direction = str(validDirections[0])
            else:
                direction = str(validDirections)

            btn = moveTranslation(move)["btn"].lower()
            numOfHits = moveTranslation(move)["numOfHits"]

            dirAbv = notation["directions"][direction]["abbreviation"]

            if (dirAbv.lower() != "n"):
                result += f"[[File:{dirAbv}.png]] + "

            if (str(numOfHits) == "0"):
                result += f"[[File:{btn}.png]] "
            else:
                result += f"[[File:{btn}.png]] ({numOfHits}) "

            inputContentsArrCurrentIndex += 1
            moveArrCurrentIndex += 1
        elif (currentMoveType == "motion"):
            # print(moveTranslation(move))
            motionNum = moveTranslation(move)["motionNum"]
            btn = moveTranslation(move)["btn"].lower()

            motionAbv = notation["motions"][motionNum]["abbreviation"]

            result += f"[[File:{motionAbv}.png]] + [[File:{btn}.png]] "

            inputContentsArrCurrentIndex += 1
            moveArrCurrentIndex += 1
        elif (currentMoveType == "charge"):
            # print(moveTranslation(move))
            hold = moveTranslation(move)["hold"]
            release = moveTranslation(move)["release"]
            btn = moveTranslation(move)["btn"].lower()

            if (hold.isdigit()):
                holdAbv = notation["directions"][hold]["abbreviation"]
            else:
                holdAbv = hold

            if (release.isdigit()):
                releaseAbv = notation["directions"][release]["abbreviation"]
            else:
                releaseAbv = release

            result += f"[[File:{holdAbv}.png]][[File:{releaseAbv}.png]] + [[File:{btn}.png]] "

        elif (currentMoveType == ","):
            result = result[:len(result) -1] + f"{move} "
            pass
        else:
            inputContentsArrCurrentIndex += 1
            moveArrCurrentIndex += 1
            result += f"{move} "

    print("Result:\n" + result + "\n--------")

def syntaxChecking(string):
    if ("(" in string or ")" in string):
        lpi = [i for i, c in enumerate(string) if c == "("]
        rpi = [i for i, c in enumerate(string) if c == ")"]
        if (len(lpi) != len(rpi)):
            print("Syntax error; uneven amount of parentheses in string \"" + string + "\", exiting")
            # exception later/if necessary
            sys.exit(1)
    if ("[" in string or "]" in string):
        lbi = [i for i, c in enumerate(string) if c == "["]
        rbi = [i for i, c in enumerate(string) if c == "]"]
        if (len(lbi) != len(rbi)):
            print("Syntax error; uneven amount of brackets in string \"" + string + "\", exiting")
            # exception later/if necessary
            sys.exit(1)

def whichNotation(move):
    if (move == ">" or move == "xx" or move == ","):
        return
   
    if (move[0].isdigit() or move[1].isdigit()):
        # print(f"Assuming move {move} is in numpad notation")
        return("numpad")
    else:
        # print(f"Assuming move {move} is not in numpad notation")
        return("capcom")

def parseMoveType(move):
    if (move == None):
        return
    if (move == ">"):
        return(">")
    elif (move == "xx"):
        return("xx")
    elif (move == ","):
        return(",")

    moveNotation = whichNotation(move)

    # if there are brackets in this move, this is a charge move ("[2]8LK... or [d]u+lk?")
    if (("[" in move or "]" in move)):
        return("charge")
    else:
        if (moveNotation == "numpad"):
            try:
                # else, if we're in numpad notation and the second character of this move is a number, this is a motion (ie. 236HP)
                if ((move[1]).isdigit()):
                    return("motion")
            except:
                pass
            else:
                # else, it's numpad notation for a direction + a button (ie. 2MK)
                return("button")
        elif (moveNotation == "capcom"):
            for motionKey in notation["motions"]:
                # if the first letters of the move match up to a possible motion written in capcom, this is a motion (ie. qcf+lk)
                if (notation["motions"][motionKey]["abbreviation"] == move[0:len(notation["motions"][motionKey]["abbreviation"])]):
                    return("motion")

            for btnKey in notation["buttons"]["sf"]:
                if ("(" in move or ")" in move):
                    lpi = [i for i, c in enumerate(move) if c == "("]
                    move = move[0:lpi[0]]

                btnLength = len(btnKey)
                # if the last letters of the move match up to a possible button written in capcom, this is a button (ie. cr.mk)
                if (btnKey.lower() == move[-btnLength:].lower()):
                    return("button")

# customTranslations = {"236*K": "Lightning Legs", "[1/2/3]7/8/9*K" : "Spinning Bird Kick"};
customTranslations = {
    "Shoryuken": {
        "input" : "623*P",
        "moveType" : "motion",
        "aliases" : ["dp", "shoryu"]
    }
}

def customTranslationParsing():
    # custom translation handling
    for input in customTranslations.keys():
        print("Key (input): " + input)
        print("Value (name): " + customTranslations[input])
        kp = input.partition("*")
        print("input.partition(\"*\"): " + str(kp) + "\n")


def moveTranslation(move):
    # moves of any language will return numpad here
    moveType = parseMoveType(move)
    notationType = whichNotation(move)

    if (moveType == None):
        pass
    elif (moveType == "xx"):
        return("xx")
    elif (moveType == ">"):
        return(">")
    elif (moveType == ","):
        return(",")

    if (notationType == "numpad"):

        if (moveType == "charge"):
            lbi = move.index("[")+1
            rbi = move.index("]")

            hold = move[lbi:rbi]
            release = move[rbi+1:rbi+2]
            btn = move[4] + move[5]

            return({"hold": hold, "release": release, "btn": btn})
        elif (moveType == "motion"):
            if (len(move) != 3 and int(move[0:2]) > 9):
                attackStrengths = ["L", "M", "H"]
                for element in attackStrengths:
                    if (move.partition(element)[2] != ""):
                        motionNum = move.partition(element.upper())[0]
                        btn =  move.partition(element.upper())[1] + move.partition(element.upper())[2]

                        return({"motionNum": motionNum, "btn": btn})
        elif (moveType == "button"):
            direction = move[0]
            btn = move[1]+move[2]
            if (("(" in move or ")" in move)):
                numOfHits = move[4]
            else:
                numOfHits = 0

            return({"directions": direction, "btn": btn, "numOfHits": numOfHits})
    elif (notationType == "capcom"):

        def findBtn():
            for btnKey in notation["buttons"]["sf"]:
                btnLength = len(btnKey)
                # if the last letters of the move match up to a possible button written in capcom, this is a button (ie. cr.mk)
                if (btnKey.lower() == move[-btnLength:].lower()):
                    return(btnKey)

        if (moveType == "charge"):

            lbi = move.index("[")+1
            rbi = move.index("]")

            hold = move[lbi:rbi]
            release = move[rbi+1:rbi+2]

            btn = findBtn()

            return({"hold": hold, "release": release, "btn": btn})
        elif (moveType == "motion"):
            for motionKey in notation["motions"]:
                # if the first letters of the move match up to a possible motion written in capcom, this is a motion (ie. qcf+lk)
                if (notation["motions"][motionKey]["abbreviation"] == move[0:len(notation["motions"][motionKey]["abbreviation"])]):
                    motionNum = motionKey

            btn = findBtn()

            return({"motionNum": motionNum, "btn": btn})
        elif (moveType == "button"):

            if (len(move) == 2):
                directions = 5
               
            if ("(" in move or ")" in move):
                numOfHits = move[move.index("(")+1:move.index(")")]
                lpi = [i for i, c in enumerate(move) if c == "("]
                rpi = [i for i, c in enumerate(move) if c == ")"]
                move = move[0:lpi[0]]
            else:
                numOfHits = 0

            btn = findBtn()

            if ("." in move):
                dotIndex = move.index(".")
                directionStateAbv = ""
                directions = []
                for key in notation["directions"]:
                    if (notation["directions"][key]["stateAbv"] == move[0:dotIndex+1]):
                        directions.append(key)

            return({"directions": directions, "btn": btn, "numOfHits": numOfHits})

# customTranslationParsing()
numpadString = "2HP(1) > 236LK, 2LP > [2]8LK"
capcomString = "cr.hp(1) > qcf+lk, cr.lp > [d]u+lk"
# imageCreation(toTranslate)
wikiMarkdownCreation(numpadString)
wikiMarkdownCreation(capcomString)
wikiMarkdownCreation("5MP, 5HP")
wikiMarkdownCreation("MP, 5HP")
wikiMarkdownCreation("5MP, HP")
wikiMarkdownCreation("MP, HP")
