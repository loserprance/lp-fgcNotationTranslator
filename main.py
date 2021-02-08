# packages/dependancies
from PIL import Image, ImageFont, ImageDraw

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

def moveTranslation(toTranslate):
    '''
    fighting game notation can express the same move, special move, super, or combo the same way
    qcf, 236, d,df,f... crouching roundhouse, crouching heavy kick, cr.hk, sweep...

    what should be the options for how the end translation is formatted?

    by dustloop rules,
    >   is a catch-all; usually for cancels, i guess
    ,   denotes a link

    jab = lp
    strong = mp
    fierce = hp
    short = lk
    forward = mk
    roundhouse = hk
    '''

    strengthAbbreviations = ("l", "m", "h", "ex")
    strengthWords = ("Light", "Medium", "Heavy", "EX.")

    formOfAttackAbbreviations = ("p", "k")
    formOfAttackWords = ("Punch", "Kick")

    attackAbbreviations = ("LP", "MP", "HP", "LK", "MK", "HK")
    attackShortforms = ("Jab", "Short", "Fierce", "Short", "Forward", "Roundhouse")

    directionAbbreviations = ("d/b", "d", "d/f", "b", "n", "f", "u/b", "u", "u/f")
    directionWords = ("down-back", "down", "down-forward", "back", "neutral", "forward", "up-back", "up", "up-forward")
    directionStates = ("Crouching", "Crouching", "Crouching", "Back", "Standing", "Towards", "Jumping", "Neutral Jumping", "Jumping")
    directionStatesAbbreviations = ("cr.", "cr.", "cr.", "b.", "s.", "f.", "j.", "nj.", "j.")
    directionNumbers = ("1", "2", "3", "4", "5", "6", "7", "8", "9")

    motionAbbreviations = ("qcf", "qcb", "hcf", "hcb", "dp", "rdp", "360", "tk", "bdbd", "fdfd")
    motionNumbers = ("236", "214", "41236", "63214", "623", "421", "6321478", "2369", "412", "632")
    motionWords = ("Quarter-Circle Forward", "Quarter-Circle Back", "Half-Circle Forward", "Half-Circle Back", "Dragon Punch", "Reverse Dragon Punch", "360", "Tiger Knee", "Back, Down-Back, Down", "Forward, Down-Forward, Down")

    customTranslations = {"236*K": "Lightning Legs", "[1/2/3]7/8/9*K" : "Spinning Bird Kick"};

    print("String: " + str(toTranslate))
    print("----")
    split = toTranslate.split(" ")
    for x in split:
        print(x)
    print("----")

    # error checking
    if ("(" in toTranslate):
        # finding all occurences of a ( or ) in the string
        leftParenthesesIndexes = [i for i, c in enumerate(toTranslate) if c == "("]
        # print(f"Found character '(' at index(es): {leftParenthesesIndexes}")

        rightParenthesesIndexes = [i for i, c in enumerate(toTranslate) if c == ")"]
        # print(f"Found character ')' at index(es): {rightParenthesesIndexes}")

        if (len(leftParenthesesIndexes) != len(rightParenthesesIndexes)):
            print("Bad syntax; uneven amount of parentheses")
            return;

    if ("[" in toTranslate):
        # finding all occurences of a [ or ] in the string
        leftBracketsIndexes = [i for i, c in enumerate(toTranslate) if c == "["]
        # print(f"Found character '[' at index(es): {leftBracketsIndexes}")

        rightBracketsIndexes = [i for i, c in enumerate(toTranslate) if c == "]"]
        # print(f"Found character ']' at index(es): {rightBracketsIndexes}")

        if (len(leftBracketsIndexes) != len(rightBracketsIndexes)):
            print("Bad syntax; uneven amount of brackets")
            return;

    # for every possible button in this notation: LP, HK, etc...
    for button in attackAbbreviations:
        # check every individual move for the number notation for a direction + a button (ie. 2HK, 5MP)
        for move in split:
            if (button in move):
                if (("[" in move or "]" in move or "(" in move or ")" in move) and len(move) != 3):
                    return;
                else:
                    attackState = directionStates[directionNumbers.index(move[0])]
                    attackWord = strengthWords[strengthAbbreviations.index(move[1].lower())] + " " + formOfAttackWords[formOfAttackAbbreviations.index(move[2].lower())]
                    attackName = attackShortforms[attackAbbreviations.index(move[1:])]

                    print(attackState + " " + attackWord + " / " + attackState + " " + attackName)

    # if string contains an attack that requires a specific amount of hits (use of parentheses () )
    # if string contains a charge move of some kind (use of brackets [] )

# toTranslate = "2HP(1) > 236HK, 2LP > [2]8LK"
toTranslate = "5LP 8MP 2HP 7LK 4MK 6HK"
moveTranslation(toTranslate)
