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

'''
by dustloop rules,
>   is a catch-all; usually for cancels, i guess
,   denotes a link
'''

def canvasCreation():
    # canvas preparation
    canvasWidth, canvasHeight = 400, 37
    canvasSize = (canvasWidth, canvasHeight)
    newImage = Image.new('RGBA', canvasSize)

    # for putting text on the image ("+", etc.)
    draw = ImageDraw.Draw(newImage)

    # image assembly
    # newImage.paste(Image.open("./images/buttons/lp.png"), (0,6))
    # draw.text((38, 4), ",", font=ImageFont.truetype("FreeSans.ttf", 24), fill=(255,255,255,255), stroke_width=2, stroke_fill=(0,0,0,255))
    # newImage.paste(Image.open("./images/buttons/hp.png"), (57,6))

    # saving the image
    # newImage.save("./complete.png", "PNG")

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
    syntaxChecking(move)
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

def buttonParsing(move):
    attackDirection = move[0]    #(5)HP
    attackStrength = move[1]     #5(H)P
    attackType = move[2]         #5H(P)
    # if string contains an attack that requires a specific amount of hits (use of parentheses () )

    if (("(" in move or ")" in move)):
        numOfHits = move[4]

    attackDirectionAbbreviation = directionAbbreviations[directionNumbers.index(attackDirection)]
    attackDirectionWord = directionWords[directionNumbers.index(attackDirection)]
    attackDirectionState = directionStates[directionNumbers.index(attackDirection)]
    attackDirectionStateAbbreviation = directionStatesAbbreviations[directionNumbers.index(attackDirection)]

    attackStrengthWord = attackStrengthWords[attackStrengthAbbreviations.index(attackStrength.lower())]
    attackTypeWord = attackTypeWords[attackTypeAbbreviations.index(attackType.lower())]

    attackMoveWord = attackStrengthWord + " " + attackTypeWord
    attackMoveAbbreviation = attackStrengthWord[0] + attackTypeWord[0]

    print("Direction number: " + attackDirection)
    print("Direction abbreviation: " + attackDirectionAbbreviation)
    print("Direction word: " + attackDirectionWord)
    print("Direction state: " + attackDirectionState)
    print("Direction state abbreviation: " + attackDirectionStateAbbreviation)
    print(" ")

    print("Attack strength abbreviation: " + attackStrengthWord[0])
    print("Attack strength word: " + attackStrengthWord)
    print("Attack type abbreviation: " + attackTypeWord[0])
    print("Attack type word: " + attackTypeWord)
    print("Attack move abbreviation: " + attackMoveAbbreviation)
    print("Attack move word: " + attackMoveWord)
    print("Attack move shortform: " + attackShortforms[attackMoveAbbreviation])

    if (("(" in move or ")" in move)):
        print("Number of hits: " + numOfHits)
    print("----")
    print(" ")

def chargeParsing(move):
    lbi = move.index("[")+1
    rbi = move.index("]")

    chargeHoldDirection = move[lbi:rbi]
    chargeHoldDirectionAbbreviation = directionAbbreviations[directionNumbers.index(chargeHoldDirection)]
    chargeHoldDirectionWord = directionWords[directionNumbers.index(chargeHoldDirection)]
    chargeHoldDirectionState = directionStates[directionNumbers.index(chargeHoldDirection)]
    chargeHoldDirectionStateAbbreviation = directionStatesAbbreviations[directionNumbers.index(chargeHoldDirection)]

    print("Charge hold direction number: " + chargeHoldDirection)
    print("Charge hold direction abbreviation: " + chargeHoldDirectionAbbreviation)
    print("Charge hold direction word: " + chargeHoldDirectionWord)
    print("Charge hold direction state: " + chargeHoldDirectionState)
    print("Charge hold direction state abbreviation: " + chargeHoldDirectionStateAbbreviation)
    print(" ")

    chargeReleaseDirection = move[rbi+1:rbi+2]
    chargeReleaseDirectionAbbreviation = directionAbbreviations[directionNumbers.index(chargeReleaseDirection)]
    chargeReleaseDirectionWord = directionWords[directionNumbers.index(chargeReleaseDirection)]
    chargeReleaseDirectionState = directionStates[directionNumbers.index(chargeReleaseDirection)]
    chargeReleaseDirectionStateAbbreviation = directionStatesAbbreviations[directionNumbers.index(chargeReleaseDirection)]

    print("Charge release direction number: " + chargeReleaseDirection)
    print("Charge release direction abbreviation: " + chargeReleaseDirectionAbbreviation)
    print("Charge release direction word: " + chargeReleaseDirectionWord)
    print("Charge release direction state: " + chargeReleaseDirectionState)
    print("Charge release direction state abbreviation: " + chargeReleaseDirectionStateAbbreviation)
    print(" ")

    attackStrengthWord = attackStrengthWords[attackStrengthAbbreviations.index(move[4].lower())]
    attackTypeWord = attackTypeWords[attackTypeAbbreviations.index(move[5].lower())]
    attackMoveWord = attackStrengthWord + " " + attackTypeWord
    attackMoveAbbreviation = move[4] + move[5]

    print("Attack strength abbreviation: " + attackStrengthWord[0])
    print("Attack strength word: " + attackStrengthWord)
    print("Attack type abbreviation: " + attackTypeWord[0])
    print("Attack type word: " + attackTypeWord)
    print("Attack move abbreviation: " + attackMoveAbbreviation)
    print("Attack move word: " + attackMoveWord)
    print("Attack move shortform: " + attackShortforms[attackMoveAbbreviation])
    print(" ")

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

                    print("Motion input in number notation: " + motionInputNumber)
                    print("Motion input in abbreviated notation: " + motionInputAbbreviation)
                    print("Motion input in word notation: " + motionInputWord)
                    print("")

                    print("Attack strength abbreviation: " + motionInputAttackStrengthAbbreviation)
                    print("Attack strength word: " + motionInputAttackStrengthWord)
                    print("Attack type abbreviation: " + motionInputAttackTypeAbbreviation)
                    print("Attack type word: " + motionInputAttackTypeWord)
                    print("Attack move abbreviation: " + motionInputAttackStrengthAbbreviation + motionInputAttackTypeAbbreviation)
                    print("Attack move word: " + motionInputAttackStrengthWord + " " + motionInputAttackTypeWord)
                    print("Attack move shortform: " + attackShortforms[attackMoveAbbreviation])

    except Exception:
        pass
    # .. not a motion

# will be defined by user; example values
customTranslations = {"236*K": "Lightning Legs", "[1/2/3]7/8/9*K" : "Spinning Bird Kick"};

def moveTranslation(toTranslate):

    split = toTranslate.split(" ")
    print("String: " + str(toTranslate) + "\n----")
    for x in split:
        print(x)
    print("----\n")

    for move in split:
        syntaxChecking(move)

        if (parseMoveType(move) == None):
            print("Evaluating \"" + move + "\"...\n")
            pass
        elif (parseMoveType(move) == "charge"):
            print("Evaluating \"" + move + "\"... (charge)\n")
            chargeParsing(move)
        elif (parseMoveType(move) == "motion"):
            print("Evaluating \"" + move + "\"... (motion)\n")
            motionParsing(move)
        elif (parseMoveType(move) == "button"):
            print("Evaluating \"" + move + "\"... (button)\n")
            buttonParsing(move)

# customTranslationParsing()
toTranslate = "2HP(1) > 236LK, 2LP > [2]8LK"
moveTranslation(toTranslate)
