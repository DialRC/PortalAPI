import sys
f1 = open("corpus.ner.feature.test")
f2 = open("output.txt")

golden = f1.readlines()
test = f2.readlines()

O = 0
X = 0
for x, y in zip(golden, test):
    #print x
    #print y
    if x.strip() == "":
        continue
    x = x.split(" ")[0]
    y = y.split(" ")[0]
    #print y

    #sys.stdin.readline()
    if x == y:
        O+=1
    else:
        X+=1

print float(O)/(X+ O)

