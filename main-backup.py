# packages/dependancies
from PIL import Image, ImageFont, ImageDraw
import sys, json

# NEXT STEPS:
# custom translating ("shoryuken" -> "623P"...)
# reimplement image function/incorporate into wiki function

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

    # if there are any custom move definitions in the string,
    if ("custom" in inputContentsArr):
        # their indexes in inputContentsArr are stored in this dict
        cmi = {}
        # if there are multiple values in inputContentsArr labeled as "custom" following each other, they must be referencing one move with multiple words (ie. "lightning legs")
        # to catch this, a "streak" is kept for as long as we keep running into concurrent "custom" values, and when it ends, begin searching for another custom definition
        customStreak = False
        customPhraseNum = 1

        for loopIndex, value in enumerate(inputContentsArr):
            if (value == "custom"):
                if customStreak:
                    cmi[f"custom{customPhraseNum}"]["indexes"].append(loopIndex)
                else:
                    try:
                        cmi[f"custom{customPhraseNum}"]["indexes"].append(loopIndex)
                    except:
                        cmi[f"custom{customPhraseNum}"] = { "indexes": [], "moveName": "" }
                        cmi[f"custom{customPhraseNum}"]["indexes"].append(loopIndex)
                    customStreak = True
            else:
                customStreak = False
                if (cmi != {}):
                    customPhraseNum += 1

        # next: inspect each key in cmi, relate the contents of the indexes for each to keys in customTranslations...
        # use that info to replace "shoryuken" with 623*P, dp+hp, whatever in the end result/on an image

        # custom1, custom2...
        for cmiKey in cmi:
            # ["4", "5"], ["6"]...
            customMovePiecedFromMoveArr = ""
            for cmiKeyIndex in cmi[cmiKey]["indexes"]:
                customMovePiecedFromMoveArr += moveArr[cmiKeyIndex] + " "

                # "Shoryuken", "Hadoken"...
                for customMove in customTranslations:
                    if (customMovePiecedFromMoveArr[:-1].lower() == customMove.lower()):
                        cmi[cmiKey]["moveName"] = customMove

        print(cmi)
    for move in split:
        nextMove = getNextMove()
        currentMoveType = parseMoveType(move)
        nextMoveType = parseMoveType(nextMove)

        if (currentMoveType == None):
            pass
        elif (currentMoveType == "custom"):
            print("MY FRIEND JUST GOT DOWNED")
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

        elif (currentMoveType == "motion"):
            # print(moveTranslation(move))
            motionNum = moveTranslation(move)["motionNum"]
            btn = moveTranslation(move)["btn"].lower()

            motionAbv = notation["motions"][motionNum]["abbreviation"]

            result += f"[[File:{motionAbv}.png]] + [[File:{btn}.png]] "
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

            result += f"[ [[File:{holdAbv}.png]] ] [[File:{releaseAbv}.png]] + [[File:{btn}.png]] "

        elif (currentMoveType == ","):
            result = result[:len(result) -1] + f"{move} "
            pass
        else:
            result += f"{move} "

        inputContentsArrCurrentIndex += 1
        moveArrCurrentIndex += 1
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

    return("custom")

customTranslations = {
    "Shoryuken": {
        "input" : {
            "dirOrMotion" : "623",
            "strength" : "*",
            "attack" : "Punch"
        },
        "moveType" : "motion",
        "aliases" : ["dp", "shoryu"]
    },
    "Donkey Kick": {
        "input" : {
            "dirOrMotion" : "41236",
            "strength" : "*",
            "attack" : "Kick"
        },
        "moveType" : "motion",
        "aliases" : ["dk"]
    },
    "Hadoken": {
        "input" : {
            "dirOrMotion" : "236",
            "strength" : "*",
            "attack" : "Punch"
        },
        "moveType" : "motion",
        "aliases" : ["fireball", "fb", "hadouken"]
    }
}

def moveTranslation(move):
    # moves of any language will return numpad here
    moveType = parseMoveType(move)
    notationType = whichNotation(move)

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

numpadString = "2HP(1) > 236LK, 2LP > [2]8LK"
capcomString = "cr.hp(1) > qcf+lk, cr.lp > [d]u+lk"
# imageCreation(toTranslate)
# wikiMarkdownCreation(numpadString)
# wikiMarkdownCreation(capcomString)
wikiMarkdownCreation("st.hk, st.lk > donkey kick > shoryuken")
# wikiMarkdownCreation("st.hk, st.lk > lightning legs > qcf+hp")
# wikiMarkdownCreation("st.mp, cr.hp > tatsu > donkey kick")
