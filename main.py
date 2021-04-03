# packages/dependancies
from PIL import Image, ImageFont, ImageDraw
import sys

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
    moveArr = []            # list of moves from received input split by spaces (st.hk, 2MK, lightning legs, etc.)
    moveTypeArr = []        # list of move types of moves from moveArr (button, charge, motion, custom, etc.)
    moveArrCurrentIndex = 0 # index of move currently being inspected in moveArr
    wikiText = ""           # contains a string of text meant for use on a wiki like srk wiki, taken from translated input
    customPhraseNum = 0     # used for following variable "cmi". goes up when the next word being inspected in moveArr is not a custom word, so we know when to start categorizing the next custom move

    print("Input: " + str(input) + "\n----")
    syntaxChecking(input)

    # input contents array population
    input = input.replace(",", " ,") # used to split commas properly; commas denote links, ">", "xx" denote cancels
    split = input.split(" ")
    for move in split:
        moveArr.append(move)
        moveTypeArr.append(parseMoveType(move))

    print("moveArr:     " + str(moveArr))
    print("moveTypeArr: " + str(moveTypeArr) + "\n----")

    # if there are any custom move definitions in the list,
    if ("custom?" in moveTypeArr):
        # their indexes in moveTypeArr (and later the name of the custom move if there's a match in the customTranslations dict) are stored in the dict "cmi"
        cmi = {}
        # if there are multiple values in moveTypeArr labeled as "custom" following each other, they must be referencing one move with multiple words (ie. "lightning legs")
        # to catch this, a "streak" is kept for as long as we keep running into concurrent "custom" values
        customStreak = False
        streakJustIncremented = False
        # when the streak ends, continue combing the list for the next occurence of a custom definition

        # loop through moveTypeArr to find all indexes that correspond to custom definitions look for
        for loopIndex, value in enumerate(moveTypeArr):
            if (value == "custom?"):
                if customStreak:
                    cmi[f"custom{customPhraseNum+1}"]["indexes"].append(loopIndex)
                else:
                    try:
                        cmi[f"custom{customPhraseNum+1}"]["indexes"].append(loopIndex)
                    except:
                        cmi[f"custom{customPhraseNum+1}"] = { "indexes": [], "moveName": "" }
                        cmi[f"custom{customPhraseNum+1}"]["indexes"].append(loopIndex)
                    customStreak = True
            else:
                customStreak = False
                if (cmi != {}):
                    if (not streakJustIncremented):
                        customPhraseNum += 1
                        streakJustIncremented = True

        # after looping through moveTypeArr to populate cmi with custom move definition instances and list indexes, this loop is for
        # finding which custom moves are meant to take the space of those indexes by checking to see if there are any matches between
        # keys in customTranslations and words in moveArr
       
        # custom1, custom2...
        for cmiKey in cmi:
            customMovePiecedFromMoveArr = ""
            # ["4", "5"], ["6"]...
            for cmiKeyIndex in cmi[cmiKey]["indexes"]:
                customMovePiecedFromMoveArr += moveArr[cmiKeyIndex] + " "
                # "Shoryuken", "Hadoken"...
                for customMove in customTranslations:
                    # todo: compare element in moveArr to alias
                    if (customMovePiecedFromMoveArr[:-1].lower() == customMove.lower()):
                        cmi[cmiKey]["moveName"] = customMove

        # next, custom move definitions that have move names containing spaces or multiple words that take up
        # multiple elements of the moveArr (and subsequently moveTypeArr) are combined into one entry, the
        # extras being deleted. this is also where move types are changed from "custom?" to "custom"
        def trimArrays(customPhraseNum):
            for i in range(customPhraseNum):
                numOfCustoms = len(cmi[f"custom{i+1}"]["indexes"])
                indexFirstElement = cmi[f"custom{i+1}"]["indexes"][0]
                indexLastElement = cmi[f"custom{i+1}"]["indexes"][-1]
                # print(f"indexes first element: " + str(indexFirstElement))
                # print(f"indexes last element: " + str(indexLastElement))

                # joining elements together/trimming moveTypeArr
                if (indexFirstElement != indexLastElement):
                    # print(f"seeking to replace {moveArr[int(indexFirstElement):int(indexLastElement+1)]} with {[' '.join(moveArr[int(indexFirstElement):int(indexLastElement+1)])]} ")
                    moveArr[indexFirstElement] = [' '.join(moveArr[int(indexFirstElement):int(indexLastElement+1)])][0]

                    for x in range(numOfCustoms):
                        if (x != 0):
                            moveArr[cmi[f"custom{i+1}"]["indexes"][x]] = "toDel"

                if (len(cmi[f"custom{i+1}"]["indexes"]) == 1):
                    moveTypeArr[cmi[f"custom{i+1}"]["indexes"][0]] = "custom"
                else:
                    indexToCutoff = cmi[f"custom{i+1}"]["indexes"][1]

                    for x in range(numOfCustoms):
                        if (x == 0):
                            moveTypeArr[cmi[f"custom{i+1}"]["indexes"][x]] = "custom"
                        else:
                            moveTypeArr[cmi[f"custom{i+1}"]["indexes"][x]] = "toDel"

            while ("toDel" in moveArr):
                moveArr.remove("toDel")
            while ("toDel" in moveTypeArr):
                moveTypeArr.remove("toDel")

            arraysToReturn = []
            arraysToReturn.append(moveArr)
            arraysToReturn.append(moveTypeArr)
            return(arraysToReturn)

        # final update and state of arrays
        newArrays = trimArrays(customPhraseNum)
        moveArr = newArrays[0]
        moveTypeArr = newArrays[1]

        print("Final state of arrays:")
        print("moveArr:     " + str(moveArr))
        print("moveTypeArr: " + str(moveTypeArr))

    for index, move in enumerate(moveArr):
        nextMove = getNextMove()
        currentMoveType = parseMoveType(move)
        nextMoveType = parseMoveType(nextMove)

        if (currentMoveType == None):
            pass
        elif (currentMoveType == "custom?"):
            # todo/ideas:
            # if movename contains light, medium, heavy...
            # compare element in moveArr to alias
            for customKey in customTranslations:
                if (customKey.lower() == move.lower()):
                    if (customTranslations[customKey]["moveType"] == "motion"):
                        motionNum = moveTranslation(customKey, currentMoveType)["motionNum"]
                        btn = moveTranslation(customKey, currentMoveType)["btn"].lower()

                        if (btn[0] == "*"):
                            btn = btn[1]

                        motionAbv = notation["motions"][motionNum]["abbreviation"]
                        wikiText += f"[[File:{motionAbv}.png]] + [[File:{btn}.png]] "

        elif (currentMoveType == "button"):
            validDirections = moveTranslation(move, currentMoveType)["directions"]

            if isinstance(validDirections, list):
                if (validDirections == ["1", "2", "3"]):
                    direction = "2"
                elif (len(validDirections) == 1):
                    direction = str(validDirections[0])
            else:
                direction = str(validDirections)

            btn = moveTranslation(move, currentMoveType)["btn"].lower()
            numOfHits = moveTranslation(move, currentMoveType)["numOfHits"]

            dirAbv = notation["directions"][direction]["abbreviation"]

            if (dirAbv.lower() != "n"):
                wikiText += f"[[File:{dirAbv}.png]] + "

            if (str(numOfHits) == "0"):
                wikiText += f"[[File:{btn}.png]] "
            else:
                wikiText += f"[[File:{btn}.png]] ({numOfHits}) "

        elif (currentMoveType == "motion"):
            motionNum = moveTranslation(move, currentMoveType)["motionNum"]
            btn = moveTranslation(move, currentMoveType)["btn"].lower()

            motionAbv = notation["motions"][motionNum]["abbreviation"]

            wikiText += f"[[File:{motionAbv}.png]] + [[File:{btn}.png]] "
        elif (currentMoveType == "charge"):
            hold = moveTranslation(move, currentMoveType)["hold"]
            release = moveTranslation(move, currentMoveType)["release"]
            btn = moveTranslation(move, currentMoveType)["btn"].lower()

            if (hold.isdigit()):
                holdAbv = notation["directions"][hold]["abbreviation"]
            else:
                holdAbv = hold

            if (release.isdigit()):
                releaseAbv = notation["directions"][release]["abbreviation"]
            else:
                releaseAbv = release

            wikiText += f"[ [[File:{holdAbv}.png]] ] [[File:{releaseAbv}.png]] + [[File:{btn}.png]] "

        elif (currentMoveType == ","):
            wikiText = wikiText[:len(wikiText) -1] + f"{move} "
            pass
        else:
            wikiText += f"{move} "

        moveArrCurrentIndex += 1
    print("\n" + wikiText + "\n--------")

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

    return("custom?")

customTranslations = {
    "Shoryuken": {
        "input" : {
            "numpadInput" : "623",
            "strength" : "*",
            "attack" : "Punch"
        },
        "moveType" : "motion",
        "aliases" : ["dp", "shoryu"]
    },
    "Spinning Bird Kick": {
        "input" : {
            "numpadInput" : "[2]8",
            "strength" : "*",
            "attack" : "Kick"
        },
        "moveType" : "charge",
        "aliases" : ["sbk"]
    },
    "Lightning Legs": {
        "input" : {
            "numpadInput" : "236",
            "strength" : "*",
            "attack" : "Kick"
        },
        "moveType" : "motion",
        "aliases" : ["legs", "hyak"]
    },
    "Donkey Kick": {
        "input" : {
            "numpadInput" : "41236",
            "strength" : "*",
            "attack" : "Kick"
        },
        "moveType" : "motion",
        "aliases" : ["dk"]
    },
    "Hadoken": {
        "input" : {
            "numpadInput" : "236",
            "strength" : "*",
            "attack" : "Punch"
        },
        "moveType" : "motion",
        "aliases" : ["fireball", "fb", "hadouken"]
    },
    "big big brongus": {
        "input" : {
            "numpadInput" : "236",
            "strength" : "*",
            "attack" : "Punch"
        },
        "moveType" : "motion",
        "aliases" : ["fireball", "fb", "hadouken"]
    }
}

def moveTranslation(m, mt):
    # moves of any language will return numpad here
    move = m
    moveType = mt

    notationType = whichNotation(move)

    if (mt == "custom?"):
        # print(customTranslations[move])
        # print("CUSTOM IN MOVE TRANSLATION!")

        numpadInput = customTranslations[m]["input"]["numpadInput"]
        strength = customTranslations[m]["input"]["strength"]
        attack = customTranslations[m]["input"]["attack"][0]

        moveType = customTranslations[m]["moveType"]
        notationType = "numpad"

        move = str(numpadInput) + str(strength) + str(attack)
        print(f"{m} -> {move}")

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
                attackStrengths = ["L", "M", "H", "*", "EX", "l", "m", "h", "eX", "Ex", "ex"]
                for element in attackStrengths:
                    if (move.partition(element)[2] != ""):
                        motionNum = move.partition(element)[0]
                        btn = move.partition(element)[1].upper() + move.partition(element)[2].upper()

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
# wikiMarkdownCreation("st.hk, st.lk > shoryuken > big big brongus > donkey kick")
# wikiMarkdownCreation("st.hk, st.lk > big big brongus")
wikiMarkdownCreation("st.hK, st.Lk > 236lp > lightning legs > qcf+hp")
# wikiMarkdownCreation("st.mp, cr.hp > tatsu > donkey kick")
