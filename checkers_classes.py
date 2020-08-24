import pygame
import math
class Game:
    def __init__(self,size,x,y):
        #self.win=win
        self.size=size
        self.pos=(x,y)
        self.burners=[]
        self.possibales=[]
        self.tiles=[]
        self.dic_tile={}
        self.p1=Player((255,255,255),-1,self)
        self.corrent=self.p1
        self.p2=Player((255,0,0),1,self)
        self.enemy=self.p2
        self.selected=None
        self.double=False

    def init_board(self):
        on = -1
        for j in range(8):
            for i in range(8):
                if on == 1:
                    self.tiles.append(BlackTile(self.size/8, self.size/8, (self.pos[0]+self.size/8 * i,self.pos[1]+self.size/8 * j), (j + 1, i + 1)))
                on *= -1
            on *= -1
        for tile in self.tiles:
            self.dic_tile[tile.name]=tile
        self.corrent.start()
        self.enemy.start()
        print(self.tiles)
        print(self.dic_tile)

    def draw_board(self,win):
        pygame.font.init()
        text = pygame.font.SysFont(None, 25)
        win.fill((255, 255, 255))
        for i in range(8):
            crn_txt = text.render(str(i + 1), True, (0, 0, 0))
            win.blit(crn_txt, (self.pos[0]-self.size/16, self.size/8 * i +self.size*3/16))
        for i in range(8):
            crn_txt = text.render(str(i + 1), True, (0, 0, 0))
            win.blit(crn_txt, (self.size/8 * i +self.size*3/16, self.pos[0]-self.size/16))
        for tile in self.tiles:
            tile.draw(win)
            crn_txt = text.render(str(tile.name[0]) + "," + str(tile.name[1]), True, (255, 255, 255))
            win.blit(crn_txt, (tile.pos[0], tile.pos[1]))
        for pawn in self.corrent.pawns+self.enemy.pawns:
            for tile in self.tiles:
                if tile.name==pawn.tile:
                    pawn.draw(win,(tile.pos[0]+math.floor(self.size/16),tile.pos[1]+math.floor(self.size/16)),math.floor(self.size/20))
        for tile in self.tiles:
            tile.color = (0, 0, 0)


    def get_burners(self):
        burners=[]
        for pawn in self.corrent.pawns:
            for move in pawn.get_poss():
                if move[0]!=None:
                    burners.append((pawn,move[1]))
        return burners
    def end_turn(self):
        self.selected=None
        self.double=False
        remp=self.corrent
        self.corrent=self.enemy
        self.enemy=remp
        self.burners = self.get_burners()

class BlackTile:
    def __init__(self,width,height,pos,name):
        self.width=width
        self.height=height
        self.pos=pos
        #self.win=win
        self.name=name
        self.color=(0,0,0)
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.pos[0],self.pos[1],self.width,self.height))

class Pawn:
    def __init__(self,tile,num,player):
        self.player=player
        self.color=player.color
        self.dir=player.dir
        self.tile=tile
        self.num=num
        self.game=player.game

    def draw(self,win,pos,rad):
        pygame.draw.circle(win,self.color,(math.floor(pos[0]),math.floor(pos[1])),rad)

    def eaten(self,corrent,enemy):
        self.player.pawns.remove(self)

    def double_eat(self):
        self.game.burners=[]
        tiles=self.game.dic_tile
        enemys=self.game.enemy
        corrent=self.game.corrent
        poss = []
        friendlys = [tile.tile for tile in corrent.pawns]
        badguys = [tile.tile for tile in enemys.pawns]
        for i in [-1, 1]:
            for j in [-1,1]:
                if 0 < self.tile[0] + j < 9 and 0 < self.tile[1] + i < 9:
                    tile=tiles[(self.tile[0] +j, self.tile[1] + i)]
                    for pawn in enemys.pawns:
                        if pawn.tile == tile.name and 0 < tile.name[0] + j< 9 and 0 < tile.name[1] + i < 9 and (tile.name[0] + j, tile.name[1] + i) not in friendlys + badguys:
                            poss.append((pawn, (tile.name[0] + j, tile.name[1] + i)))
        return (len(poss)>0,poss)

    def move(self,move):
        enemy = self.game.enemy
        corrent = self.game.corrent
        self.tile=move[1]
        if self.dir==1:
            end=8
        elif self.dir==-1:
            end=1
        if self.tile[0]==end:
            self.crown()
        if move[0]!=None:
            move[0].eaten(enemy,corrent)
            check=self.double_eat()
            if check[0]:
                self.game.possibales=check[1]
                self.game.double=True
            else:
                self.game.possibales=[]

        else:
            self.game.possibales=[]

    def get_poss(self):
        tiles = self.game.dic_tile
        enemys = self.game.enemy
        corrent = self.game.corrent
        poss=[]
        friendlys=[tile.tile for tile in corrent.pawns]
        badguys=[tile.tile for tile in enemys.pawns]
        for i in [-1,1]:
            if 0<self.tile[0]+1*self.dir<9 and 0<self.tile[1]+i<9:
                tile=tiles[(self.tile[0]+1*self.dir,self.tile[1]+i)]
                if tile.name not in friendlys + badguys:
                    poss.append((None,tile.name))
                elif tile.name in badguys:
                    if 0<tile.name[0]+1*self.dir<9 and 0<tile.name[1]+i<9 and (tile.name[0]+1*self.dir,tile.name[1]+i) not in friendlys+badguys:
                        poss.append((enemys.pawns[badguys.index(tile.name)], (tile.name[0] + 1 * self.dir, tile.name[1] + i)))

        return poss

    def crown(self):
        self.__class__=Queen
        self.player.Q+=1


class Player:
    def __init__(self,color,dir,game):
        self.color=color
        self.dir=dir
        self.pawns=[]
        self.game=game
        self.Q=0

    def start(self):
        for i in range(12):
            if self.dir<0:
                self.pawns.append(Pawn(self.game.tiles[self.dir*(i+1)].name,i,self))
            else:
                self.pawns.append(Pawn(self.game.tiles[i].name,i,self))

class Queen(Pawn):
    def __init__(self,tile,num,player):
        super().__init__(self,tile,num,player)

    def draw(self,win,pos,rad):
        pygame.draw.circle(win, self.color, (math.floor(pos[0]), math.floor(pos[1])), rad)
        pygame.draw.circle(win, (255,255,0), (math.floor(pos[0]), math.floor(pos[1])), rad,3)

    def get_poss(self):
        def checkline(self,tiles,badguys,friendlys,i,j,n,enemys):
            out=[]
            if 0 < self.tile[0] + i*n < 9 and 0 < self.tile[1] + j*n < 9:
                tile= tiles[(self.tile[0] + i*n, self.tile[1] + j*n)]
                if tile.name not in badguys + friendlys:
                    out.append((None,tile.name))
                    out+=checkline(self,tiles,badguys,friendlys,i,j,n+1,enemys)
                elif tile.name in badguys:
                    if (tile.name[0]+i,tile.name[1]+j) not in badguys+friendlys:
                        pawn=enemys.pawns[badguys.index(tile.name)]
                        if 0<tile.name[0]+i<9 and 0<tile.name[1]+j<9 and tile.name:
                            out.append((pawn,(tile.name[0]+i,tile.name[1]+j)))
                    return out
            return out

        tiles = self.game.dic_tile
        enemys = self.game.enemy
        corrent = self.game.corrent
        poss=[]
        friendlys = [tile.tile for tile in corrent.pawns]
        badguys = [tile.tile for tile in enemys.pawns]
        for i in [-1,1]:
            for j in [-1,1]:
                poss+=checkline(self,tiles,badguys,friendlys,i,j,1,enemys)

        return poss

    def eaten(self,corrent,enemy):
        self.player.pawns.remove(self)
        self.player.Q-=1

class Button:
    def __init__(self,pos,width):
        self.pos=pos
        self.active=False
        self.color=(0,255,0)
        self.width=width
        self.massage="Activate MiniMax"
    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.pos[0], self.pos[1], self.width, 30))
        text = pygame.font.SysFont(None, 25)
        crn_txt = text.render(self.massage, True, (255, 255, 255))
        win.blit(crn_txt, (self.pos[0], self.pos[1]))
    def press(self):
        if self.active:
            self.active=False
            self.color=(0,255,0)
            self.massage = "Activate MiniMax"
        else:
            self.active=True
            self.color = (255,0, 0)
            self.massage = "Shutdown MiniMax"







