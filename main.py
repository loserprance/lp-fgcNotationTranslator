# packages/dependancies
from PIL import Image, ImageFont, ImageDraw
import sys, json

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
            "stateAbv": "s.",
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

moveArr = []
inputContentsArr = []

def getNextMove():
    try:
        # print("    Current move: " + moveArr[moveArrCurrentIndex])
        # print("    Next move: " + moveArr[moveArrCurrentIndex+1])
        return(moveArr[moveArrCurrentIndex+1])
    except:
        return(None)

def wikiMarkdownCreation(input):
    input = input.replace(",", " ,")
    # input contents array population
    inputContentsArrPush(input)
    inputContentsArrCurrentIndex = 0
    moveArrCurrentIndex = 0

    result = ""

    for move in input.split(" "):
        nextMove = getNextMove()
        nextMoveType = parseMoveType(nextMove)

        if (parseMoveType(move) == None):
            pass
        elif (parseMoveType(move) == "button"):
            direction = moveTranslation(move)["direction"]
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
        elif (parseMoveType(move) == "motion"):
            motionNum = moveTranslation(move)["motionNum"]
            btn = moveTranslation(move)["btn"].lower()

            motionAbv = notation["motions"][motionNum]["abbreviation"]
            result += f"[[File:{motionAbv}.png]] + [[File:{btn}.png]] "

            inputContentsArrCurrentIndex += 1
            moveArrCurrentIndex += 1
        elif (parseMoveType(move) == "charge"):
            hold = moveTranslation(move)["hold"]
            release = moveTranslation(move)["release"]
            btn = moveTranslation(move)["btn"].lower()

            holdAbv = notation["directions"][hold]["abbreviation"]
            releaseAbv = notation["directions"][release]["abbreviation"]

            result += f"[[File:{holdAbv}.png]][[File:{releaseAbv}.png]] + [[File:{btn}.png]] "

        elif (parseMoveType(move) == ","):
            result = result[:len(result) -1] + f"{move} "
            pass
        else:
            inputContentsArrCurrentIndex += 1
            moveArrCurrentIndex += 1
            result += f"{move} "

    print("Result:\n" + result)

def imageCreation(input):

    # input contents array population
    inputContentsArrPush(input.replace(",", " ,"))
    inputContentsArrCurrentIndex = 0
    moveArrCurrentIndex = 0

    # canvas preparation
    canvasWidth, canvasHeight = 400, 37
    canvasSize = (canvasWidth, canvasHeight)
    canvas = Image.new('RGBA', canvasSize)
    # for putting text on the image ("+", etc.)
    draw = ImageDraw.Draw(canvas)

    # these values are adjusted to determine where to put the next image or text used in the completed image
    nextWidth = nextHeight = 0

    # function for determining how many pixels away to place the next image element, depending on what the current and next ones are
    def incWidth(stateFrom, stateTo, dirOrMotionNum):
        addend = 0

        if (stateFrom == "direction" and stateTo == "plus"):
            if (dirOrMotionNum == "1" or dirOrMotionNum == "2" or dirOrMotionNum == "4" or dirOrMotionNum == "5" or dirOrMotionNum == "7" or dirOrMotionNum == "8"):
                addend = 36
            elif (dirOrMotionNum == "3" or dirOrMotionNum == "9"):
                addend = 37
            elif (dirOrMotionNum == "6"):
                addend = 41

            # print("before \"direction\" -> \"plus\": " + str(nextWidth))
            # print("after \"direction\" -> \"plus\": " + str(nextWidth+addend))
            # print("")
        elif (stateFrom == "motion" and stateTo == "plus"):
            if (dirOrMotionNum == "236"):
                addend = 41
            else:
                addend = 36

            # print("before \"motion\" -> \"plus\": " + str(nextWidth))
            # print("after \"motion\" -> \"plus\": " + str(nextWidth+addend))
            # print("")
        elif (stateFrom == "plus" and stateTo == "button"):
            addend = 18

            # print("before \"plus\" -> \"button\": " + str(nextWidth))
            # print("after \"plus\" -> \"button\": " + str(nextWidth+addend))
            # print("")
        elif (stateFrom == "button" and stateTo == ">"):
            addend = 32

            # print("before \"button\" -> \">\": " + str(nextWidth))
            # print("after \"button\" -> \">\": " + str(nextWidth+addend))
            # print("")
        elif (stateFrom == ">" and stateTo == "button"):
            addend = 12

            # print("before \">\" -> \"button\": " + str(nextWidth))
            # print("after \">\" -> \"button\": " + str(nextWidth+addend))
            # print("")
        elif (stateFrom == ">" and stateTo == "motion"):
            if (dirOrMotionNum == "236"):
                addend = 12
            elif (dirOrMotionNum == "214"):
                addend = 17
            else:
                addend = 120

            # print("before \">\" -> \"motion\": " + str(nextWidth))
            # print("after \">\" -> \"motion\": " + str(nextWidth+addend))
            # print("")

        return(addend)

    def drawPlus(w,h):
        draw.text((w,h), "+", font=ImageFont.truetype("FreeSans.ttf", 24), fill=(255,255,255,255), stroke_width=2, stroke_fill=(0,0,0,255))

    def drawComma(w,h):
        draw.text((w,h), ",", font=ImageFont.truetype("FreeSans.ttf", 18), fill=(255,255,255,255), stroke_width=2, stroke_fill=(0,0,0,255))

    def drawArrow(w,h):
        draw.text((w,h), ">", font=ImageFont.truetype("FreeSans.ttf", 18), fill=(255,255,255,255), stroke_width=2, stroke_fill=(0,0,0,255))

    def drawxx(w,h):
        draw.text((w,h), "xx", font=ImageFont.truetype("FreeSans.ttf", 18), fill=(255,255,255,255), stroke_width=2, stroke_fill=(0,0,0,255))

    # automated image assembly using other functions for info
    for move in input.split(" "):
        print("\"" + move + "\"")
        print("return data: " + str(moveTranslation(move)))
        print("move is: " + str(parseMoveType(move)))
        print(" ")

        nextMove = getNextMove()
        nextMoveType = parseMoveType(nextMove)

        if (parseMoveType(move) == None):
            pass
        elif (parseMoveType(move) == "button"):
            # if neutral...no direction?
            # different width spacing depending on direction before text...arrow can get in way
            dirNum = moveTranslation(move)[0].lower()
            btn = moveTranslation(move)[1].lower()
            numOfHits = moveTranslation(move)[2]

            dirAbv = notation["directions"][dir]["abbreviation"]
            dirImg = Image.open(f"./images/directions/{dirAbv}.png")
            btnImg = Image.open(f"./images/buttons/{btn}.png")

            canvas.paste(dirImg, (nextWidth, nextHeight))
            nextWidth += incWidth("direction", "plus", dirNum)
            drawPlus(nextWidth, 5)
            nextWidth += incWidth("plus", "button", 0)
            canvas.paste(btnImg, (nextWidth, 7))

            nextWidth += incWidth("button", nextMoveType, 0)
            inputContentsArrCurrentIndex += 1
            moveArrCurrentIndex += 1
        elif (parseMoveType(move) == "motion"):
            motionNum = moveTranslation(move)[0].lower()
            btn = moveTranslation(move)[1].lower()

            motionAbv = notation["motions"][motionNum]["abbreviation"]
            motionImg = Image.open(f"./images/motions/{motionAbv}.png")
            btnImg = Image.open(f"./images/buttons/{btn}.png")

            canvas.paste(motionImg, (nextWidth, nextHeight))
            nextWidth += incWidth("motion", "plus", motionNum)
            drawPlus(nextWidth, 5)
            nextWidth += incWidth("plus", "button", 0)
            canvas.paste(btnImg, (nextWidth, 7))

            nextWidth += incWidth("button", nextMoveType, 0)
            inputContentsArrCurrentIndex += 1
            moveArrCurrentIndex += 1
        elif (parseMoveType(move) == "charge"):
            pass
        elif (parseMoveType(move) == ">"):
            drawArrow(nextWidth,7)
            # print(f"before \">\" -> \"{nextMoveType}\": " + str(nextWidth))

            if (nextMoveType == "motion"):
                motionNum = moveTranslation(nextMove)[0].lower()
                nextWidth += incWidth(">", nextMoveType, str(motionNum))
                pass
            else:
                nextWidth += incWidth(">", nextMoveType, 0)
                pass

            # print(f"after \">\" -> \"{nextMoveType}\": " + str(nextWidth))
            # print("")
            inputContentsArrCurrentIndex += 1
            moveArrCurrentIndex += 1

        elif (parseMoveType(move) == ","):
            pass
        elif (parseMoveType(move) == "xx"):
            pass

        canvas.save("./move.png", "PNG")

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

def parseMoveType(move):
    if (move == None):
        return
    # print(f"(parseMoveType) Checking syntax of move '{move}'")
    syntaxChecking(move)
    if (move == ">"):
        return(">")
    elif (move == "xx"):
        return("xx")
    elif (move == ","):
        return(",")
    # elif (move == ","):
        # return(",")
    # if the first character in this move is a bracket, this is a charge move
    if (("[" in move or "]" in move)):
        return("charge")
    # else, if it's a number (we assume for now)...
    else:
        # if the second character of this move is also a number,
        # it's an abbreviation for an attack strength level (l for light, h for heavy, etc)...
        try:
            if ((move[1]).isdigit()):
                return("motion")
        except:
            pass
        # else, it's number notation for a direction + a button
        else:
            return("button")

customTranslations = {"236*K": "Lightning Legs", "[1/2/3]7/8/9*K" : "Spinning Bird Kick"};

def customTranslationParsing():
    # custom translation handling
    for input in customTranslations.keys():
        print("Key (input): " + input)
        print("Value (name): " + customTranslations[input])
        kp = input.partition("*")
        print("input.partition(\"*\"): " + str(kp) + "\n")


def moveTranslation(move):
    # print(f"(moveTranslation) Checking syntax of move '{move}'")
    syntaxChecking(move)

    if (parseMoveType(move) == None):
        pass
    elif (parseMoveType(move) == "charge"):
        lbi = move.index("[")+1
        rbi = move.index("]")

        hold = move[lbi:rbi]
        release = move[rbi+1:rbi+2]
        btn = move[4] + move[5]

        return({"hold": hold, "release": release, "btn": btn})
    elif (parseMoveType(move) == "motion"):
        if (len(move) != 3 and int(move[0:2]) > 9):
            attackStrengths = ["L", "M", "H"]
            for element in attackStrengths:
                if (move.partition(element)[2] != ""):
                    motionNum = move.partition(element.upper())[0]
                    btn =  move.partition(element.upper())[1] + move.partition(element.upper())[2]

                    return({"motionNum": motionNum, "btn": btn})
    elif (parseMoveType(move) == "button"):
        direction = move[0]
        btn = move[1]+move[2]
        if (("(" in move or ")" in move)):
            numOfHits = move[4]
        else:
            numOfHits = 0

        return({"direction": direction, "btn": btn, "numOfHits": numOfHits})
    elif (parseMoveType(move) == "xx"):
        return("xx")
    elif (parseMoveType(move) == ">"):
        return(">")
    elif (parseMoveType(move) == ","):
        return(",")

def inputContentsArrPush(input):
    print("Input: " + str(input))
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

    # print(moveArr)
    # print(inputContentsArr)
    # print("----\n")

# customTranslationParsing()
toTranslate = "2HP(1) > 236LK, 2LP > [2]8LK"
# imageCreation(toTranslate)
wikiMarkdownCreation(toTranslate)
# wikiMarkdownCreation("2LP > 5MP > 2MK > [2]8LK")
