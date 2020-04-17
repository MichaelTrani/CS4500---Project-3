"""
Michael Trani
9/30/2019
Introduction to the Software Profession:
CompSci 4500 - 001
Homework 3

This program plays a painting game, described in section Reference 01.
The program takes input from the user to determine how many blobs of paint will be dropped.
This input, n, is used to determine the size of the display screen and the speed at which 
blobs will drop. A large n will display faster than one of a smaller size.
A second number, k, determines how many paintings are created.

The paintings variables are stored in an object, paintings, and the paintings are stored
in an object list, gallery.
The primary component of the painting object is a 2D list, grid, populated with all zeros, indicating
a blank canvas.

The program chooses random numbers to determine x and y coordinates on a painting's grid. 
A random paint color is selected and its numerical value is stored in the grid's position
determined previously.  The coordinate and painting number is stored as a string in the
list celluse.

The grid is displayed and updated as each color is added.

Once every element in the grid contains a non-zero value the painting is completed
The program will repeat this process until all paintings have been completed.



#### Reference 01 ####

 You have an N X N grid lying on the floor, where N is an integer between 2 and 15 inclusive. You are
capable of dropping blobs of paint on to the grid in such a way that The blob lands randomly on the grid on to only
one cell (each time) The blob does not splatter into any of the other cells The blob always falls somewhere on the
grid If subsequent blobs of paint fall on that same cell, that’s OK, and again there is no splatter In order to
“complete” your painting (and our apologies to Jackson Pollock), you continue dropping paint blobs, one at a time,
until each cell has at least one paint blob dropped on to it. When the painting is complete, every cell contains
paint, and some cells may have LOTS of paint.

For homework 3, you are to write a Python program that does the following:

On the screen, ask the interactive user to enter an integer between 2 and 15 inclusive. This will determine the size
of your square grid. I will call this number N. If the user enters something illegal, give an error message and keep
asking until you get something appropriate. Next, ask the interactive user to enter an integer between 1 and 10
inclusive. This will tell your program how many “paintings” it will make. I will call this number K. If the user
enters something illegal, give an error message and keep asking until you get something appropriate. Make an N X N
random paint blob painting K times. As each of the K paintings is being made, display graphics on the screen to show
the interactive user how the painting is proceeding. You have great latitude as to how you will display the painting
as it fills up with paint. At the very least, the interactive user should be able to tell which cells have NO paint
so far, which cells have SOME paint so far, and which cell is being painted right at the moment. This minimum would
require three distinct colors. However, you might be able to think of a clever way to visually communicate more
information about the painting than no paint, some paint, and currently being painted. Be thoughtful and creative
about this, please. Give some thought as to how quickly you want to paint drops to appear in your simulation. After a
painting “finishes,” alert the interactive user, and inform them that they must push ENTER (or RETURN) to continue.
After all K paintings have been finished (including the final ENTER push by the user), display the following
statistics from all the paintings: The minimum, maximum, and average number of paint blobs it took to paint a
picture; and the minimum, maximum, and average number that describes the most paint blobs that fell into any one cell
in a painting.
#### End of Reference 01 ####
"""

import pygame as pg
import random

# Define Colors
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
RED = (225, 0, 0)
BLUE = (0, 0, 225)
GREEN = (0, 225, 0)


# Circle class to keep track of all canvas data
class Paintings:
    def __init__(self, iteration, red, blue, green, grid, testID):
        self.iteration = iteration  # count blobs

        # colour-use trackers
        self.red = red
        self.blue = blue
        self.green = green

        self.grid = grid  # canvas for painting, 2D array
        self.testID = testID  # Serial number for each canvas for troubleshooting and identification


# User input and data declarations
n = 0  # size of canvas
k = 0  # canvas count

gallery = []  # array of canvases
celluse = []  # keep track of most used cell
totalRed = 0  # Not used: for color analysis
totalBlue = 0  # Not used: for color analysis
totalGreen = 0  # Not used: for color analysis
totalBlobs = 0  # Total blob count of all paintings
blobMax = 0  # Determine maximum blob count
blobMin = 1000000  # Determine minimum blob count, unlikely to trigger false positive
bigBlob = " "  # Get the name of the biggest blob painting
littleBlob = " "  # Get the name of the smallest blob painting

# Get canvas size and count from user. Both use same logic checks
lock = True
while lock:
    n = input("Please enter canvas size (2- 15): \n")

    # Ensure input is a digit
    if not n.isdigit():
        print("Invalid entry")
        continue
    # Ensure within bounds
    n = int(n)
    if (n < 2) or (n > 15):
        print("Input is out of bounds")
    # Redundancy check
    if (n >= 2) and (n <= 15):
        lock = False

lock = True
while lock:
    k = input("Please enter how many paintings you would like (1-10): \n")
    # Ensure input is a digit
    if not k.isdigit():
        print("Invalid entry")
        continue
    # Ensure within bounds
    k = int(k)
    if (k < 1) or (k > 10):
        print("Input is out of bounds")
    # Redundancy check
    if (k >= 1) and (k <= 10):
        lock = False

# Construct gallery array of Paintings objects
for i in range(0, k):
    gallery.append(Paintings(int(0), int(0), int(0), int(0), [], ("Painting: " + str(i))))
    gallery[i].grid = [[int(0)] * n for i in range(n)]  # Set 2D list to 0 for a "blank" canvas

# Initialize pygame and make preparations for window
s_width = 15
s_height = 15

# An attempt to make the fill for smaller n (better aesthetics)
if n >= 8:
    MARGIN = 1
else:
    MARGIN = 2

pg.init()
window = [(n+1) * 15, (n+1) * 15]  # This seems to be the best fit after trial and error
screen = pg.display.set_mode(window)

clock = pg.time.Clock()  # Used to change frame rate

# Larger paintings have larger frame rates to cut down on runtime
# Smaller paintings have a lower frame rate so user can see changes
clockTime = 60  # used to suppress an error
if n >= 7:
    clockTime = 500
if n < 7:
    clockTime = 30
if n < 5:
    clockTime = 3


color = WHITE  # Declare color and give a default value

for j in range(0, k):  # Loop for all paintings
    pg.display.set_caption(gallery[j].testID)

    lock = True
    while lock:  # Inelegant to avoid blank paint spots.
        pg.display.flip()  # Update display

        # Check for complete canvas before painting process. ##DO NOT MOVE##
        if not any(0 in sublist for sublist in gallery[j].grid):
            lock = False

        # Assign location to drop blob
        x = random.randint(0, n - 1)
        y = random.randint(0, n - 1)

        # Pick a paint
        blob = random.randint(1, 3)

        # Paint at location
        gallery[j].grid[x][y] = blob

        # Keep Track of painted square
        cellNum = str(x) + "," + str(y) + " " + gallery[j].testID  #" Painting #: " + str(j)
        celluse.append(cellNum)

        # Keep track of paint usage
        if blob == 1:
            gallery[j].red += 1
        if blob == 2:
            gallery[j].blue += 1
        if blob == 3:
            gallery[j].green += 1

        # Display paintings
        for row in range(n):
            for column in range(n):

                if gallery[j].grid[row][column] == 0:
                    color = WHITE
                if gallery[j].grid[row][column] == 1:
                    color = RED
                if gallery[j].grid[row][column] == 2:
                    color = BLUE
                if gallery[j].grid[row][column] == 3:
                    color = GREEN

                # Draw screen
                pg.draw.rect(screen, color, [(MARGIN + s_width) * column + MARGIN,
                                             (MARGIN + s_height) * row + MARGIN,
                                             s_width,
                                             s_height])

        gallery[j].iteration += 1  # keeping track of how many blobs are on a painting
        totalRed += gallery[j].red  # Color tracking
        totalBlue += gallery[j].blue
        totalGreen += gallery[j].green

        clock.tick(clockTime)  # Frame rate limiter
        celluse.append(cellNum)  # Updates display

    # Compare the blob min and max after each painting is complete
    if gallery[j].iteration > blobMax:  # Max blobs per painting
        blobMax = gallery[j].iteration
        bigBlob = gallery[j].testID

    if gallery[j].iteration < blobMin:  # Min blobs per painting
        blobMin = gallery[j].iteration
        littleBlob = gallery[j].testID

    totalBlobs += gallery[j].iteration  # keep track of all blobs

    # Print extra data for easy fact checking
    print(gallery[j].testID)
    print("Blobs dropped: ", str(gallery[j].iteration))
    print("Red used: ", str(gallery[j].red), " Blue used: ",
          str(gallery[j].blue), " Green used: ", str(gallery[j].green))
    input('Press ENTER to continue')  # Pause to admire the pretty picture

input('That was the last one!\nPress ENTER for gallery data')
print('#######################')

averageBlobs = totalBlobs / k
print("The average blob count for all paintings was:", str(averageBlobs))
print("The most amount of paint blobs was: ", bigBlob, " with: ", str(blobMax), " blobs.")
print("The minimum amount of paint blobs was: ", littleBlob, " with: ", str(blobMin), " blobs.")

averageCells = totalBlobs / (k * n * n)
print("The average paint per square was: ", str(averageCells))

mostVisit = max(set(celluse), key=celluse.count)
countMost = celluse.count(mostVisit)
print("Most painted square was: ", mostVisit, " with ", countMost, " blobs.")

leastVisit = min(set(celluse), key=celluse.count)
countLeast = celluse.count(leastVisit)
print("Least painted square was: ", leastVisit, " with ", countLeast, " blobs.")

print('#######################')
input('Press ENTER to exit')
