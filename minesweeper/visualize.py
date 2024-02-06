import pygame
from minesweeper import Game 

class Visual(Game):

    def __init__(self, manual=True,width=9, height=9, mines=10):

        #Init and set our pygame properties
        pygame.init()

        pygame.mixer.init() 

        self.screen = pygame.display.set_mode((144,144))
        
        self.clock = pygame.time.Clock()

        self.tilemap_image = pygame.image.load('tiles.png')
        
        self.tmap = [[9 for _ in range(9)] for _ in range (9)]
        
        self.lost = False

        #init a game instance
        super().__init__(manual, width, height, mines)

        self.inst = self.gameLoop()
    
    def convertMap(self, coord):
        x,y = coord
        return self.Grid[y][x]
        
    def draw_tile(self,x,y,tile_idx):
        self.screen.blit(self.tilemap_image, (x*16, y*16), (tile_idx * 16, 0, 16, 16))

    def setTile(self, coord, tile):
        x,y = coord
        match tile:
            case 'B':
                self.tmap[y][x] = 11
            case None:
                self.tmap[y][x] = 0
            case _:
                self.tmap[y][x] = int(tile)
    
    def getTile(self, pos):
        x,y = pos
        relx = x//16; rely = y//16
        
        return self.tmap[rely][relx]
    
    def unveil(self, coord):
        x,y = coord
        relx = x//16; rely = y//16
        
        if (relx,rely) in self.bombs:
            self.lost = True

        if (relx,rely) in self.unveiled:
            return
        
        self.setTile((relx,rely), self.convertMap((relx,rely)))
        self.unveiled.append((relx,rely))

    def placeFlag(self, coord):
        x,y = coord
        relx = x // 16; rely = y//16
        
        if (relx,rely) in self.unveiled:
            return

        if (relx,rely) not in self.flags:
            self.flags.append((relx,rely))
            self.setTile((relx, rely), 12)
        else:
            self.removeFlag((relx,rely))
            self.setTile((relx,rely), 9)

    def gameLoop(self):
        while not self.lost:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.lost = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        self.unveil(pos)       
                    elif event.button == 3:
                        self.placeFlag(pos)
                    self.checkWin()

            for y, row in enumerate(self.tmap):
                for x, tile in enumerate(row):
                    self.draw_tile(x,y,tile)


            pygame.display.flip()
            self.clock.tick(15)
        


