from mod.parse import parse

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
                for elm in parse(e, i, len(analysed)):
                    analysed.append(elm)
                
        if DEBUG_PRINT:
            print("\nAnalyse :")
            for a in analysed:
                print(f"| {a}")
        return analysed

    def generer(self) -> str:
        print("\nGeneration :")
        for e in self.analysed:
            print("| " + " ".join(e))


Decoupeur("""
0, 1 >> or + 41 > print
""")