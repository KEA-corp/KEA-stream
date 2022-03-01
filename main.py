DEBUG_PRINT = True

class Decoupeur:
    def __init__(self, code: str):
        self.brut = self.polissage(code)
        self.decouped = self.decoupe()
        self.analysed = self.analyse()
        self.generer()

    def polissage(self, code) -> str:
        code = code.replace("\n", " ")
        code = code.replace("\t", " ")
        if DEBUG_PRINT:
            print("Polissage :")
            print(code)      
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
            print("\nDecoupe :")
            for e in exit_list:
                print(e)
        return exit_list

    def analyse(self) -> list:
        analysed = []
        for e in self.decouped:
            if len(e[2]) != e[1] and self.decouped.index(e) != len(self.decouped) - 1:
                raise Exception("le nombre de chevron ne correspond pas au nombre de parametres")
            for i in range(len(e[2])):
                c = str(e[2][i])
                if c.isdigit():
                    # si c'est un nombre
                    analysed.append(["V", f"stream{i}" ,c.strip()])
                elif c[0] == c[-1] and c[0] in ["'", '"']:
                    # si c'est une chaine
                    analysed.append(["V", f"stream{i}" ,c[1:-1]])
                elif c[0] == "$":
                    # si c'est une variable
                    if e[0] > 1:
                        raise Exception("une variable ne peut pas prendre plusieurs entrées")
                    if len(analysed) == 0:
                        analysed.append(["H", f"stream{i}", c[1:]])
                    else:
                        analysed.append(["H", c[1:], f"stream{i}"])
                else:
                    # si c'est une fonction
                    analysed.append(["T", c ,"&".join([f"stream{j+i}" for j in range(e[0] // (e[1] if e[1] != 0 else 1))])])
                    if e[1] > 0:
                        analysed[-1].append(f"stream{i}")
        if DEBUG_PRINT:
            print("\nAnalyse :")
            for a in analysed:
                print(a)
        return analysed

    def generer(self) -> str:
        print("\nGeneration :")
        for e in self.analysed:
            print(" ".join(e))


Decoupeur("""
42 > $coucou
""")

print("\n--------------------\n")

Decoupeur("""
$coucou > print
""")