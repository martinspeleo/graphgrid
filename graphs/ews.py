def calculateEWS(RR, SpO2, Temp, SBP, HR, ConciousLevel, SupO2):
#this function firstly makes sure the values are integers (or a float, in the case of Temperature, then, using the values from the 
#NEWS system - http://www.rcplondon.ac.uk/sites/default/files/documents/national-early-warning-score-standardising-assessment-acute-illness-severity-nhs.pdf 
#returns a NEWS score + whether it triggers the "RED score" (IE, individual parameter = 3)
    try:
        intRR = int(RR)
    except:
        intRR = 0
    try:
        intSpO2 = int(SpO2)
    except:
        intSpO2 = 0
    try:
        flTemp = float(Temp)
    except:
        flTemp = 0
    try:
        intSBP = int(SBP)
    except:
        intSBP = 0
    try:
        intHR = int(HR)
    except:
        intHR = 0
    try:
        intConciousLevel = int(ConciousLevel)
    except:
        intConciousLevel = 4
    try:
        intSupO2 = int(SupO2)
    except:
        intSupO2 = 1
    if (8 <= intRR >= 25):
         RREWS = 3
    else:
        if (intRR >= 21):
            RREWS = 2
        else:
            if (11 >= intRR):
                RREWS = 1
            else:
                RREWS = 0
    if (intSpO2 <= 91):
        SpO2EWS = 3
    else:
        if (intSpO2 <= 93):
            SpO2EWS = 2
        else:
            if (intSpO2 <= 95):
                SpO2EWS = 1
            else:
                SpO2EWS = 0
    if (35.0 >= flTemp):
        tempEWS = 3
    else:
        if (39.1 <= flTemp):
            tempEWS = 2
        else:
            if (36.0 >= flTemp >= 38.1):
                tempEWS = 1
            else:
                tempEWS = 0
    if (90 >= intSBP >= 220):
        SBPEWS = 3
    else:
        if (100 >= intSBP):
            SBPEWS = 2
        else:
            if (110 >= intSBP):
                SBPEWS = 1
            else:
                SBPEWS = 0
    if (40 >= intHR >=131):
        HREWS = 3
    else:
        if (intHR >=111):
            HREWS = 2
        else:
            if (50 >= intHR >= 91):
                HREWS = 1
            else:
                HREWS = 0
    if (intConciousLevel != 0):
        conciousLevelEWS = 3
    else:
        conciousLevelEWS = 0
    if (intSupO2 != 0):
        supO2EWS = 2
    else:
        supO2EWS = 0
    EWSObs = [RREWS, SpO2EWS, tempEWS, SBPEWS, HREWS, conciousLevelEWS, supO2EWS]
    for EWSRed in EWSObs:
        if (EWSRed == 3):
            EWSRedScore = 1
        else:
            EWSRedScore = 0
    EWS = RREWS + SpO2EWS + tempEWS + SBPEWS + HREWS + conciousLevelEWS + supO2EWS
    return {'EWS': EWS, 'EWSRedScore': EWSRedScore}