from mod.decoupeur import Decoupeur
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true", help="Debug mode")
parser.add_option("-f", "--file", dest="file", default="main.ks", help="File to parse")
parser.add_option("-o", "--output", dest="output", default="output.kea", help="Output file")
options = parser.parse_args()[0]

code = open(options.file, "r").read()

kea = Decoupeur(code, options.debug)

def printe(p,k):
    print(f"{p} : {k}")

parsed = "\n".join([" ".join(k) for k in kea.start()])

with open(options.output, "w") as f:
    f.write(parsed)