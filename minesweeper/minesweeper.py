import random

class Game:
    def __init__(self,manual=True, width=9, height=9, mines=10):
        self.width = width
        self.height = height
        self.mines = mines
        self.manual = manual

        self.Grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.bombs = []
        self.flags = []
        self.unveiled = []

        self.generate()
        self.lost = False

        self.inst = self.gameLoop()

    def __str__(self):
        ret = ""
        #ret = "Filled board (Cheater View): \n"
        #for row in range(self.height):
        #    for col in range(self.width):
        #        if self.Grid[row][col] == None:
        #            ret += " "
        #        else:
        #            ret += str(self.Grid[row][col])
        #    ret += "\n"
        
        ret += "Current Board View: \n"
        for row in range(self.height):
            for col in range(self.width):
                if (col,row) in self.unveiled:
                    if self.Grid[row][col] == None:
                        ret += " "
                    else:
                        ret += str(self.Grid[row][col])
                elif (col,row) in self.flags:
                    ret += "F"
                else:
                    ret += "X"
            ret += "\n"
        return ret
            
    def gameLoop(self):
        while(not self.lost):
            print(self)
            a,x,y = self.textInput()
            match a:
                case "f":
                    if (x-1,y-1) not in self.flags:
                        self.placeFlag((x-1,y-1))
                    else:
                        self.removeFlag((x-1,y-1))
                    print(f"Flag placed on {x,y}")
                case "u":   
                    self.unveil((x-1,y-1))
                    print(f"Tile unveiled at {x,y}")
            if(self.checkWin()):
                print("You won.")
                break

    def textInput(self):
        act = None
        x,y = None,None
        invalid = True
        while(invalid):
            t = input("Enter your next move: (ex. F3,5 or U3,5)")
            if t.startswith("F") or t.startswith("f"):
                    act = "f"
                    x,y = t[1:].split(",")
                    try:
                        x = int(x)
                        y = int(y)
                        invalid = False
                    except:
                        print("There was an error processing the input")
            elif t.startswith("U") or t.startswith("u"):
                    act = "u"
                    x,y = t[1:].split(",")
                    try:
                        x = int(x)
                        y = int(y)
                        invalid = False
                    except:
                        print("There was an error processing the input")
            else:
                print("Invalid input.")
        
        return act,x,y
    
    def generate(self):
        self.plantBombs()
        self.plantNumbers() 

    def plantBombs(self):
        bombsToPlant = self.mines
        while(bombsToPlant > 0):
            x,y = random.randint(0,self.width-1), random.randint(0,self.height-1)

            if(self.Grid[y][x] == None):
                self.Grid[y][x] = "B"
                self.bombs.append((x,y))
                bombsToPlant -= 1
            else:
                continue
        
    def plantNumbers(self):
        for bomb in self.bombs:
            surrounding = self.getSurroundingTiles(bomb)
            for tile_coord in surrounding:
                x,y = tile_coord
                tile = self.Grid[y][x]

                if tile == 'B':
                    continue

                if tile == None:
                    self.Grid[y][x] = '1'
                else:
                    cur = int(tile)
                    self.Grid[y][x] = str(cur+1)

    def getSurroundingTiles(self, coord):
        x,y = coord 

        tiles = []

        for i in range(-1,2):
            for j in range(-1,2):
                tx,ty = x+i, y+j
                if (tx >=0 and tx <= 8) and (ty >= 0 and ty <= 8):
                    tiles.append((tx,ty))

        return tiles
    
    def placeFlag(self, coord):
        if coord not in self.flags:
            self.flags.append(coord)
            print(f"Flags left: {self.mines}")

    def removeFlag(self, coord):
        self.flags.remove(coord)

    def unveil(self, coord):
        if coord in self.bombs:
            print("You lost.")
            self.lost = True
            #reveal all bombs
        else:
            self.unveiled.append(coord)
            print(self.unveiled)

    def checkWin(self):
        for bomb in self.bombs:
            if bomb in self.flags:
                continue
            else:
                return False
            
        return True
        