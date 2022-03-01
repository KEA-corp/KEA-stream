def remove_strvide(liste):
    while "" in liste:
        liste.remove("")
    return liste


def get_type(elmt: str):
    if elmt.isdigit():
        return "int", elmt
    elif elmt[0] == elmt[-1] and elmt[0] in ["'", '"']:
        return "str", elmt[1:-1]
    elif elmt[0] == "$":
        return "var", elmt[1:]
    elif elmt in ["LOOP", "IF", "END", "BREAK"]:
        return "mc", elmt
    elif elmt in ["+", "-", "*", "/", "%", "^", "**"]:
        return "op", elmt
    elif elmt in ["==", "!=", "=", "=+", "=-", "==+", "==-"]:
        return "cpr", elmt
    else:
        return "func", elmt


def parse(e, i, length, ACTIVE_MCN): # sourcery no-metrics
    """
    e =>        [nb in args, nb out args, [code]]
    i =>        index de la partie a analyser
    length =>   longeur de la liste de code deja analyser
    """

    charge = 0
    Vstream = f"stream{i}"
    sortie = []

    for c in str(e[2][i]).split(" "):

        etype, econt = get_type(c)

        if charge:
            if etype in ["int", "str"]:
                sortie.append(["V", "temp", econt])
                temp = "temp"  

            elif etype == "var":
                temp = econt

            else:
                raise Exception(f"{etype} ne peut pas etre utilise apres un operateur")

            if get_type(charge)[0] == "op":
                sortie.append(["C", Vstream, Vstream, charge, temp])

            elif get_type(charge)[0] == "cpr":
                sortie.append(["B", Vstream, Vstream, charge, temp])
            
            charge = 0

        elif etype in ["int", "str"]:
            sortie.append(["V", Vstream, econt])

        elif etype == "var":
            if e[0] > 1:
                raise Exception("une variable ne peut pas prendre plusieurs entrées")
            # soit [VAR > STREAM] (length == 0) soit [STREAM > VAR]
            sortie.append(["H", Vstream, econt] if length == 0 else ["H", econt, Vstream])

        elif etype == "mc":
            if econt == "LOOP":
                sortie.append(["L", f"loop{ACTIVE_MCN[1]}", Vstream])
                ACTIVE_MCN[0].append(f"loop{ACTIVE_MCN[1]}")
                ACTIVE_MCN[1] += 1

            elif econt == "IF":
                sortie.append(["X", f"if{ACTIVE_MCN[1]}", Vstream])
                ACTIVE_MCN[0].append(f"if{ACTIVE_MCN[1]}")
                ACTIVE_MCN[1] += 1

            elif econt == "END":
                sortie.append(["E", ACTIVE_MCN[0][-1]])
                ACTIVE_MCN[0].pop()

            elif econt == "BREAK":
                sortie.append(["Z", Vstream])

        elif etype in ["op", "cpr"]:
            charge = econt

        else:
            temp = ["T", c ,"&".join([f"stream{j+i}" for j in range(e[0] // (e[1] if e[1] != 0 else 1))])]
            # si la fonction retourne une valeur
            if e[1] > 0:
                temp.append(Vstream)
            sortie.append(remove_strvide(temp))

    return sortie, ACTIVE_MCN