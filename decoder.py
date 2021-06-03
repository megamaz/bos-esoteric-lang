"""A decoder for my completely garbage custom language: BOS. (Bytes Or Something).
Here's how it works;
You have a 2D array of cells, 255x255.
You have a pointer which... well, points to a location.
The pointer starts in the top left - 0, 0
You can set the pointer's position by doing `M [x] [y]`
You can set the current cell's value by doing `S [v]` (values must be 0-255)

Another thing you can do is change the currently being read line. A file will be read line by line from top to bottom.
if you use the command `F [l]` you can make the currently being read line be earlier, or later.
So, an eternal loop would be
```
0 # code here
1 
2 F 0
```

You can also have logic. Logic is done using the `I [v1] [v2]`. Keep in mind you can only check if v1 and v2 are equal.
After any logic, indentation is not needed. Once you are done with your current logic area, use an `E`.

Settings variables is easy as pie. Use the `V [name] [addressX]X[addressY] [width] [height]` command. This will set a value based on the address of the grid of cells. Keep in mind you can only set variables based
off of this grid of cells and no other way!

To display content to the console, use the `D [content]` command. If the content is a number, the ascii value will be displayed.

To input content, use the `R [variable]` command. The response will be saved to the variable.
If inputted contents width does not match the width of the variable, then the next row will be used to continue.
If the total amount of cells is not enough to store all ascii values, then an error will be raised.



Ok what about math?
to increment the current cell by one, simply have a `+`. All `+`s stringed together will increment the current cell.
Keep in mind `+` connected to one another is more efficient than `+ + +`!

to decrement the current cell, use `-`. Same thing as above.

Built in constants are:
X - pointer X
Y - pointer Y
C - current cell value

That's it! have fun lol. 
to add comments use #
"""
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
                        X = int(char)
                        valuesSet = 1
                    elif valuesSet == 1:
                        Y = int(char)
                        currentCommand = None
                        valuesSet = -1
                    continue

                if currentCommand == "S":
                    if char in variables.keys():
                        cells(X, Y, variables[char])
                    elif char == "C":
                        cells(X, Y, cells(X, Y)) # why
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
                        variables[v0][0] = int(char.split("X")[0])
                        valuesSet +=1

                    elif valuesSet == 2:
                        variables[v0][1] = int(char.split("X")[1])
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
    Interpret("./.bos")

