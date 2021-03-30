# packages/dependancies
from PIL import Image, ImageFont, ImageDraw
import sys

# fighting game terminologies...maybe make a dict later?
attackStrengthAbbreviations = ("l", "m", "h", "ex")
attackStrengthWords = ("Light", "Medium", "Heavy", "EX.")

attackTypeAbbreviations = ("p", "k")
attackTypeWords = ("Punch", "Kick")

attackShortforms = {"LP":"Jab", "MP":"Short", "HP":"Fierce", "LK":"Short", "MK":"Forward", "HK":"Roundhouse"}

directionNumbers = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
directionAbbreviations = ("d/b", "d", "d/f", "b", "n", "f", "u/b", "u", "u/f")
directionWords = ("down-back", "down", "down-forward", "back", "neutral", "forward", "up-back", "up", "up-forward")
directionStates = ("Crouching", "Crouching", "Crouching", "Back", "Standing", "Towards", "Jumping", "Neutral Jumping", "Jumping")
directionStatesAbbreviations = ("cr.", "cr.", "cr.", "b.", "s.", "f.", "j.", "nj.", "j.")

motionNumbers = ("236", "214", "41236", "63214", "623", "421", "6321478", "2369", "412", "632")
motionAbbreviations = ("qcf", "qcb", "hcf", "hcb", "dp", "rdp", "360", "tk", "bdbd", "fdfd")
motionWords = ("Quarter-Circle Forward", "Quarter-Circle Back", "Half-Circle Forward", "Half-Circle Back", "Dragon Punch", "Reverse Dragon Punch", "360", "Tiger Knee", "Back, Down-Back, Down", "Forward, Down-Forward, Down")

moveArr = []
inputContentsArr = []

def wikiMarkdownCreation(input):
    # todo
    print("wiki markdown creation function")
    print(input)

def imageCreation(input):
    def getNextMove():
        try:
            # print("    Current move: " + moveArr[moveArrCurrentIndex])
            # print("    Next move: " + moveArr[moveArrCurrentIndex+1])
            return(moveArr[moveArrCurrentIndex+1])
        except:
            return(None)

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
        # print("\"" + move + "\"")
        # print("return data: " + str(moveTranslation(move)))
        # print("move is: " + str(parseMoveType(move)))
        # print(" ")

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

            dirAbv = directionAbbreviations[directionNumbers.index(dirNum)].replace("/", "")
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

            motionAbv = motionAbbreviations[motionNumbers.index(motionNum)]
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
    syntaxChecking(move)
    if (move == ">"):
        return(">")
    elif (move == "xx"):
        return("xx")
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

def parseDirection(dirNum):

    dirAbbreviation = directionAbbreviations[directionNumbers.index(dirNum)]
    dirWord = directionWords[directionNumbers.index(dirNum)]
    dirState = directionStates[directionNumbers.index(dirNum)]
    dirStateAbbreviation = directionStatesAbbreviations[directionNumbers.index(dirNum)]

    # print("Direction number: " + dirNum)
    # print("Direction abbreviation: " + dirAbbreviation)
    # print("Direction word: " + dirWord)
    # print("Direction state: " + dirState)
    # print("Direction state abbreviation: " + dirStateAbbreviation)
    # print(" ")

    return(dirNum)

def parseAttack(move):
    attStrAbv = move[1]
    attTypeAbv = move[2]

    # if string contains an attack that requires a specific amount of hits (use of parentheses () )
    if (("(" in move or ")" in move)):
        numOfHits = move[4]
    else:
        numOfHits = 0

    attStrWord = attackStrengthWords[attackStrengthAbbreviations.index(attStrAbv.lower())]
    attTypeWord = attackTypeWords[attackTypeAbbreviations.index(attTypeAbv.lower())]

    attMoveWord = attStrWord + " " + attTypeWord
    attMoveAbv = attStrWord[0] + attTypeWord[0]

    # print("Attack strength abbreviation: " + attStrWord[0])
    # print("Attack strength word: " + attStrWord)
    # print("Attack type abbreviation: " + attTypeWord[0])
    # print("Attack type word: " + attTypeWord)
    # print("Attack move abbreviation: " + attMoveAbv)
    # print("Attack move word: " + attMoveWord)
    # print("Attack move shortform: " + attackShortforms[attMoveAbv])

    # if (("(" in move or ")" in move)):
        # print("Number of hits: " + numOfHits)

    return(attMoveAbv, str(numOfHits))

def buttonParsing(move):
    # parseDirection(move[0])
    # parseAttack(move)

    return(str(parseDirection(move[0])), str(parseAttack(move)[0]), str(parseAttack(move)[1]),)

def chargeParsing(move):
    lbi = move.index("[")+1
    rbi = move.index("]")

    chargeHoldDirection = move[lbi:rbi]
    chargeHoldDirectionAbbreviation = directionAbbreviations[directionNumbers.index(chargeHoldDirection)]
    chargeHoldDirectionWord = directionWords[directionNumbers.index(chargeHoldDirection)]
    chargeHoldDirectionState = directionStates[directionNumbers.index(chargeHoldDirection)]
    chargeHoldDirectionStateAbbreviation = directionStatesAbbreviations[directionNumbers.index(chargeHoldDirection)]

    # print("Charge hold direction number: " + chargeHoldDirection)
    # print("Charge hold direction abbreviation: " + chargeHoldDirectionAbbreviation)
    # print("Charge hold direction word: " + chargeHoldDirectionWord)
    # print("Charge hold direction state: " + chargeHoldDirectionState)
    # print("Charge hold direction state abbreviation: " + chargeHoldDirectionStateAbbreviation)
    # print(" ")

    chargeReleaseDirection = move[rbi+1:rbi+2]
    chargeReleaseDirectionAbbreviation = directionAbbreviations[directionNumbers.index(chargeReleaseDirection)]
    chargeReleaseDirectionWord = directionWords[directionNumbers.index(chargeReleaseDirection)]
    chargeReleaseDirectionState = directionStates[directionNumbers.index(chargeReleaseDirection)]
    chargeReleaseDirectionStateAbbreviation = directionStatesAbbreviations[directionNumbers.index(chargeReleaseDirection)]

    # print("Charge release direction number: " + chargeReleaseDirection)
    # print("Charge release direction abbreviation: " + chargeReleaseDirectionAbbreviation)
    # print("Charge release direction word: " + chargeReleaseDirectionWord)
    # print("Charge release direction state: " + chargeReleaseDirectionState)
    # print("Charge release direction state abbreviation: " + chargeReleaseDirectionStateAbbreviation)
    # print(" ")

    attackStrengthWord = attackStrengthWords[attackStrengthAbbreviations.index(move[4].lower())]
    attackTypeWord = attackTypeWords[attackTypeAbbreviations.index(move[5].lower())]
    attackMoveWord = attackStrengthWord + " " + attackTypeWord
    attackMoveAbbreviation = move[4] + move[5]

    # print("Attack strength abbreviation: " + attackStrengthWord[0])
    # print("Attack strength word: " + attackStrengthWord)
    # print("Attack type abbreviation: " + attackTypeWord[0])
    # print("Attack type word: " + attackTypeWord)
    # print("Attack move abbreviation: " + attackMoveAbbreviation)
    # print("Attack move word: " + attackMoveWord)
    # print("Attack move shortform: " + attackShortforms[attackMoveAbbreviation])
    # print(" ")

    return(chargeHoldDirection, chargeReleaseDirection, attackMoveAbbreviation)

def motionParsing(move):
    try:
        if (len(move) != 3 and int(move[0:2]) > 9):
            for element in attackStrengthAbbreviations:
                if (move.partition(element.upper())[2] != ""):
                    motionInputNumber = move.partition(element.upper())[0]            # (236)LK,
                    motionInputAttackStrengthAbbreviation = move.partition(element.upper())[1]    # 236(L)K,
                    motionInputAttackStrengthWord = attackStrengthWords[attackStrengthAbbreviations.index(motionInputAttackStrengthAbbreviation.lower())]
                    motionInputAttackTypeAbbreviation = (move.partition(element.upper())[2])[0]       # 236L(K),
                    motionInputAttackTypeWord = attackTypeWords[attackTypeAbbreviations.index(motionInputAttackTypeAbbreviation.lower())]
                    attackMoveAbbreviation = motionInputAttackStrengthAbbreviation + motionInputAttackTypeAbbreviation

                    motionInputAbbreviation = motionAbbreviations[(motionNumbers.index(motionInputNumber))]
                    motionInputWord = motionWords[(motionNumbers.index(motionInputNumber))]

                    # print("Motion input in number notation: " + motionInputNumber)
                    # print("Motion input in abbreviated notation: " + motionInputAbbreviation)
                    # print("Motion input in word notation: " + motionInputWord)
                    # print("")

                    # print("Attack strength abbreviation: " + motionInputAttackStrengthAbbreviation)
                    # print("Attack strength word: " + motionInputAttackStrengthWord)
                    # print("Attack type abbreviation: " + motionInputAttackTypeAbbreviation)
                    # print("Attack type word: " + motionInputAttackTypeWord)
                    # print("Attack move abbreviation: " + motionInputAttackStrengthAbbreviation + motionInputAttackTypeAbbreviation)
                    # print("Attack move word: " + motionInputAttackStrengthWord + " " + motionInputAttackTypeWord)
                    # print("Attack move shortform: " + attackShortforms[attackMoveAbbreviation])

                    return(motionInputNumber, attackMoveAbbreviation)

    except Exception:
        pass
    # .. not a motion

# will be defined by user; example values
customTranslations = {"236*K": "Lightning Legs", "[1/2/3]7/8/9*K" : "Spinning Bird Kick"};

def customTranslationParsing():
    # custom translation handling
    for input in customTranslations.keys():
        print("Key (input): " + input)
        print("Value (name): " + customTranslations[input])
        kp = input.partition("*")
        print("input.partition(\"*\"): " + str(kp) + "\n")

        # if the partition successfully split the string...
        if (kp[2] != ""):
            # charge move handling
            if ("[" in kp[0] or "]" in kp[0]):
                lbi = input.index("[")
                rbi = input.index("]")
                chargeHoldDirections = (input[lbi+1:rbi]).split("/")
                chargeReleaseDirections = (input[rbi+1:].partition("*")[0]).split("/")

                chargeAttackStrength = (input[rbi+1:].partition("*")[1])
                if (chargeAttackStrength == "*"):
                    chargeAttackStrength = "Any"
                chargeAttackType = (input[rbi+1:].partition("*")[2])

                # print("Valid charge hold directions: ")
                # for validChargeHoldDirection in chargeHoldDirections:
                    # print(validChargeHoldDirection)

                # print("Valid charge release directions:")
                # for validChargeReleaseDirection in chargeReleaseDirections:
                    # print(validChargeReleaseDirection)

                # print("Charge attack strength: " + chargeAttackStrength)
                # print("Charge attack type: " + chargeAttackType)

            # motion input move handling
            elif (kp[0] in motionNumbers):
                customMotionInputNumber = kp[0]
                customMotionInputAttackStrength = kp[1]
                customMotionInputAttackTypeAbbreviation = (kp[2])[0]
                customMotionInputAttackTypeWord = attackTypeWords[attackTypeAbbreviations.index(customMotionInputAttackTypeAbbreviation.lower())]

                # print("Custom motion input number: " + customMotionInputNumber)
                # if ("*" in kp[1]):
                    # print("Custom motion input attack strength: " + "Any")
                # else:
                    # print("Custom motion input attack strength: " + customMotionInputAttackStrength)
                # print("Custom motion input attack type abbreviation: " + customMotionInputAttackTypeAbbreviation)
                # print("Custom motion input attack type word: " + customMotionInputAttackTypeWord)
                # print("\n----")
            # elif ("(" in toTranslate or ")" in toTranslate):


def moveTranslation(move):
    syntaxChecking(move)
    # print(move)

    if (parseMoveType(move) == None):
        pass
    elif (parseMoveType(move) == "charge"):
        # print("syntax: hold, release, button")
        return(chargeParsing(move))
    elif (parseMoveType(move) == "motion"):
        # print("syntax: motion, button")
        return(motionParsing(move))
    elif (parseMoveType(move) == "button"):
        # print("syntax: direction, button, numofhits")
        return(buttonParsing(move))
    elif (parseMoveType(move) == "xx"):
        return("xx")
    elif (parseMoveType(move) == ">"):
        return(">")
    elif (parseMoveType(move) == ","):
        return(",")
    else:
        pass

def inputContentsArrPush(input):
    split = input.split(" ")
    # print("String: " + str(input) + "\n----")
    for move in split:
        # print(move)
        moveArr.append(move)
        inputContentsArr.append(parseMoveType(move))
    # print("----\n")

    # print(moveArr)
    # print(inputContentsArr)
    # print("----\n")

# customTranslationParsing()
# toTranslate = "2HP(1) > 236LK, 2LP > [2]8LK"
# imageCreation(toTranslate)
# imageCreation("41236HP")
wikiMarkdownCreation("41236HP")
