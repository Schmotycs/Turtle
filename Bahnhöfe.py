def Bahnhofslänge(Bahnhof, Standard):
    laengen = {
        # FA Haltestellen
        "FA_Haltestelle_1": 341000, "FA_Stop_1": 341000,
        "FA_Haltestelle_2": 358000, "FA_Stop_2": 358000,
        "FA_Haltestelle_3": 280000, "FA_Stop_3": 280000,
        "FA_Haltestelle_4": 280000, "FA_Stop_4": 280000,
        "FA_Haltestelle_5": 376000, "FA_Stop_5": 376000,
        
        # AR Haltestellen
        "AR_Haltestelle_1": 291000, "AR_Stop_1": 291000,
        "AR_Haltestelle_2": 293000, "AR_Stop_2": 293000,
        "AR_Haltestelle_3": 329000, "AR_Stop_3": 329000,
        "AR_Haltestelle_4": 347000, "AR_Stop_4": 347000,
        "AR_Haltestelle_5": 360000, "AR_Stop_5": 360000,
        "AR_Haltestelle_6": 263000, "AR_Stop_6": 263000
    }
    return laengen.get(Bahnhof, Standard)