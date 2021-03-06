class Cells:
    
    cells = [[0 for x in range(255)] for x in range(255)]

    def __call__(self, x, y, v=None):
        if v:
            self.cells[x][y] = v
        return self.cells[x][y]

# not sure if this actually works lol
def Interpret(filePath, viewMemUtilization=False):
    data = open(filePath).read().splitlines()

    X = 0
    Y = 0

    cells = Cells()
    currentLine = 0
    variables = {}
    skippingLogic = False
    lineContent = ''
    try:
        ICount = 0
        while currentLine < len(data):
            line = data[currentLine].split("#")[0]

            valuesSet = -1
            currentCommand = None
            v0 = -1
            v1 = -1
            for char in line.split():

                if skippingLogic:
                    currentCommand = None
                    valuesSet = -1
                    if char == "I":
                        ICount += 1
                        continue

                    if char == "E":
                        if ICount == 0:
                            skippingLogic = False
                        else: 
                            ICount -= 1
                    continue
                if not currentCommand:
                    if char.startswith("+"):
                        cells(X, Y, cells(X, Y)+len([x for x in char if x == "+"]))
                        if cells(X, Y) == 256:
                            cells(X, Y, 0)
                        continue
                    if char.startswith("-"):
                        cells(X, Y, cells(X, Y)-len([x for x in char if x == "-"]))
                        if cells(X, Y) == -1:
                            cells(X, Y, 255)
                        continue
                
                if not currentCommand and char != "E":
                    valuesSet = 0
                    currentCommand = char
                    continue


                if currentCommand == "M":
                    if valuesSet == 0:
                        if char.startswith("+"):
                            X += len([x for x in char if x == "+"])
                        elif char.startswith("-"):
                            X -= len([x for x in char if x == "-"])
                        elif char == "/":
                            pass
                        else:
                            X = int(char)
                        valuesSet = 1
                    elif valuesSet == 1:
                        if char.startswith("+"):
                            Y += len([x for x in char if x == "+"])
                        elif char.startswith("-"):
                            Y -= len([x for x in char if x == "-"])
                        elif char == "/":
                            pass
                        else:
                            Y = int(char)

                        currentCommand = None
                        valuesSet = -1
                    continue

                if currentCommand == "S":
                    if char == "C":
                        cells(X, Y, cells(X, Y)) # why
                    elif char == "X":
                        cells(X, Y, X)
                    elif char == "Y":
                        cells(X, Y, Y)
                    else:
                        cells(X, Y, int(char))
                    currentCommand = None
                    valuesSet = -1
                    continue
                
                if currentCommand == "F":
                    currentLine = int(char)-2 # go one line early to keep processing said line and not one after it
                    currentCommand = None
                    valuesSet = -1
                    continue

                if currentCommand == "I":
                    if valuesSet == 0:
                        if char in variables.keys():
                            v0 = variables[char]
                        elif char == "C":
                            v0 = cells(X, Y)
                        else:
                            v0 = int(char)

                        valuesSet = 1
                    else:
                        valuesSet = -1
                        currentCommand = None

                        v2 = 0
                        if char in variables.keys():
                            v2 = variables[char]
                        elif char == "C":
                            v2 = cells(X, Y)
                        else:
                            v2 = int(char)
                        skippingLogic = not (v0 == v2)

                    continue
                
                if currentCommand == "V":
                    if valuesSet == 0:
                        v0 = char
                        variables[v0] = [0, 0, 0, 0]
                        valuesSet += 1

                    elif valuesSet == 1:
                        variables[v0][0] = int(char)
                        valuesSet +=1

                    elif valuesSet == 2:
                        variables[v0][1] = int(char)
                        valuesSet += 1 

                    elif valuesSet == 3:
                        variables[v0][2] = int(char)
                        valuesSet += 1

                    elif valuesSet == 4:
                        variables[v0][3] = int(char)
                        currentCommand = None
                        valuesSet = -1
                    continue
                
                if currentCommand == "D":
                    if char != "D":
                        if char == "C":
                            lineContent += f"{chr(cells(X, Y))} "
                        elif char == "X":
                            lineContent += f"{chr(X)} "
                        elif char == "Y":
                            lineContent += f"{chr(Y)} "
                        elif char in variables.keys():
                            for x in range(variables[char][0], variables[char][0]+(variables[char][2]-1)):
                                for y in range(variables[char][1], variables[char][1]+(variables[char][3]-1)):
                                    lineContent += chr(cells(x, y))
                                lineContent += "\n"
                        else:
                            print(f"Err: Printed content must be number, or variable on line {currentLine+1}")
                            quit()

                    continue

                if currentCommand == "R":
                    if valuesSet == 0:
                        v0 = input("> ")
                    else:
                        if char not in variables.keys():
                            print("Err: variable must have defined area and size before setting")
                            quit()
                        vSet = 0
                        for x in range(variables[char][0], variables[char][0]+(variables[char][2]-1)):
                            for y in range(variables[char][1], variables[char][1]+(variables[char][3]-1)):
                                cells(x, y, ord(v0[vSet]))
                                vSet += 1
                    
                        currentCommand = None
                        valuesSet = -1
                    continue

                if currentCommand == "P":
                    if valuesSet == 0:
                        v0 = char
                        valuesSet +=1

                    elif valuesSet == 1:
                        v1 = char
                        valuesSet += 1
                    else:
                        for x in range(variables[v0][2]):
                            for y in range(variables[v0][3]):
                                cells(x+int(v1), y+int(char), cells(variables[v0][0]+x, variables[v0][1]+y))
                        
                        valuesSet = -1
                        currentCommand = -1
                    continue


                
            if valuesSet >= 0 and currentCommand not in "D + -".split():
                print(f"Err: Line {currentLine+1} missing arguments.")
                quit()

            if lineContent != "":
                try:
                    print(chr(int(lineContent)))
                except ValueError:
                    print(lineContent)
                lineContent = ""

            currentLine += 1
        
        # if viewMemUtilization:
    except Exception as e:
        print(f"Error on line {currentLine+1}\n{e}")





if __name__ == "__main__":
    Interpret("./snake.bos")

