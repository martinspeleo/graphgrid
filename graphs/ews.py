def calculateEWS(RR, SpO2, Temp, SBP, HR, ConciousLevel, SupO2):
    try:
        intRR = int(RR)
    except:
        intRR = 0
    try:
        intSpO2 = int(SpO2)
    except:
        intSpO2 = 0
    try:
        intTemp = int(Temp)
    except:
        intTemp = 0
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
    if (intSpO2 <=91):
        SpO2EWS = 3
    else:
        if (intSpO2 <=93):
            SpO2EWS = 2
        else:
            if (intSpO2 <=95):
                SpO2EWS = 1
            else:
                SpO2EWS = 0
    EWS = RREWS + SpO2EWS
    return EWS