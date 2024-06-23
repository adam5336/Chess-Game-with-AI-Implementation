class boardState:
    def __init__(self):
        self.board=[["bR","bN","bB","bQ","bK","bB","bN","bR"],
                    ["bp","bp","bp","bp","bp","bp","bp","bp"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["wp","wp","wp","wp","wp","wp","wp","wp"],
                    ["wR","wN","wB","wQ","wK","wB","wN","wR"]
                    ]
        self.move_log = []
        self.white = True
        self.valid_castling=[[0,0,0],[0,4,0],[0,7,0],[7,0,0],[7,4,0],[7,7,0]]
        self.valid_castling_strings=["0400","0407","7470","7477"]
        self.undo_type = []
    def move_piece(self,move,is_virtual):
        if(move is not None):
            enpassant = self.list_enpassant(move.startrow,move.startcol,move.piece_moved[0])
            piece_name = self.board[move.startrow][move.startcol]
            srow=move.startrow
            scol=move.startcol
            erow=move.endrow
            ecol=move.endcol
            if(enpassant and ((move.endrow,move.endcol) in enpassant)):
                move = self.move_piece_enpassant(move)
                self.undo_type.append("enpassant")
            elif(self.is_castling(srow,scol,erow,ecol,piece_name)==True or (move in self.is_castling_ai() and self.is_castling_move_ai(move))):
                self.move_piece_castling(move)
                self.undo_type.append("castling")
            else:
                self.board[move.endrow][move.endcol] = self.board[move.startrow][move.startcol]
                self.board[move.startrow][move.startcol] = "--"
                self.undo_type.append("normal")
            self.move_log.append(move) 
            if(is_virtual==True):
                for valid in self.valid_castling:
                    if(move.startrow==valid[0] and move.startcol==valid[1]):
                        valid[2]+=1
    def move_piece_castling(self,move):
        castle = (("0400",(0,2),(0,3)),
                  ("0407",(0,6),(0,5)),
                  ("7470",(7,2),(7,3)),
                  ("7477",(7,6),(7,5)))
        pattern = str(move.startrow)+str(move.startcol)+str(move.endrow)+str(move.endcol)
        for d in castle:
            if(d[0]==pattern):
                self.board[d[1][0]][d[1][1]] = self.board[move.startrow][move.startcol]
                self.board[d[2][0]][d[2][1]] = self.board[move.endrow][move.endcol]
                self.board[move.startrow][move.startcol] = "--"
                self.board[move.endrow][move.endcol] = "--"
                
    def is_castling(self,srow,scol,erow,ecol,name_piece):
        if(self.for_castling(srow,scol,erow,ecol)==False):
            return False
        pattern = str(srow)+str(scol)+str(erow)+str(ecol)
        if(pattern not in self.valid_castling_strings):
            return False
        invalid = (("0400",(0,1),(0,2),(0,3),(0,4)),
                   ("0407",(0,4),(0,5),(0,6)),
                   ("7470",(7,1),(7,2),(7,3),(7,4)),
                   ("7477",(7,4),(7,5),(7,6)))
        possibility = []
        for i in range(8):
            for j in range(8):
                if(self.board[i][j][0]!=name_piece[0] and self.board[i][j]!="--"):
                    possibility+=self.allpossiblemoves(i,j)
        for castle in (invalid):
            if(castle[0]==pattern):
                for pos in castle [1:]:
                    if(pos in possibility):
                        return False
        for d in self.valid_castling:
            if((d[0]==srow and d[1]==scol and d[2]!=0)or(d[0]==erow and d[1]==ecol and d[2]!=0)):
                return False
        return True
    def is_castling_move_ai(self,move):
        pos1 = (move.startrow,move.startcol)
        pos2 = (move.endrow,move.endcol)
        if(pos1==(0,4) and(pos2==(0,0) or pos2==(0,7)) and self.white==False):
            return True
        return False
    def is_castling_ai(self):
        invalid = (("0400",(0,1),(0,2),(0,3),(0,4)),("0407",(0,4),(0,5),(0,6)))
        possibility1=[]
        possibility = []
        compt = 0
        for i in range(8):
            for j in range(8):
                if(self.board[i][j][0]!='b' and self.board[i][j]!="--"):
                    possibility1+=self.allpossiblemoves(i,j)
        for castle in (invalid):
            test1=test2=test3=True
            if(self.for_castling_ai(castle[0])==False):
                test1=False
            for pos in castle [1:]:
                if(pos in possibility1):
                    test2=False
            for d in self.valid_castling:
                if((d[0]==int(castle[0][0]) and d[1]==int(castle[0][1]) and d[2]!=0)or(d[0]==int(castle[0][2]) and d[1]==int(castle[0][3]) and d[2]!=0)):
                    test3=False
            if(test1 and test2 and test3):
                if(compt==0):
                    nmove = move((0,4),(0,0),self.board)
                    possibility.append(nmove)
                elif(compt==1):
                    nmove = move((0,4),(0,7),self.board)
                    possibility.append(nmove)
            compt+=1
        return possibility
    def for_castling_ai(self,pattern):
        max1 = max(int(pattern[1]),int(pattern[-1]))
        min1 = min(int(pattern[1]),int(pattern[-1]))
        for i in range(min1+1,max1):
            if(self.board[0][i]!="--"):
                return False
        return True
    def for_castling(self,srow,scol,erow,ecol):
        if(self.board[srow][scol][1]!='K' or self.board[erow][ecol][1]!='R' or srow!=erow):
            return False
        min1 = min(scol,ecol)
        max1 = max(scol,ecol)
        for i in range(min1+1,max1):
            if(self.board[srow][i]!="--"):
                return False    
        return True
    def move_piece_enpassant(self,move):
        name_piece = self.board[move.startrow][move.startcol]
        self.board[move.endrow][move.endcol] = self.board[move.startrow][move.startcol]
        self.board[move.startrow][move.startcol] = "--"
        if(name_piece[0]=='w'):
            move.piece_captured = self.board[move.endrow+1][move.endcol]
            self.board[move.endrow+1][move.endcol]="--"
        else:
            move.piece_captured = self.board[move.endrow-1][move.endcol]
            self.board[move.endrow-1][move.endcol]="--"
        return move
        
    def undo_move(self,is_virtual):
        if(len(self.move_log)!=0):
            move = self.move_log[-1]
            self.move_log.pop()
            if(self.undo_type[-1]=="normal"):
                self.board[move.endrow][move.endcol] = move.piece_captured
                self.board[move.startrow][move.startcol] = move.piece_moved
                if(is_virtual==True):
                    for d in self.valid_castling:
                        if(d[0]==move.startrow and d[1]==move.startcol):
                            d[2]-=1
            elif(self.undo_type[-1]=="castling"):
                self.board[move.endrow][move.endcol] = move.piece_captured
                self.board[move.startrow][move.startcol] = move.piece_moved
                pattern = str(move.startrow)+str(move.startcol)+str(move.endrow)+str(move.endcol)
                data = (("0400",(0,1),(0,2),(0,3)),("0407",(0,5),(0,6)),("7470",(7,1),(7,2),(7,3)),("7477",(7,5),(7,6)))
                for d in data:
                    if(d[0]==pattern):
                        for pos in d[1:]:
                            self.board[pos[0]][pos[1]] = "--"
                if(is_virtual==True):
                    for d in self.valid_castling:
                        if((pattern[0:2]==str(d[0])+str(d[1])and d[2]>0) or (pattern[2:4]==str(d[0])+str(d[1])and d[2]>0)):
                            d[2]-=1
            else:
                if(self.board[move.startcol][move.startrow][0]=='w'):
                    self.board[move.endrow-1][move.endcol] = move.piece_captured
                    self.board[move.startrow][move.startcol] = move.piece_moved
                    self.board[move.endrow][move.endcol]="--"
                else:
                    self.board[move.endrow+1][move.endcol] = move.piece_captured
                    self.board[move.startrow][move.startcol] = move.piece_moved
                    self.board[move.endrow][move.endcol]="--"
                    
            self.undo_type.pop()
            self.white = not self.white
    def allpossiblemoves(self,row,col):
        possible_moves=[]
        if(self.board[row][col]!="--"):
            name_piece = self.board[row][col]
            if name_piece[1] == "N":
                possible_moves = self.get_knightmoves(name_piece,row,col)
            elif name_piece[1] == "p":
                possible_moves = self.get_pawnmoves(row,col,name_piece)
            elif name_piece[1] == "B":
                possible_moves = self.get_bishopmoves(name_piece,row,col)
            elif name_piece[1] == "R":
                possible_moves = self.get_rookmoves(name_piece,row,col)
            elif name_piece[1] == "Q":
                possible_moves = self.get_queenmoves(name_piece,row,col)
            elif name_piece[1] == "K":
                possible_moves = self.get_kingmoves(name_piece,row,col)
        return possible_moves
    
    def get_pawnmoves(self,row,col,name_piece):
        possible_moves=[]
        data = (("w",6,-2,-1),("b",1,2,1))
        for d in data:
            if(name_piece[0]==d[0]):
                if(row==d[1]):
                    if(self.board[row+d[2]][col]=="--" and self.board[row+d[3]][col]=="--"):
                        pos = (row+d[2],col)
                        possible_moves.append(pos)
                if(col<7 and (row<7 and row>0) and self.board[row+d[3]][col+1]!="--" and self.board[row+d[3]][col+1][0]!=name_piece[0]):
                    pos = (row+d[3],col+1)
                    possible_moves.append(pos)
                if(col>0 and (row<7 and row>0) and self.board[row+d[3]][col-1]!="--" and self.board[row+d[3]][col-1][0]!=name_piece[0]):
                    pos = (row+d[3],col-1)
                    possible_moves.append(pos)
                if((row<7 and row>0) and self.board[row+d[3]][col]=="--"):
                    pos = (row+d[3],col)
                    possible_moves.append(pos)
        enpassant = self.list_enpassant(row,col,name_piece[0])
        if(enpassant):
            possible_moves+=enpassant
        return possible_moves         
    def get_bishopmoves(self,name_piece,row,col):
        possible_moves = []
        directions = ((-1,-1),(-1,1),(1,1),(1,-1))
        for d in (directions):
            i=row
            j=col
            while((i<=7 and i>=0) and (j<=7 and j>=0)):
                if(i!=row and j!=col):
                    if(self.board[i][j]!="--"):
                        if(self.board[i][j][0]!=name_piece[0]):
                            pos = (i,j)
                            possible_moves.append(pos)
                            break
                        else:
                            break
                    else:
                        pos = (i,j)
                        possible_moves.append(pos)
                i+=d[0]
                j+=d[1]
        return possible_moves
    def get_rookmoves(self,name_piece,row,col):
        possible_moves = []
        direction = ((-1,0),(1,0),(0,1),(0,-1))
        for d in direction:
            i=row
            j=col
            while((i>=0 and i<=7) and (j>=0 and j<=7)):
                if(i!=row or j!=col):
                    if(self.board[i][j]!="--"):
                        if(self.board[i][j][0]!=name_piece[0]):
                            pos = (i,j)
                            possible_moves.append(pos)
                            break
                        else:
                            break
                    else:
                        pos = (i,j)
                        possible_moves.append(pos)
                i+=d[0]
                j+=d[1]
        return possible_moves
    def get_queenmoves(self,name_piece,row,col):
        possible_move1 = self.get_bishopmoves(name_piece,row,col)
        possible_move2 = self.get_rookmoves(name_piece,row,col)
        return possible_move1 + possible_move2
    def get_kingmoves(self,name_piece,row,col):
        possible_moves = []
        direction = ((-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1))
        for d in direction:
            i=row+d[0]
            j=col+d[1]
            if((i>=0 and i<=7) and (j<=7 and j>=0)):
                if(self.board[i][j]!="--"):
                    if(self.board[i][j][0]!=name_piece[0]):
                        pos = (i,j)
                        possible_moves.append(pos)
                else:
                    pos = (i,j)
                    possible_moves.append(pos)
        return possible_moves
    def get_knightmoves(self,name_piece,row,col):
        possible_moves = []
        direction = ((-2,-1),(-1,-2),(1,-2),(2,-1),(2,1),(1,2),(-1,2),(-2,1))
        for d in direction:
            i=row+d[0]
            j=col+d[1]
            if((i<=7 and i>=0) and (j<=7 and j>=0)):
                if(self.board[i][j]!="--"):
                    if(self.board[i][j][0]!=name_piece[0]):
                        pos=(i,j)
                        possible_moves.append(pos)
                else:
                    pos = (i,j)
                    possible_moves.append(pos)
                
        return possible_moves
    def is_check(self,name_piece):
        pos = self.king_position(name_piece[0])
        possibility=[]
        for i in range(8):
            for j in range(8):
                if(self.board[i][j][0]!=name_piece[0] and self.board[i][j][1]!='-'):
                    possibility+=self.allpossiblemoves(i,j)
        if(pos in possibility):
            return True
        return False
    def list_enpassant(self,row,col,name_piece):
        possible_moves=[]
        if(self.board[row][col][1]=='p' and len(self.move_log)>1):
            nmove = self.move_log[len(self.move_log)-1]
            pos1 = (nmove.startrow,nmove.startcol)
            pos2 = (nmove.endrow,nmove.endcol)
            data = (('w',1,3,-1),('b',6,4,1))
            for d in data:
                if(name_piece==d[0] and row==d[2]):
                    if(col<7 and col>=0):
                        if(pos1==(d[1],col+1) and pos2==(row,col+1)):
                            pos = (row+d[3],col+1)
                            possible_moves.append(pos)
                    if(col>0 and col <=7):
                        if(pos1==(d[1],col-1) and pos2==(row,col-1)):
                            pos = (row+d[3],col-1)
                            possible_moves.append(pos)
        return possible_moves   
    def is_checkmate(self,d):
        possibility = []
        if(self.is_check(d)):
            for i in range(8):
                for j in range(8):
                    if (self.board[i][j][0] == d[0]):
                        possibility1 = self.allpossiblemoves(i, j)
                        for valid in possibility1:
                            nmove = move((i,j),valid,self.board)
                            self.move_piece(nmove,False)
                            if(self.is_check(d)==False):
                                possibility.append(valid)
                            self.undo_move(False)               
            if (not possibility and self.is_check(d)):
                return True
        return False

    def is_stalemate(self):
        data = ["wK","bK"]
        for d in data:
            if(self.is_check(d)==False):
                possibility=[]
                for i in range(8):
                    for j in range(8):
                        if(self.board[i][j][0]==d[0] and self.board[i][j]!=d):
                            possibility += self.allpossiblemoves(i,j)
                if(not possibility and self.is_kingvalid(d)==False):
                    return True
        return False
    def game_over(self):
        if(self.is_checkmate("wK") or self.is_checkmate("bK") or self.is_stalemate()):
            return True
        return False
    def is_kingvalid(self,name_piece):
        pos = self.king_position(name_piece[0])
        possibility =self.allpossiblemoves(pos[0],pos[1])
        king_unvalid_moves = 0
        for valid in possibility:
            nmove = move(pos,valid,self.board)
            self.move_piece(nmove,False)
            if(self.is_check(name_piece)==True):
                king_unvalid_moves+=1
            self.undo_move(False)
        if(king_unvalid_moves == len(possibility)):
            return False
        else:
            return True
    def king_position(self,name):
        for i in range(8):
            for j in range(8):
                if(self.board[i][j]==name+'K'):
                    return i,j
        return -1,-1
    def is_promotion(self,move):
        if((move.piece_moved=="wp" and move.endrow==0)):
            return True
        return False
    def promoting(self,move,name_piece):
        self.board[move.endrow][move.endcol] = name_piece
    def out_check_possibility(self,row,col,name_piece,possibility1):
        possibility = []
        for pos in possibility1:
            nmove = move((row,col),pos,self.board)
            self.move_piece(nmove,False)
            if(self.is_check(name_piece)==False):
                possibility.append(pos)
            self.undo_move(False)
        return possibility
    def all_valid_moves(self,turn):
        possibility = []
        data =(('w',True),('b',False))
        for d in data:
            if(d[1]==turn):
                for i in range(8):
                    for j in range(8):
                        if(self.board[i][j][0]==d[0]):
                            possibility1 = self.allpossiblemoves(i,j)
                            possibility1 = self.out_check_possibility(i,j,self.board[i][j],possibility1)
                            for pos in possibility1:
                                nmove = move((i,j),pos,self.board)
                                possibility.append(nmove)
        if(turn==False):
            possibility1=self.is_castling_ai()
            possibility+=possibility1
        return possibility 
    def reset_game(self):
        self.board = [["bR","bN","bB","bQ","bK","bB","bN","bR"],
                      ["bp","bp","bp","bp","bp","bp","bp","bp"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["wp","wp","wp","wp","wp","wp","wp","wp"],
                      ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.move_log = []
        self.undo_type = []
        self.white = True
        self.valid_castling = [[0,0,0],[0,4,0],[0,7,0],[7,0,0],[7,4,0],[7,7,0]]
        self.valid_castling_strings = ["0400","0407","7470","7477"]     
    def promotion_ia(self):
        for i in range(8):
            if(self.board[7][i]=="bp"):
                self.board[7][i] = "bQ"   
                       
            
        
        
class move():
    def __init__(self,startsq,endsq,board):
        self.startrow = startsq[0]
        self.startcol = startsq[1]
        self.endrow = endsq[0]
        self.endcol = endsq[1]
        self.piece_moved = board[self.startrow][self.startcol]
        self.piece_captured = board[self.endrow][self.endcol]
