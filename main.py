import pygame
from checkers_classes import BlackTile, Player, Pawn, Game, Button,Queen
import minimax
import math

height=400
width=600
win=pygame.display.set_mode((width,height))
pygame.display.set_caption("checkersAI")
run=True




g=Game(300,50,50)
g.init_board()
button=Button((g.pos[0]+g.size,g.pos[1]),g.size/2)

while run:
    corrent=g.corrent
    enemy=g.enemy
    mouse_pos = pygame.mouse.get_pos()

    g.draw_board(win)
    button.draw(win)
        #if poss include eatable enemy-append tiles to burners
    for poss in g.burners:
        g.dic_tile[poss[1]].color=(70,0,0)
        g.dic_tile[poss[0].tile].color = (70, 0, 0)

    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN:
            if button.pos[0]<=mouse_pos[0]<=button.pos[0]+g.size/2 and button.pos[1]<=mouse_pos[1]<=button.pos[1]+30:
                button.press()
            for tile in g.tiles:
                if g.double==True:
                    if tile.name not in [move[1] for move in g.possibales] and tile.pos[0]<=mouse_pos[0]<=tile.pos[0]+g.size/8 and tile.pos[1]<=mouse_pos[1]<=tile.pos[1]+g.size/8:
                        g.end_turn()
                        break
                for pawn in corrent.pawns:
                    if tile.name==pawn.tile and tile.pos[0]<=mouse_pos[0]<=tile.pos[0]+g.size/8 and tile.pos[1]<=mouse_pos[1]<=tile.pos[1]+g.size/8:
                        g.selected=pawn
                        g.possibales=pawn.get_poss()
                if g.selected!=None:
                    for move in g.possibales:
                        if tile.name==move[1] and tile.pos[0]<=mouse_pos[0]<=tile.pos[0]+g.size/8 and tile.pos[1]<=mouse_pos[1]<=tile.pos[1]+g.size/8:
                            g.selected.move(move)
                            if len(g.burners)>0 and (g.selected,move[1]) not in g.burners:
                                g.burners[0][0].eaten(corrent,enemy)
                                g.end_turn()
                                break
                            else:
                                if len(g.possibales)==0:
                                    g.end_turn()
                                    break

        if event.type==pygame.QUIT:
            run=False

    if g.selected != None:
        for ent in g.possibales:
            g.dic_tile[ent[1]].color=(0,0,70)
            g.dic_tile[g.selected.tile].color=(0,0,70)

    if button.active:
        if corrent.dir==1:
            m=minimax.play(g,4,-50,50,True)

            for pawn in corrent.pawns:

                if pawn.num==m[1].num:
                    pawn.move(m[2])
                    g.selected=pawn
                    if len(g.burners) > 0 and (pawn, m[2]) not in g.burners:
                        g.burners[0][0].eaten(corrent, enemy)
                        g.selected=None
                        g.end_turn()
                    elif m[2][0]!=None and g.selected.double_eat()[0]:
                        g.double=True
                    else:
                        g.end_turn()



            print(m[0])







    pygame.display.update()