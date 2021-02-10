def chargeParsing(move):
    chargeHoldDirection, chargeReleaseDirection = move[1], move[3]

    chargeHoldDirectionWord = directionWords[directionNumbers.index(chargeHoldDirection)]
    chargeHoldDirectionAbbreviation = directionAbbreviations[directionNumbers.index(chargeHoldDirection)]

    print("Charge hold direction number: " + chargeHoldDirection)
    print("Charge hold direction word: " + chargeHoldDirectionWord)
    print("Charge hold direction abbreviation: " + chargeHoldDirectionAbbreviation)
    print(" ")

    chargeReleaseDirectionWord = directionWords[directionNumbers.index(chargeReleaseDirection)]
    chargeReleaseDirectionAbbreviation = directionAbbreviations[directionNumbers.index(chargeReleaseDirection)]

    print("Charge release direction number: " + chargeReleaseDirection)
    print("Charge release direction word: " + chargeReleaseDirectionWord)
    print("Charge release direction abbreviation: " + chargeReleaseDirectionAbbreviation)
    print(" ")

    chargeAttackStrengthWord = attackStrengthWords[attackStrengthAbbreviations.index(move[4].lower())]
    chargeAttackTypeWord = attackTypeWords[attackTypeAbbreviations.index(move[5].lower())]
    chargeAttackMoveWord = chargeAttackStrengthWord + " " + chargeAttackTypeWord
    chargeAttackMoveAbbreviation = move[4] + move[5]

    print("Charge attack strength: " + chargeAttackStrengthWord)
    print("Charge attack type: " + chargeAttackTypeWord)
    print("Charge attack move word: " + chargeAttackMoveWord)
    print("Charge attack move abbreviation: " + chargeAttackMoveAbbreviation)
    print("Charge attack move shortform: " + attackShortforms[chargeAttackMoveAbbreviation])
    print("----")
    print(" ")

def motionParsing(move):
    # motion parsing
    try:
        if (len(move) != 3 and int(move[0:2]) > 9):
            for element in attackStrengthAbbreviations:
                if (move.partition(element.upper())[2] != ""):
                    motionInputNumber = move.partition(element.upper())[0]            # (236)LK,
                    motionInputAttackStrengthAbbreviation = move.partition(element.upper())[1]    # 236(L)K,
                    motionInputAttackStrengthWord = attackStrengthWords[attackStrengthAbbreviations.index(motionInputAttackStrengthAbbreviation.lower())]
                    motionInputAttackTypeAbbreviation = (move.partition(element.upper())[2])[0]       # 236L(K),
                    motionInputAttackTypeWord = attackTypeWords[attackTypeAbbreviations.index(motionInputAttackTypeAbbreviation.lower())]

                    motionInputAbbreviation = motionAbbreviations[(motionNumbers.index(motionInputNumber))]
                    motionInputWord = motionWords[(motionNumbers.index(motionInputNumber))]

                    print("Motion input in number notation: " + motionInputNumber)
                    print("Motion input in abbreviated notation: " + motionInputAbbreviation)
                    print("Motion input in word notation: " + motionInputWord)

                    print("Motion input attack strength abbreviation: " + motionInputAttackStrengthAbbreviation)
                    print("Motion input attack strength word: " + motionInputAttackStrengthWord)
                    print("Motion input attack type abbreviation: " + motionInputAttackTypeAbbreviation)
                    print("Motion input attack type word: " + motionInputAttackTypeWord)

    except Exception:
        pass
    # .. not a motion

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

        print("Attack strength: " + attackStrengthWord)
        print("Attack type: " + attackTypeWord)
        print("Attack move word: " + attackMoveWord)
        print("Attack move abbreviation: " + attackMoveAbbreviation)
        print("Attack move shortform: " + attackShortforms[attackMoveAbbreviation])

        if (("(" in move or ")" in move)):
            print("Number of hits: " + numOfHits)
        print("----")
        print(" ")

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
