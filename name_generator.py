glas = ["a", "e", "i", "o", "u", "y"]
sogl = ["b", "c", "d", "f", "g", "h", "k", "l", "m", "n", "p", "r", "s", "t", "v", "w", "x", "z"]
l = glas + sogl
n = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
c = letters + numbers
# zones file https://data.iana.org/TLD/tlds-alpha-by-domain.txt
ZONE_FILE = "tlds-alpha-by-domain.txt"

with open(ZONE_FILE, 'r') as f:
    ZONE = [line.rstrip() for line in f]

def save2file(content, file="output.txt"):
    with open(file, 'a') as f:
        f.write(content + '\n')

def gsgsg():
    for a in glas:
        for b in sogl:
            for c in glas:
                for d in sogl:
                    for e in glas:
                        save2file(a+b+c+d+e, "gsgsg.txt")

def generate(pattern, zones = ZONE):
    #namez = ['t5', 'mytetzonnam']
    for a in n:
        for b in n:
            for zone in zones:
                save2file(a + "." + zone.lower(), pattern + ".txt")

generate("nn", ["pm"])