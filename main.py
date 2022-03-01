DEBUG_PRINT = True

class Decoupeur:
    def __init__(self, code: str):
        self.brut = self.polissage(code)
        self.decouped = self.decoupe()
        self.analysed = self.analyse()
        self.generer()

    def polissage(self, code) -> str:
        code = code.replace("\n", " ").replace("\t", " ").strip()
        while "  " in code:
            code = code.replace("  ", " ")
        if DEBUG_PRINT:
            print(f"Polissage :\n| {code}")
        return code

    def decoupe(self) -> list:
        analiser_codetemp = lambda code: [c.strip() for c in code.split(",")]
        code = self.brut
        exit_list = []
        in_str = False
        codetemp = ""
        push = 0
        oldpush = 0
        for l in code:
            if l != ">" or in_str:
                codetemp += l

            if l in ["\"", "'"]:
                in_str = not in_str

            elif not in_str:
                if l == ">":
                    push += 1

                elif push > 0:
                    exit_list.append([oldpush ,push, analiser_codetemp(codetemp)])
                    oldpush, push = push, 0
                    codetemp = ""

        exit_list.append([oldpush, push, analiser_codetemp(codetemp)])
        if DEBUG_PRINT:
            print("\nDecoupe - [in args, out args, [code]] :")
            for e in exit_list:
                print(f"| {e}")
        return exit_list

    def analyse(self) -> list:
        analysed = []
        for e in self.decouped:
            if len(e[2]) != e[1] and self.decouped.index(e) != len(self.decouped) - 1:
                raise Exception("le nombre de chevron ne correspond pas au nombre de parametres")
            for i in range(len(e[2])):
                analysed.append(self.parse(e, i, len(analysed)))
                
        if DEBUG_PRINT:
            print("\nAnalyse :")
            for a in analysed:
                print(f"| {a}")
        return analysed

    def generer(self) -> str:
        print("\nGeneration :")
        for e in self.analysed:
            print("| " + " ".join(e))


    def parse(self, e, i, length):
        """
        e =>        [nb in args, nb out args, [code]]
        i =>        index de la partie a analyser
        length =>   longeur de la liste de code deja analyser
        """

        c = str(e[2][i])
        Vstream = f"stream{i}"
        
        # si c'est un nombre
        if c.isdigit():
            return ["V", Vstream, c.strip()]
        
        # si c'est une chaine
        elif c[0] == c[-1] and c[0] in ["'", '"']:
            return ["V", Vstream, c[1:-1]]
        
        # si c'est une variable
        elif c[0] == "$":
            if e[0] > 1:
                raise Exception("une variable ne peut pas prendre plusieurs entrées")
            if length == 0:
                return ["H", Vstream, c[1:]]
            else:
                return ["H", c[1:], Vstream]
        
        # si c'est une fonction
        else:
            sortie = ["T", c ,"&".join([f"stream{j+i}" for j in range(e[0] // (e[1] if e[1] != 0 else 1))])]
            if e[1] > 0:
                sortie.append(Vstream)
            while "" in sortie:
                sortie.remove("")
            return sortie





Decoupeur("""
1 + 6 > print
""")