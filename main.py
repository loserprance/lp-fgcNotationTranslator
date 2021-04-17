# packages/dependancies
from PIL import Image, ImageFont, ImageDraw
import sys

# NEXT STEPS AND GOALS:
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

# custom user defined moves; special moves, unique attacks, game-specific information...
# dicts of movelists from specific fighting games could be added (sfv)
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
    "Tatsumaki Senpukyaku": {
        "input" : {
            "numpadInput" : "214",
            "strength" : "*",
            "attack" : "Kick"
        },
        "moveType" : "motion",
        "aliases" : ["tatsu", "hurricane"]
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
    }
}

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

def parseMoveNotation(move):
    if (move == "xx" or move == ">"):
        return("cancel")
    elif (move == ","):
        return("link")

    if (move[0].isdigit() or move[1].isdigit()):
        return("numpad")
    else:
        return("capcom")

def parseMoveType(move):
    if (move == None):
        return
    elif (move == "xx" or move == ">"):
        return("cancel")
    elif (move == ","):
        return("link")

    moveNotation = parseMoveNotation(move)

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

def parseInput(input):
    moveDict = {}  # dict of input split move by move with all relevant information stored
    resultArr = [] # list of moves to combine into string once text processing has finished

    print("Input: " + str(input) + "\n----")
    syntaxChecking(input)

    # array population
    input = input.replace(",", " ,") # used to split commas properly; commas denote links, ">", "xx" denote cancels
    split = input.split(" ")
    for i, move in enumerate(split):
        moveDict[i] = {}
        moveDict[i]["move"] = move
        moveDict[i]["moveType"] = parseMoveType(move)
        if (moveDict[i]["moveType"] == "custom?" or moveDict[i]["moveType"] == "custom"):
            moveDict[i]["moveNotation"] = "custom"
        else:
            moveDict[i]["moveNotation"] = parseMoveNotation(move)

    # if there are any custom move definitions that need to be turned into notation,
    # their indexes in moveDict are stored in the dict "cmi"
    cmi = {}
    customPhraseNum = 1 # goes up when the next word being inspected in moveDict is not a custom word, so we know when to start categorizing the next custom move
    # if there are multiple moves with moveType "custom?" occuring in moveDict sequentially, they must be referencing one move with multiple words (ie. "lightning legs")
    # to catch this, a "streak" is kept for as long as we keep running into concurrent "custom" values
    customStreak = False
    streakJustIncremented = False
    # when the streak ends, continue combing the list for the next occurence of a custom definition
    for i in moveDict:
        move = moveDict[i]
        moveNotation = moveDict[i]["moveNotation"]

        if (moveNotation == "custom"):
            # print(f"    Custom streak?: {customStreak}")
            # print(f"    Streak just incremented?: {streakJustIncremented}")
            # print(f"    Custom phrase num?: {customPhraseNum}")

            if (streakJustIncremented):
                streakJustIncremented = False
            if customStreak:
                cmi[f"custom{customPhraseNum}"]["indexes"].append(i)
            else:
                try:
                    cmi[f"custom{customPhraseNum}"]["indexes"].append(i)
                except:
                    cmi[f"custom{customPhraseNum}"] = { "indexes": [], "moveName": "" }
                    cmi[f"custom{customPhraseNum}"]["indexes"].append(i)
                customStreak = True
        else:
            customStreak = False
            if (cmi != {}):
                if (not streakJustIncremented):
                    customPhraseNum += 1
                    streakJustIncremented = True
                else:
                    streakJustIncremented = False

    customPhraseNum -= 1

    # after looping through moveDict move types to populate cmi with custom move definition instances and list indexes, this loop is for
    # finding which custom moves are meant to take the space of those indexes by checking to see if there are any matches between
    # keys in customTranslations and words in moveDict

    # custom1, custom2...
    for cmiKey in cmi:
        customMovePiecedFromMoveDict = ""
        # ["4", "5"], ["6"]...
        for cmiKeyIndex in cmi[cmiKey]["indexes"]:
            customMovePiecedFromMoveDict += moveDict[cmiKeyIndex]["move"]  + " "
            # "Shoryuken", "Hadoken"...
            for customMove in customTranslations:
                if (customMovePiecedFromMoveDict[:-1].lower() == customMove.lower()):
                    cmi[cmiKey]["moveName"] = customMove
                for alias in customTranslations[customMove]["aliases"]:
                    if (customMovePiecedFromMoveDict[:-1].lower() == alias.lower()):
                        cmi[cmiKey]["moveName"] = customMove
                        moveDict[cmi[cmiKey]["indexes"][0]]["move"] = customMove

    # next, custom move definitions that have move names containing spaces or multiple words that take up
    # multiple elements of the moveDict are combined into one entry, the
    # extras being deleted. this is also where move types are changed from "custom?" to "custom"

    def trimDict(customPhraseNum):
        for i in range(1,customPhraseNum+1):
            numOfCustoms = len(cmi[f"custom{i}"]["indexes"])
            indexFirstElement = cmi[f"custom{i}"]["indexes"][0]
            indexLastElement = cmi[f"custom{i}"]["indexes"][-1]

            if (indexFirstElement != indexLastElement):
                for x in range(numOfCustoms):
                    dictIndex = cmi[f"custom{i}"]["indexes"][x]
                    if (x == 0):
                        moveDict[dictIndex]["move"] = cmi[f"custom{i}"]["moveName"]
                        moveDict[dictIndex]["moveType"] = "custom"
                    else:
                        moveDict[dictIndex] = "toDel"
            else:
                dictIndex = indexFirstElement
                moveDict[dictIndex]["move"] = cmi[f"custom{i}"]["moveName"]
                moveDict[dictIndex]["moveType"] = "custom"

        return(moveDict)

    if (cmi != {}):
        moveDict = trimDict(customPhraseNum)

    # remove null'd elements from trimDict. fix indexes later?
    for i in range(len(moveDict)):
        if (moveDict[i] == "toDel"):
            del (moveDict[i])

    for i in moveDict:
        def findBtn(m):
            move = m

            if (move[-2] == "*"):
                return(move[-2:])

            for btnKey in notation["buttons"]["sf"]:
                btnLength = len(btnKey)
                # if the last letters of the move match up to a possible button written in capcom, this is a button (ie. cr.mk)
                if (btnKey.lower() == move[-btnLength:].lower()):
                    return(btnKey)

        move = moveDict[i]["move"]
        moveType = moveDict[i]["moveType"]
        moveNotation = moveDict[i]["moveNotation"]
        moveDict[i]["input"] = {}

        if (moveNotation == "custom"):
            m = move
            move = str(customTranslations[m]["input"]["numpadInput"]) + customTranslations[m]["input"]["strength"][0] + customTranslations[m]["input"]["attack"][0]
            # moveDict[i]["input"] = customTranslations[move]["input"]
            customMoveType = customTranslations[m]["moveType"]
            moveDict[i]["moveType"] = customMoveType

            if (customMoveType == "motion"):
                attackStrengths = ["L", "M", "H", "*", "EX", "l", "m", "h", "eX", "Ex", "ex"]
                for element in attackStrengths:
                    if (move.partition(element)[2] != ""):
                        motionNum = move.partition(element)[0]
                        moveDict[i]["input"]["motions"] = {}
                        moveDict[i]["input"]["motions"]["num"] = motionNum
                        moveDict[i]["input"]["motions"]["abv"] = notation["motions"][motionNum]["abbreviation"]
                        moveDict[i]["input"]["motions"]["word"] = notation["motions"][motionNum]["full"]

                moveDict[i]["input"]["button"] = {}
                btn = findBtn(move)
                moveDict[i]["input"]["button"]["shortform"] = btn
                if (btn[0] == "*"):
                    moveDict[i]["input"]["button"]["strWord"] = "Any"
                    moveDict[i]["input"]["button"]["attWord"] = customTranslations[m]["input"]["attack"]
                else:
                    moveDict[i]["input"]["button"]["strWord"] = notation["buttons"]["sf"][btn]["strength"]
                    moveDict[i]["input"]["button"]["attWord"] = notation["buttons"]["sf"][btn]["attack"]
                moveDict[i]["input"]["button"]["strAbv"] = btn[0]
                moveDict[i]["input"]["button"]["attAbv"] = btn[1]
                moveDict[i]["input"]["button"]["fullWords"] = moveDict[i]["input"]["button"]["strWord"] + " " + moveDict[i]["input"]["button"]["attWord"]
                moveDict[i]["input"]["button"]["attBoomer"] = None
            else:
                print("not adding additional data to moveDict for custom, functionality not implemented yet")

        if (moveNotation == "numpad"):
            if (moveType == "charge"):
                lbi = move.index("[")+1
                rbi = move.index("]")

                hold = move[lbi:rbi]
                holdDirections = []
                for numpadDirection in notation["directions"]:
                    if (hold == numpadDirection):
                        holdDirections.append(numpadDirection)
                        # state = notation["directions"][numpadDirection]["state"]
                        # for numpadDirection2 in notation["directions"]:
                            # if (state == notation["directions"][numpadDirection2]["state"]):
                                # holdDirections.append(numpadDirection2)

                release = move[rbi+1:rbi+2]
                releaseDirections = []
                for numpadDirection3 in notation["directions"]:
                    if (release == numpadDirection3):
                        releaseDirections.append(numpadDirection3)
                        # state = notation["directions"][numpadDirection3]["state"]
                        # for numpadDirection4 in notation["directions"]:
                            # if (state == notation["directions"][numpadDirection4]["state"]):
                                # releaseDirections.append(numpadDirection4)

                moveDict[i]["input"]["directions"] = {}
                moveDict[i]["input"]["directions"]["hold"] = {}
                moveDict[i]["input"]["directions"]["hold"]["dirNums"] = holdDirections
                moveDict[i]["input"]["directions"]["hold"]["dirAbvs"] = []
                moveDict[i]["input"]["directions"]["hold"]["dirWords"] = []
                moveDict[i]["input"]["directions"]["hold"]["dirStates"] = []
                moveDict[i]["input"]["directions"]["hold"]["dirStateAbvs"] = []

                for n in holdDirections:
                    moveDict[i]["input"]["directions"]["hold"]["dirAbvs"].append(notation["directions"][n]["abbreviation"])
                    moveDict[i]["input"]["directions"]["hold"]["dirWords"].append(notation["directions"][n]["full"])
                    moveDict[i]["input"]["directions"]["hold"]["dirStates"].append(notation["directions"][n]["state"])
                    moveDict[i]["input"]["directions"]["hold"]["dirStateAbvs"].append(notation["directions"][n]["stateAbv"])

                moveDict[i]["input"]["directions"]["release"] = {}
                moveDict[i]["input"]["directions"]["release"]["dirNums"] = releaseDirections
                moveDict[i]["input"]["directions"]["release"]["dirAbvs"] = []
                moveDict[i]["input"]["directions"]["release"]["dirWords"] = []
                moveDict[i]["input"]["directions"]["release"]["dirStates"] = []
                moveDict[i]["input"]["directions"]["release"]["dirStateAbvs"] = []

                for n in releaseDirections:
                    moveDict[i]["input"]["directions"]["release"]["dirAbvs"].append(notation["directions"][n]["abbreviation"])
                    moveDict[i]["input"]["directions"]["release"]["dirWords"].append(notation["directions"][n]["full"])
                    moveDict[i]["input"]["directions"]["release"]["dirStates"].append(notation["directions"][n]["state"])
                    moveDict[i]["input"]["directions"]["release"]["dirStateAbvs"].append(notation["directions"][n]["stateAbv"])

                btn = move[4] + move[5]
                moveDict[i]["input"]["button"] = {}
                moveDict[i]["input"]["button"]["shortform"] = btn
                moveDict[i]["input"]["button"]["strWord"] = notation["buttons"]["sf"][btn]["strength"]
                moveDict[i]["input"]["button"]["strAbv"] = btn[0]
                moveDict[i]["input"]["button"]["attWord"] = notation["buttons"]["sf"][btn]["attack"]
                moveDict[i]["input"]["button"]["attAbv"] = btn[1]
                moveDict[i]["input"]["button"]["fullWords"] = moveDict[i]["input"]["button"]["strWord"] + " " + moveDict[i]["input"]["button"]["attWord"]
                moveDict[i]["input"]["button"]["attBoomer"] = notation["buttons"]["sf"][btn]["boomer"]

            elif (moveType == "motion"):
                if (len(move) != 3 and int(move[0:2]) > 9):
                    attackStrengths = ["L", "M", "H", "*", "EX", "l", "m", "h", "eX", "Ex", "ex"]
                    for element in attackStrengths:
                        if (move.partition(element)[2] != ""):
                            motionNum = move.partition(element)[0]
                            moveDict[i]["input"]["motions"] = {}
                            moveDict[i]["input"]["motions"]["num"] = motionNum
                            moveDict[i]["input"]["motions"]["abv"] = notation["motions"][motionNum]["abbreviation"]
                            moveDict[i]["input"]["motions"]["word"] = notation["motions"][motionNum]["full"]

                            btn = move.partition(element)[1].upper() + move.partition(element)[2].upper()
                            moveDict[i]["input"]["button"] = {}
                            moveDict[i]["input"]["button"]["shortform"] = btn
                            moveDict[i]["input"]["button"]["strWord"] = notation["buttons"]["sf"][btn]["strength"]
                            moveDict[i]["input"]["button"]["strAbv"] = btn[0]
                            moveDict[i]["input"]["button"]["attWord"] = notation["buttons"]["sf"][btn]["attack"]
                            moveDict[i]["input"]["button"]["attAbv"] = btn[1]
                            moveDict[i]["input"]["button"]["fullWords"] = moveDict[i]["input"]["button"]["strWord"] + " " + moveDict[i]["input"]["button"]["attWord"]
                            moveDict[i]["input"]["button"]["attBoomer"] = notation["buttons"]["sf"][btn]["boomer"]

            elif (moveType == "button"):
                if (("(" in move or ")" in move)):
                    numOfHits = move[4]
                else:
                    numOfHits = 0

                direction = move[0]
                moveDict[i]["input"]["directions"] = {}
                moveDict[i]["input"]["directions"]["dirNums"] = [direction]
                moveDict[i]["input"]["directions"]["dirAbvs"] = []
                moveDict[i]["input"]["directions"]["dirWords"] = []
                moveDict[i]["input"]["directions"]["dirStates"] = []
                moveDict[i]["input"]["directions"]["dirStateAbvs"] = []

                moveDict[i]["input"]["directions"]["dirAbvs"].append(notation["directions"][direction]["abbreviation"])
                moveDict[i]["input"]["directions"]["dirWords"].append(notation["directions"][direction]["full"])
                moveDict[i]["input"]["directions"]["dirStates"].append(notation["directions"][direction]["state"])
                moveDict[i]["input"]["directions"]["dirStateAbvs"].append(notation["directions"][direction]["stateAbv"])

                btn = move[1]+move[2]
                moveDict[i]["input"]["button"] = {}
                moveDict[i]["input"]["button"]["shortform"] = btn
                moveDict[i]["input"]["button"]["strWord"] = notation["buttons"]["sf"][btn]["strength"]
                moveDict[i]["input"]["button"]["strAbv"] = btn[0]
                moveDict[i]["input"]["button"]["attWord"] = notation["buttons"]["sf"][btn]["attack"]
                moveDict[i]["input"]["button"]["attAbv"] = btn[1]
                moveDict[i]["input"]["button"]["fullWords"] = moveDict[i]["input"]["button"]["strWord"] + " " + moveDict[i]["input"]["button"]["attWord"]
                moveDict[i]["input"]["button"]["attBoomer"] = notation["buttons"]["sf"][btn]["boomer"]
                moveDict[i]["input"]["numOfHits"] = numOfHits

        elif (moveNotation == "capcom"):

            if (moveType == "button"):
                if ("(" in move or ")" in move):
                    numOfHits = move[move.index("(")+1:move.index(")")]
                    lpi = [i for i, c in enumerate(move) if c == "("]
                    rpi = [i for i, c in enumerate(move) if c == ")"]
                    move = move[0:lpi[0]]
                else:
                    numOfHits = 0
                moveDict[i]["input"]["button"] = {}
                btn = findBtn(move)
                moveDict[i]["input"]["button"]["shortform"] = btn
                moveDict[i]["input"]["button"]["strWord"] = notation["buttons"]["sf"][btn]["strength"]
                moveDict[i]["input"]["button"]["strAbv"] = btn[0]
                moveDict[i]["input"]["button"]["attWord"] = notation["buttons"]["sf"][btn]["attack"]
                moveDict[i]["input"]["button"]["attAbv"] = btn[1]
                moveDict[i]["input"]["button"]["fullWords"] = moveDict[i]["input"]["button"]["strWord"] + " " + moveDict[i]["input"]["button"]["attWord"]
                moveDict[i]["input"]["button"]["attBoomer"] = notation["buttons"]["sf"][btn]["boomer"]

                moveDict[i]["input"]["directions"] = {}
                if (len(move) == 2):
                    directions = ["5"]
                elif ("." in move):
                    dotIndex = move.index(".")
                    directionStateAbv = ""
                    directions = []
                    for key in notation["directions"]:
                        if (notation["directions"][key]["stateAbv"] == move[0:dotIndex+1]):
                            directions.append(key)
                    if (directions == ["1", "2", "3"]):
                        directions = ["2"]
                else:
                    print("failed to parse button with no period")

                moveDict[i]["input"]["directions"]["dirNums"] = directions
                moveDict[i]["input"]["directions"]["dirAbvs"] = []
                moveDict[i]["input"]["directions"]["dirWords"] = []
                moveDict[i]["input"]["directions"]["dirStates"] = []
                moveDict[i]["input"]["directions"]["dirStateAbvs"] = []

                for n in directions:
                    moveDict[i]["input"]["directions"]["dirAbvs"].append(notation["directions"][n]["abbreviation"])
                    moveDict[i]["input"]["directions"]["dirWords"].append(notation["directions"][n]["full"])
                    moveDict[i]["input"]["directions"]["dirStates"].append(notation["directions"][n]["state"])
                    moveDict[i]["input"]["directions"]["dirStateAbvs"].append(notation["directions"][n]["stateAbv"])

                moveDict[i]["input"]["numOfHits"] = numOfHits

            if (moveType == "motion"):
                moveDict[i]["input"]["button"] = {}
                btn = findBtn(move)
                moveDict[i]["input"]["button"]["shortform"] = btn
                moveDict[i]["input"]["button"]["strWord"] = notation["buttons"]["sf"][btn]["strength"]
                moveDict[i]["input"]["button"]["strAbv"] = btn[0]
                moveDict[i]["input"]["button"]["attWord"] = notation["buttons"]["sf"][btn]["attack"]
                moveDict[i]["input"]["button"]["attAbv"] = btn[1]
                moveDict[i]["input"]["button"]["fullWords"] = moveDict[i]["input"]["button"]["strWord"] + " " + moveDict[i]["input"]["button"]["attWord"]
                moveDict[i]["input"]["button"]["attBoomer"] = notation["buttons"]["sf"][btn]["boomer"]

                moveDict[i]["input"]["motions"] = {}
                for motionKey in notation["motions"]:
                    # if the first letters of the move match up to a possible motion written in capcom, this is a motion (ie. qcf+lk)
                    if (notation["motions"][motionKey]["abbreviation"] == move[0:len(notation["motions"][motionKey]["abbreviation"])]):
                        motionNum = motionKey

                moveDict[i]["input"]["motions"]["num"] = motionNum
                moveDict[i]["input"]["motions"]["abv"] = notation["motions"][motionNum]["abbreviation"]
                moveDict[i]["input"]["motions"]["word"] = notation["motions"][motionNum]["full"]

            if (moveType == "charge"):
                moveDict[i]["input"]["button"] = {}
                btn = findBtn(move)
                moveDict[i]["input"]["button"]["shortform"] = btn
                moveDict[i]["input"]["button"]["strWord"] = notation["buttons"]["sf"][btn]["strength"]
                moveDict[i]["input"]["button"]["strAbv"] = btn[0]
                moveDict[i]["input"]["button"]["attWord"] = notation["buttons"]["sf"][btn]["attack"]
                moveDict[i]["input"]["button"]["attAbv"] = btn[1]
                moveDict[i]["input"]["button"]["fullWords"] = moveDict[i]["input"]["button"]["strWord"] + " " + moveDict[i]["input"]["button"]["attWord"]
                moveDict[i]["input"]["button"]["attBoomer"] = notation["buttons"]["sf"][btn]["boomer"]

                lbi = move.index("[")+1
                rbi = move.index("]")

                hold = move[lbi:rbi]
                release = move[rbi+1:rbi+2]
                holdDirections = []
                releaseDirections = []

                for numpadDirection in notation["directions"]:
                    if (hold.lower() == notation["directions"][numpadDirection]["abbreviation"].lower()):
                        holdDirections.append(numpadDirection)
                        # state = notation["directions"][numpadDirection]["state"]
                        # for numpadDirection2 in notation["directions"]:
                            # if (state == notation["directions"][numpadDirection2]["state"]):
                                # holdDirections.append(numpadDirection2)

                for numpadDirection3 in notation["directions"]:
                    if (release.lower() == notation["directions"][numpadDirection3]["abbreviation"].lower()):
                        releaseDirections.append(numpadDirection3)
                        # state = notation["directions"][numpadDirection3]["state"]
                        # for numpadDirection4 in notation["directions"]:
                            # if (state == notation["directions"][numpadDirection4]["state"]):
                                # releaseDirections.append(numpadDirection4)

                moveDict[i]["input"]["directions"] = {}
                moveDict[i]["input"]["directions"]["hold"] = {}
                moveDict[i]["input"]["directions"]["hold"]["dirNums"] = holdDirections
                moveDict[i]["input"]["directions"]["hold"]["dirAbvs"] = []
                moveDict[i]["input"]["directions"]["hold"]["dirWords"] = []
                moveDict[i]["input"]["directions"]["hold"]["dirStates"] = []
                moveDict[i]["input"]["directions"]["hold"]["dirStateAbvs"] = []

                for n in holdDirections:
                    moveDict[i]["input"]["directions"]["hold"]["dirAbvs"].append(notation["directions"][n]["abbreviation"])
                    moveDict[i]["input"]["directions"]["hold"]["dirWords"].append(notation["directions"][n]["full"])
                    moveDict[i]["input"]["directions"]["hold"]["dirStates"].append(notation["directions"][n]["state"])
                    moveDict[i]["input"]["directions"]["hold"]["dirStateAbvs"].append(notation["directions"][n]["stateAbv"])

                moveDict[i]["input"]["directions"]["release"] = {}
                moveDict[i]["input"]["directions"]["release"]["dirNums"] = releaseDirections
                moveDict[i]["input"]["directions"]["release"]["dirAbvs"] = []
                moveDict[i]["input"]["directions"]["release"]["dirWords"] = []
                moveDict[i]["input"]["directions"]["release"]["dirStates"] = []
                moveDict[i]["input"]["directions"]["release"]["dirStateAbvs"] = []

                for n in releaseDirections:
                    moveDict[i]["input"]["directions"]["release"]["dirAbvs"].append(notation["directions"][n]["abbreviation"])
                    moveDict[i]["input"]["directions"]["release"]["dirWords"].append(notation["directions"][n]["full"])
                    moveDict[i]["input"]["directions"]["release"]["dirStates"].append(notation["directions"][n]["state"])
                    moveDict[i]["input"]["directions"]["release"]["dirStateAbvs"].append(notation["directions"][n]["stateAbv"])

    for i in moveDict:
        moveDictEntry = moveDict[i]
        move = moveDict[i]["move"]
        currentMoveType = moveDict[i]["moveType"]
        try:
            nextMoveType = moveDict[i+1]["moveType"]
        except:
            nextMoveType = None

        if (currentMoveType == None):
            pass
        elif (currentMoveType == "button"):
            validDirections = moveDictEntry["input"]["directions"]["dirNums"]

            if isinstance(validDirections, list):
                if (validDirections == ["1", "2", "3"]):
                    direction = "2"
                elif (len(validDirections) == 1):
                    direction = str(validDirections[0])
            else:
                direction = str(validDirections)

            btn = moveDictEntry["input"]["button"]["shortform"].lower()
            numOfHits = moveDictEntry["input"]["numOfHits"]

            dirAbv = notation["directions"][direction]["abbreviation"]

            if (dirAbv.lower() != "n"):
                resultArr.append(f"[[File:{dirAbv}.png]] ")
                resultArr.append(f"+ ")

            resultArr.append(f"[[File:{btn}.png]] ")
            if (str(numOfHits) != "0"):
                resultArr.append(f"({numOfHits}) ")

        elif (currentMoveType == "motion"):
            motionNum = moveDictEntry["input"]["motions"]["num"]
            motionAbv = notation["motions"][motionNum]["abbreviation"]
            btn = moveDictEntry["input"]["button"]["shortform"].lower()
            isPreviousElementBtn = False
            newBtn = ""

            print(resultArr)
            if (btn[0] == "*"):
                for key in notation["buttons"]["sf"]:
                    if (resultArr != []):
                        print(resultArr[-1])
                        if key.lower() in resultArr[-1].lower():
                            isPreviousElementBtn = True
                            newBtn = (resultArr[-1])[7:9]
                            del resultArr[-1]
            else:
                print(btn)

            if (isPreviousElementBtn):
                resultArr.append(f"[[File:{motionAbv}.png]] ")
                resultArr.append(f"+ ")
                resultArr.append(f"[[File:{newBtn}.png]] ")
            else:
                btn = btn[-1]
                resultArr.append(f"[[File:{motionAbv}.png]] ")
                resultArr.append(f"+ ")
                resultArr.append(f"[[File:{btn}.png]] ")
        elif (currentMoveType == "charge"):
            hold = moveDictEntry["input"]["directions"]["hold"]["dirNums"][0]
            release = moveDictEntry["input"]["directions"]["release"]["dirNums"][0]
            btn = moveDictEntry["input"]["button"]["shortform"].lower()

            if (hold.isdigit()):
                holdAbv = notation["directions"][hold]["abbreviation"]
            else:
                holdAbv = hold

            if (release.isdigit()):
                releaseAbv = notation["directions"][release]["abbreviation"]
            else:
                releaseAbv = release

            resultArr.append(f"[ [[File:{holdAbv}.png]] ] ")
            resultArr.append(f"[[File:{releaseAbv}.png]] ")
            resultArr.append(f"+ ")
            resultArr.append(f"[[File:{btn}.png]] ")
        elif (currentMoveType == ","):
            resultArr[-1] = (resultArr[-1])[0:len(resultArr[-1])-1]
            resultArr.append(", ")
            pass
        else:
            resultArr.append(f"{move} ")

    finalResult = ""
    for move in resultArr:
        print(move)
        finalResult += move
        # print(move)

    # print("--")
    # for i in moveDict:
        # move = moveDict[i]
        # moveType = moveDict[i]["moveType"]
        # print(f"{i}: {move}")

    print("--")
    print(finalResult)
    print("----\n")

numpadString = "2HP(1) > 236LK, 2LP > [2]8LK"
# capcomString = "cr.hp(1) > qcf+lk, cr.lp > Spinning Bird Kick"
# parseInput("cr.hp(1) > qcf+lk, cr.lp > HP shoryu, 3HK")

parseInput("LP fireball > MK fireball > HK lightning legs > shoryu")

# parseInput("LP fireball > MK fireball > HK lightning legs > shoryu, spinning bird kick > HK")
# parseInput("cr.hp(1) > qcf+lk, cr.lp > [d]u+lk, lightning legs, shoryuken")
# imageCreation(toTranslate)
# parseInput(numpadString)
# parseInput(capcomString)
