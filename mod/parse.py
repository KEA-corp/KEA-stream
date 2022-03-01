def get_type(elmt: str):
    if elmt.isdigit():
        return "int", elmt
    elif elmt[0] == elmt[-1] and elmt[0] in ["'", '"']:
        return "str", elmt[1:-1]
    elif elmt[0] == "$":
        return "var", elmt[1:]
    elif elmt in ["+", "-", "*", "/", "=+", "=-", "=", "!"]:
        return "op", elmt
    else:
        return "func", elmt


def parse(e, i, length):
    """
    e =>        [nb in args, nb out args, [code]]
    i =>        index de la partie a analyser
    length =>   longeur de la liste de code deja analyser
    """


    c = str(e[2][i])
    Vstream = f"stream{i}"
    sortie = []

    etype, econt = get_type(c)

    if etype in ["int", "str"]:
        sortie.append(f"V {Vstream} {econt}")
    
    elif c[0] == "$":
        if e[0] > 1:
            raise Exception("une variable ne peut pas prendre plusieurs entrées")
        # soit [VAR > STREAM] (length == 0) soit [STREAM > VAR]
        return ["H", Vstream, c[1:]] if length == 0 else ["H", c[1:], Vstream]

    # si c'est une fonction
    else:
        sortie = ["T", c ,"&".join([f"stream{j+i}" for j in range(e[0] // (e[1] if e[1] != 0 else 1))])]
        if e[1] > 0:
            sortie.append(Vstream)
        while "" in sortie:
            sortie.remove("")
        return sortie
