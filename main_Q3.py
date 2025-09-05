#ASSINGNMENT 2 - Question 3 #

import turtle as trl
# user inputs to decide geometeric pattern (wondering if I should use float or int)
sides = int(input("Enter number of sides: "))
side_length = int(input("Enter side length: "))
rdepth = int(input("Enter the recursion depth: "))

#turtle screen and tool setup
screen = trl.Screen()
t = trl.Turtle()

#defining the ident using a recursive function
def indent(side_length,rdepth):
    #spliting the length into 3 parts line|point|line
    side_length /= 3
    #base case as in assignment if depth == 0 draw a line
    if rdepth == 0:
        t.fd(side_length)
    #the recursive looping - turns 60|120|60 create the EQ triangle point and the ident() 
    # recursive looping creates the line + layering of the --V--
    else:
        indent(side_length, rdepth - 1)
        t.right(60)
        indent(side_length, rdepth - 1)
        t.left(120)
        indent(side_length, rdepth - 1)
        t.right(60)
        indent(side_length, rdepth - 1)

# this creates the shape and the nests the recusive ident() function inside to create the 
# geometric patterns. It takes sides (sides of the shape e.g 4 woulde be a square), side_length (length of sides) and the rdepth (recursive depth number)
def geoPattern(sides,side_length,rdepth):
    for i in range(sides):
        #creates the "indents"
        indent(side_length,rdepth)
        #creates the shape
        t.right(360/sides)


#using the function
geoPattern(sides, side_length,rdepth)

