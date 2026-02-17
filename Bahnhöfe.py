def Bahnhofslänge(Bahnhof):
    if Bahnhof == "FA_Haltestelle_1":
        länge = 341
    if Bahnhof == "FA_Haltestelle_2":
        länge = 358
    if Bahnhof == "FA_Haltestelle_3":
        länge = 280
    if Bahnhof == "FA_Haltestelle_4":
        länge = 280
    if Bahnhof == "FA_Haltestelle_4":
        länge = 376

    if Bahnhof == "AR_Haltestelle_1":
        länge = 291
    if Bahnhof == "AR_Haltestelle_2":
        länge = 293
    if Bahnhof == "AR_Haltestelle_3":
        länge = 329
    if Bahnhof == "AR_Haltestelle_4":
        länge = 347
    if Bahnhof == "AR_Haltestelle_5":
        länge = 360
    if Bahnhof == "AR_Haltestelle_6":
        länge = 263
    else:
        länge = 180
    return länge*100

