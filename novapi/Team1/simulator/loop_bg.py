pos = 0
def updateNumbers():
    global pos
    pos +=1



def run():
    global pos
    if pos != 10:
        while pos != 10:
            updateNumbers()
            print(pos)


run()
