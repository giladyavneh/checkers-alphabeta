import copy
from checkers_classes import Queen, Pawn
#still returns the first pawn as an option
def play(game1,n,alpha,beta,max):
    if max:
        potential=[-20,None,None]
    else:
        potential = [20, None, None]
    if n==0 or len(game1.p2.pawns)==0 or len(game1.p1.pawns)==0:
        #print(type(len(game1.corrent.pawns) - len(game1.enemy.pawns)))
        i=0
        if game1.selected!=None or len(game1.burners)>0:
            i=game1.corrent.dir
        return [len(game1.p2.pawns)+game1.p2.Q-len(game1.p1.pawns)+game1.p1.Q+i]
    else:
        if game1.double:
            if len(game1.possibales)==0:
                game1.possibales=game1.selected.double_eat()[1]
            i=game1.corrent.pawns.index(game1.selected)
            if len(game1.burners) > 0:
                bi=game1.corrent.pawns.index(game1.burners[0][0])
            for poss in game1.possibales:
                game = copy.deepcopy(game1)
                pawni=game.corrent.pawns[i]
                pawni.tile = poss[1]
                if isinstance(pawni, Queen) == False:
                    if game.corrent.dir == 1:
                        if pawni.tile[0] == 8:
                            pawni.__class__=Queen
                            game.corrent.Q+=1
                    elif game.corrent.dir == -1:
                        if pawni.tile[0] == 0:
                            pawni.__class__ = Queen
                            game.corrent.Q += 1
                if poss[0] != None:
                    for bad in game.enemy.pawns:
                        if bad.num == poss[0].num:
                            if isinstance(bad,Queen):
                                game.enemy.Q-=1
                            game.enemy.pawns.remove(bad)
                b = False
                if len(game.burners) > 0:
                    for mov in game.burners:
                        if poss[1] != mov[1]:
                            b = True
                            if isinstance(game.corrent.pawns[bi],Queen):
                                game.corrent.Q-=1
                            game.corrent.pawns.remove(game.corrent.pawns[bi])

                check = pawni.double_eat()
                if check[0] and not b:
                    game.double = True
                    game.selected = pawni
                    game.burners = []
                    game.possibales=check[1]
                else:
                    game.double = False
                    game.end_turn()
                if game.corrent.dir == -1:
                    eval = play(game, n - 1,alpha,beta, False)[0]
                    if eval < beta:
                        beta = eval

                else:
                    eval = play(game, n - 1,alpha,beta, True)[0]
                    if eval > alpha:
                        alpha = eval
                if max:
                    if eval > potential[0]:
                        potential = [eval, game1.selected, poss]
                else:
                    if eval < potential[0]:
                        potential = [eval, game1.selected, poss]
                if beta <= alpha:
                    break

        else:
            index=-1
            if len(game1.burners) > 0:
                bi=game1.corrent.pawns.index(game1.burners[0][0])
            burns = [mov[1] for mov in game1.burners]
            for pawn in game1.corrent.pawns:
                index+=1
                for poss in pawn.get_poss():
                    game=copy.deepcopy(game1)
                    pawni=game.corrent.pawns[index]
                    pawni.tile=poss[1]
                    if isinstance(pawni,Queen)==False:
                        if game.corrent.dir==1:
                            if pawni.tile[0]==8:
                                pawni.__class__ = Queen
                                game.corrent.Q += 1
                        elif game.corrent.dir==-1:
                            if pawni.tile[0]==0:
                                pawni.__class__ = Queen
                                game.corrent.Q += 1
                    if poss[0]!=None:
                        for bad in game.enemy.pawns:
                            if bad.num==poss[0].num:
                                if isinstance(bad, Queen):
                                    game.enemy.Q -= 1
                                game.enemy.pawns.remove(bad)
                    b=False
                    if len(game.burners) > 0:

                        if poss[1] not in burns:
                            b=True
                            if isinstance(game.corrent.pawns[bi],Queen):
                                game.corrent.Q-=1
                            game.corrent.pawns.remove(game.corrent.pawns[bi])

                    check = pawni.double_eat()
                    if check[0] and not b:
                        game.double = True
                        game.selected = pawni
                        game.burners=[]
                        game.possibales=check[1]
                    else:
                        game.double = False
                        game.end_turn()
                    if game.corrent.dir == -1:
                        eval = play(game, n - 1,alpha,beta, False)[0]
                        if eval < beta:
                            beta = eval
                    else:
                        eval = play(game, n - 1,alpha,beta, True)[0]
                        if eval > alpha:
                            alpha = eval
                    if max:
                        if eval > potential[0]:
                            potential = [eval, pawn, poss]
                    else:
                        if eval < potential[0]:
                            potential = [eval, pawn, poss]
                    if beta <= alpha:
                        break
        return potential