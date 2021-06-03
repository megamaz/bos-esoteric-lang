# Bytes Or Something
The worst programming language out there.
# How does it work?
You have access to a 255x255 grid of cells - each who can have a value from 0-255. Similarly to brainfuck, to increment or decrement, you use `+` and `-`.\
NOT similary to brainfuck, you can't just use `^` `v` `>` and `<` to move your pointer. Instead, you can set your pointer to a specific location using a command.\
The file is newline separated. \
Comments are `#`
# Commands
## M
Usage: `M [new pointer X] [new pointer Y]`\
Moves your pointer to a new cell. New position cannot be a variable!
## S
Usage: `S [new value]`\
Sets the current cell value. Must be 0-255.
## F
Usage: `F [current file line]`\
Moves the currently being read line to a specific line. You can go backwards, and re-read parts of the file, or forwards which will skip parts of the file.
## I
Usage: `I [value 1] [value 2]`\
Will implement logic. All lines of code will only be read if `value 1` and `value 2` are equal.
## E
Usage: `E`\
Marks the end of an `I` statement.
## V
Usage: `V [name] [xAdress] [yAdress] [width] [height]`\
By far the most complicated command. The variable will cover an area of your grid of cells. The `xAdress` will be the left wall, while the `yAdress` will be the top wall. The `width` and `height` defines the... well, width and height of the area. 0 will not an acceptable value for either of them.
## D
Usage: `D [variable name / number]`\
Will display all the cells of a variable as ascii values, where each new row represents a new line, or a single ascii value.
## R
Usage: `R [variable name]`\
Will accept any length of input and set all their ascii values to the cells. (if width overflow, then go to next row). If there are too many characters for the variable to handle, an error will arise.
## P
Usage 1: `P [variable 1] [X] [Y]`\
... Copies variable content from variable 1 to a new location.\
Why did I use P for this? Because C for copy is already taken and D for duplicate is already taken.\
What do P stand for? idfk
# Constant Variables
These are values that cannot be assigned to or modified.
## X
The pointer's current X value.
## Y
The pointer's current Y value.
## C
The cell's current value.
