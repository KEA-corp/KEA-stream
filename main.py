from mod.decoupeur import Decoupeur

Decoupeur.DEBUG_PRINT = False

code = """
1 =+ 5 > print
"""

kea = Decoupeur(code, False)

print(kea.start())