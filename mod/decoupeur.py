'''
--|~|--|~|--|~|--|~|--|~|--|~|--

██  ████        ██████        ██
████    ██     ██           ████
██      ██   ████████     ██  ██
████████       ██       ██    ██
██             ██       █████████
██             ██             ██
██
 - codé en : UTF-8
 - langage : python 3
 - GitHub  : github.com/pf4-DEV
             github.com/KEA-corp
 - Licence : mit
--|~|--|~|--|~|--|~|--|~|--|~|--
'''

from mod.parse import parse


class Decoupeur:
    
    def __init__(self, code, debug=False):
        self.DEBUG_PRINT = bool(debug)
        self.active_mcn = [[],0] # nom des boucle / condition active
        self.brut = code
    
    def start(self):
        self.brut = self.polissage(self.brut)
        self.decouped = self.decoupe()
        self.analysed = self.analyse()
        return self.generer()

    def polissage(self, code) -> str:
        def replace_while(old, new, text):
            while old in text:
                text = text.replace(old, new)
            return text

        code = code.replace("\n", ";").replace("\t", " ").strip()
        code = replace_while("  ", " ", code)
        code = replace_while(";;", ";", code)

        if self.DEBUG_PRINT:
            print(f"Polissage :\n| {code}")
        return code

    def decoupe(self) -> list:
        decouped = []
        analiser_codetemp = lambda code: [c.strip() for c in code.split(",")]

        for code in self.brut.split(";"):

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
            decouped.append(exit_list)

        for d in decouped:
            for e in d:
                if len(e[2]) != e[1] and len(d) - 1 != d.index(e):
                    raise Exception("le nombre de chevron ne correspond pas au nombre de parametres")
                if e[2] == [""]:
                    decouped.remove(d)

        if self.DEBUG_PRINT:
            print("\nDecoupe - [in args, out args, [code]] :")
            for d in decouped:
                print(f"| ligne {decouped.index(d)}")
                for e in d:
                    print(f"| | {e}")

        return decouped

    def analyse(self) -> list:
        analysed = []
        for d in self.decouped:
            local_analyse = []

            if d[0][2][0].startswith("#") or d[0][2][0].startswith("//"):
                analysed.append([" =+ ".join([e[2][0] for e in d])])
                continue

            for e in d:
                for i in range(len(e[2])):
                    sortie, self.active_mcn = parse(e, i, len(local_analyse), self.active_mcn)
                    local_analyse.extend(iter(sortie))

            analysed.extend(local_analyse)

        if self.DEBUG_PRINT:
            print("\nAnalyse :")
            for a in analysed:
                print(f"| {a}")
        return analysed

    def generer(self) -> str:                
        return [[f.replace("=+", ">").replace("=-", "<") for f in e] for e in self.analysed]