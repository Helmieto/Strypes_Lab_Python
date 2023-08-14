import random
from sys import argv


maze_str = """
11111111111111111111
10000000000000000001
10111111101011111101
10000000101010110101
10111111101010110101
10100000000010110101
10101110111110110101
10101010100000110101
10001000001000000001
11111111111111111111
"""


maze = [
    [int(digit) for digit in row] for row in maze_str.strip().split("\n")
]
maze[3][16] = 7


# initializes grid
def init_maze ( l ,w):
    maze = [ [ 1] * l for i in range (w) ]
    for i in range(1, w-1, 2):
        for j in range(1, l-1, 2):
           maze[i][j] = 9
    return maze


# creates random maze from grid
def walk(maze, x, y) :
    maze [ x ] [ y ] = 0
    neighbors = [ [ x - 2, y ] , [ x + 2, y ] , [ x , y - 2] , [x , y + 2] ]
    random . shuffle(neighbors)
    for newX, newY in neighbors :
        if ( newX in range ( 1 , len(maze)) and newY in range ( 1 , len ( maze [ 0 ]) ) ) :
            if maze [ newX ] [ newY ] == 9:
                maze [ ( newX + x ) // 2 ] [ ( newY + y ) // 2 ] = 0
                walk (maze , newX , newY )


# sets a target in a random maze
def setGold(maze):
    isSet = False
    while not isSet:
        x_cord = random.randint(1, len(maze) - 1)
        y_cord = random.randint(1, len(maze[0]) - 1)
        if maze[x_cord][y_cord] == 0:
            maze[x_cord][y_cord] = 7
            isSet = True


# recursive backtracking
def solveMazeRecursive(maze, x, y):
    if x not in range(1, len(maze) - 1) or y not in range(1, len(maze[0]) - 1):
        return False

    if maze[x][y] == 7:
        return True
    if maze[x][y] == 1 or maze[x][y] == 5 or maze[x][y] == 3:
        return False
    if maze[x][y] == 0:
        maze[x][y] = 3

#down
    if solveMaze(maze, x + 1, y):
        return True
    #right
    if solveMaze(maze, x, y + 1):
        return True
    #up
    if solveMaze(maze, x - 1, y):
        return True
#left
    if solveMaze(maze, x, y - 1):
        return True

    maze[x][y] = 5
    return False


#print function
def printMaze(maze):
    for row in maze:
        for symbol in row:
            if symbol == 0:
                print(' ', end=' ')
            if symbol == 1:
                print('#', end=' ')
            if symbol == 3:
                print('.', end=' ')
            if symbol == 5:
                print('x', end=' ')
            if symbol == 7:
                print('g', end=' ')
        print('')


def solveMaze(x, y):
    #stores all legal moves
    moves = [(x,y)]

    #stores all visited cells
    visited = []

    #stores the cells that are intersections
    intersections=[]

    #iterates through moves and ques new ones
    while moves:
        x, y = moves.pop()
        visited.append((x,y))

        if maze[x][y] == 0:
            maze[x][y] = 3

        neighbours = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]

        #counter for number of valid neighbours
        counter = 0

        for newX, newY in neighbours:
            #checks if the neighbours are valid
            if newX in range(1, len(maze) - 1) and newY in range(1, len(maze[0]) - 1) and (maze[newX][newY] == 0 or maze[newX][newY] == 7):
                                #if the neighbour is the target it ends
                if maze[newX][newY] == 7:
                    return True

                #it marks valid neighbours as possible moves
                moves.append((newX,newY))

                counter += 1
                                #if there are more than 1 valid neighbours the cell is an intersection
                if counter > 1:
                    intersections.append((x,y))

        #if there are no valid neighbour we either went to a corner or reached a path we alreade passed through
        if counter == 0:

            endedDeleting = False

            while not endedDeleting:
#mark all visited cells until the last intersection as not leading to the target
                while visited[-1] != intersections[-1]:
                    x_pop, y_pop = visited.pop()
                    maze[x_pop][y_pop] = 5

#checks if the intersection has valid neighbours or not
                x, y = intersections.pop()
                tmp_neighbours = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]

                for newX, newY in tmp_neighbours:
                    # if it has it puts it back into intersections list
                    #else it is deleted and the process of marking invalid path is repeated
                    if maze[newX][newY] == 0:
                        intersections.append((x, y))
                        endedDeleting = True

    return False


x = int(argv[1])
y = int(argv[2])

solveMaze(x, y)
printMaze(maze)
