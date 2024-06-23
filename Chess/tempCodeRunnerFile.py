def draw_pieces(screen,board):
    for i in range(8):
        for j in range(8):
            name_piece = board[i][j]
            if(name_piece!="--"):
                screen.blit(p.image.load("images/"+ name_piece + ".png"),p.Rect(j*sqsize,i*sqsize,sqsize,sqsize))