from tkinter import *
from PIL import Image, ImageTk
import pygame as p
import boardState
import chessegine
import random
height = width = 512
sqsize = height//8
def main():
    p.init()
    screen = p.display.set_mode((height,width))
    game = boardState.boardState()
    ex=True
    ai_turn = False
    startsq=()
    sqselected=[]
    possibility=[]
    while(ex):
        try:
            for e in p.event.get():
                if(e.type == p.QUIT):
                    ex=False
                elif(e.type==p.MOUSEBUTTONDOWN):
                    if(not game.game_over()):
                        location = p.mouse.get_pos()
                        startsq = (location[1]//sqsize,location[0]//sqsize)
                        i,j=startsq
                        if((len(sqselected)==0 and (game.board[i][j]!="--" and game.white==True and game.board[i][j][0]=='w') or len(sqselected)==1)):
                            sqselected.append(startsq)
                            if(len(sqselected)==1):
                                possibility = game.allpossiblemoves(i,j)
                                name_piece = game.board[i][j]
                                possibility = game.out_check_possibility(i,j,name_piece,possibility)
                                print(possibility)
                            if(len(sqselected)==2):
                                nmove = boardState.move(sqselected[0],sqselected[1],game.board)
                                srow,scol = sqselected[0]
                                erow,ecol = sqselected[1]
                                if((sqselected[0]!=sqselected[1] and sqselected[1] in possibility) or game.is_castling(srow,scol,erow,ecol,name_piece)):
                                    game.move_piece(nmove,True)
                                    game.white=False
                                    ai_turn = True
                                    if(game.is_promotion(nmove)):
                                        choice=None
                                        choice = promotion_window()
                                        if(choice is not None):
                                            game.promoting(nmove,choice)
                                        else:
                                            game.undo_move(False)
                                            game.white=True
                                            ai_turn = False
                                print(game.white)
                                print(ai_turn)
                                sqselected=[]
                                startsq=() 
                                if(ai_turn==False and game.white==False):
                                    game.white=True
                                    ai_turn = False
                    else:
                        mouse_pos = p.mouse.get_pos()
                        if (rect.collidepoint(mouse_pos)):
                            game.reset_game()
                elif(e.type == p.KEYDOWN):
                    if(e.key == p.K_DOWN):
                        game.undo_move(True)
                        if(len(game.move_log)%2!=0):
                            ai_turn = False
                            game.white = False
                        else:
                            game.white = True
                        sqselected=[]
                        startsq=()
        except:
            pass
        display_game(screen,game,sqselected,possibility)
        if(game.game_over()):
            font = p.font.SysFont("Arial", 30)
            text = font.render("Reset Game", True, p.Color("white"))
            rect = text.get_rect(center=(width // 2, height - 50))
            p.draw.rect(screen, p.Color("blue"), rect, border_radius=10)
            screen.blit(text, rect)
        p.display.flip()
        if(not game.game_over() and game.white==False and ai_turn==True):
            print("is thinking .....")
            ai_evaluation = chessegine.find_minimax(game,game.board,False,-100000000,100000000,2)
            ai_move = ai_evaluation[0]
            if(ai_move is None):
                possibility = game.all_valid_moves(False)
                ai_move = possibility[random.randint(0,len(possibility)-1)]
            p.time.delay(900)
            game.move_piece(ai_move,True)
            game.promotion_ia()
            game.white=True
            ai_turn = False
            print("your turn : ")
def display_game(screen , game,sqselected,possibility):
    draw_board(screen)
    highlightSquares(screen,possibility,sqselected)
    highlightChecks(screen,game)
    draw_pieces(screen,game.board)
    if(game.is_checkmate("wK")):
        Drawtext(screen,"Black wins by checkmate")
    elif(game.is_checkmate("bK")):
        Drawtext(screen,"white wins by checkmate")
    elif(game.is_stalemate()):
        Drawtext(screen,"Stalemate")


def promotion_window():
    global promotion_choice
    promotion_choice = None
    window = Tk()
    window.title("Promotion window")
    window.geometry(f"+{500}+{200}")
    pieces = ["wQ", "wR", "wB", "wN"]
    images = {}
    for piece in pieces:
        img = Image.open(f"C:/Users/adamm/Desktop/Chess/images/{piece}.png")
        img = img.resize((40, 40)) 
        images[piece] = ImageTk.PhotoImage(img)
    name_pieces =["Queen","Rook","Bishop","Knight"]
    i=0
    for piece in pieces:
        btn = Button(window, text=name_pieces[i], image=images[piece], compound="right", command=lambda p=piece: clicked(window, p))
        btn.pack()
        i+=1
    window.mainloop()
    return promotion_choice
def clicked (window,piece):
    global promotion_choice
    promotion_choice = piece
    window.destroy()
    
def draw_board(screen):
    k=0
    x=0
    y=0
    for i in range(8):
        for j in range(8):
            if(k%2==0):
                color=p.Color("white")
            else:
                color=p.Color("dark green")
            rectangle1 = p.Rect(x,y,sqsize,sqsize)
            p.draw.rect(screen,color,rectangle1)
            k+=1
            x+=sqsize
        k+=1
        x=0
        y+=sqsize
def draw_pieces(screen,board):
    for i in range(8):
        for j in range(8):
            name_piece = board[i][j]
            if(name_piece!="--"):
                screen.blit(p.image.load("C:/Users/adamm/Desktop/Chess/images/"+ name_piece + ".png"),p.Rect(j*sqsize,i*sqsize,sqsize,sqsize))
def highlightSquares(screen,possibility,sqselected):
    if(len(sqselected)==1):
        r,c = sqselected[0]
        s = p.Surface((sqsize,sqsize))
        s.set_alpha(50)#transparancy
        s.fill(p.Color('yellow'))
        screen.blit(s,(c*sqsize,r*sqsize))
        s.set_alpha(80)
        s.fill(p.Color('blue'))
        if(possibility):
            for pos in possibility:
                screen.blit(s,(pos[1]*sqsize,pos[0]*sqsize))
def highlightChecks(screen,game):
    data = (("wK"),("bK"))
    for d in data:
        if(game.is_check(d)):
            r,c = game.king_position(d[0])
            s = p.Surface((sqsize,sqsize))
            s.set_alpha(90)
            s.fill(p.Color('red'))
            screen.blit(s,(c*sqsize,r*sqsize))
def Drawtext(screen, text):
    font = p.font.SysFont("Helvetica", 50, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textRect = textObject.get_rect()
    textRect.center = (width // 2, height // 2) 
    screen.blit(textObject, textRect)
    textObject = font.render(text, 0, p.Color('Gray'))
    screen.blit(textObject,textRect.move(2,2))   
if (__name__ == "__main__"):
    main()
            
    
        
        