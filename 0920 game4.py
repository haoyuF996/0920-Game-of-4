def InitialiseBorad(size):
    '''
    initialise the borad with 0s\n
    borad is a dictionary with coordinates as keys\n
    coordinates starts with 0
    '''
    Borad = {}
    for x in range(size[0]):
        for y in range(size[1]):
            Borad[(x,y)] = 0
    return Borad
def DisplyBorad(Borad):
    '''
    Display the borad\n
    Borad: a dictionary with coordinates as keys\n
    0 for empty, 1 for red, 2 for blue\n
    '''
    global screen
    color = (128,138,135)
    size,pos = (SIZE[0]*50+50, SIZE[1]*50+50),(0,100)
    pygame.draw.rect(screen, color, Rect(pos, size))
    pygame.draw.rect(screen, (128,138,135), Rect(pos, size),3)
    for point in Borad:
        c = (255,255,224)
        if Borad[point]==1:
            c = (255,127,0)
        elif Borad[point]==2:
            c = (0,0,205)
        elif Borad[point]==-1:
            c = (255,151,0)
        elif Borad[point]==-2:
            c = (0,0,230)
        p = ((point[0]+1)*50,(point[1]+1)*50+100)
        pygame.draw.circle(screen, c, p, 20)
    return screen
def GetDiagonal(Coordinate,Borad,Direct):
    '''
    Return the values of the diagoal from\n
    upleft to bottomright if Direct is l\n
    upright to bottomleft if Direct is r\n
    with the coordinate as the center and a total lenth of 7\n
    as a list
    '''
    x,y = Coordinate[0],Coordinate[1]
    Xs,Ys = [i for i in range(x-3,x+4)],[i for i in range(y-3,y+4)]
    if Direct == 'l':
        Xs.reverse()
    List = []
    for i in range(7):
        if (Xs[i],Ys[i]) in Borad:
            List.append(Borad[(Xs[i],Ys[i])])
    return List
def GetLine(Coordinate,Borad,Direct):
    '''
    Return the values of the line\n
    from left to right if Direct is x\n
    from top to bottom if Direct is y\n
    with the coordinate as the center and a total lenth of 7\n
    as a list
    '''
    x,y = Coordinate[0],Coordinate[1]
    Xs,Ys = [i for i in range(x-3,x+4)],[i for i in range(y-3,y+4)]
    List = []
    if Direct == 'x':
        for i in range(7):
            if (Xs[i],y) in Borad:
                List.append(Borad[(Xs[i],y)])
    elif Direct == 'y':
        for i in range(7):
            if (x,Ys[i]) in Borad:
                List.append(Borad[(x,Ys[i])])
    return List
def CheckWinL(List):
    '''
    Check the values in List\n
    return R for red win, B for blue win, False for not win
    '''
    countr,countb = [0],[0]
    for i in List:
        if i == 1:
            countr.append(countr[-1]+1)
            countb.append(0)
        elif i == 2:
            countb.append(countb[-1]+1)
            countr.append(0)
        else:
            countb.append(0)
            countr.append(0)
    countr.sort()
    countb.sort()
    if countb[-1]>=4:
        return 'B'
    elif countr[-1]>=4:
        return 'R'
    else:
        return False
def CheckWin(Borad,loc):
    '''
    Check the values in Borad around loc\n
    return R for red win, B for blue win, D for Draw,\n
    False for not win
    '''
    l,r = GetDiagonal(loc,Borad,'l'),GetDiagonal(loc,Borad,'r')
    x,y = GetLine(loc,Borad,'x'),GetLine(loc,Borad,'y')
    win_list = [CheckWinL(l),CheckWinL(r),CheckWinL(x),CheckWinL(y)]
    Draw = True
    for pos in Borad:
        if Borad[pos]==0:
            Draw = False
    if 'B' in win_list:
        return 'B'
    elif 'R' in win_list:
        return 'R'
    elif Draw:
        return 'D'
    else:
        return False
def GetMouse(Borad):
    '''
    return position of mouse on Borad\n
    if not on Borad, return False
    '''
    x, y = pygame.mouse.get_pos()
    #获得鼠标位置
    for pos in Borad:
        if pos[1]==0:
            distance = (x-(pos[0]+1)*50)**2 + (y-(pos[1]+3)*50)**2
            if distance<=400.0:
                return pos
    return False
def ShowWin(winner):
    '''
    Show who wins
    '''
    global screen,player,Won
    font = pygame.font.SysFont('impact',68)
    if winner == 'D':
        surface = font.render('Draw',True,(255,255,224))
    else:
        surface = font.render('WIN',True,winner)
    size = surface.get_width(),surface.get_height()
    pygame.draw.rect(screen, (0,0,0), Rect((SIZE[0]*15,10), size))
    screen.blit(surface,(SIZE[0]*15,10))
    player = False
    Won = True
def ShoeState():
    '''
    Show the state of movement
    '''
    global screen,player
    font = pygame.font.SysFont('impact',50)
    if player == 1:
        k = font.render('Move',True,(255,165,0))
    elif player == 2:
        k = font.render('Move',True,(72,118,255))
    else:
        k = font.render('Wait',True,(255,255,224))
    size = k.get_width(),k.get_height()
    pygame.draw.rect(screen, (0,0,0), Rect((SIZE[0]*15,30), size))
    screen.blit(k,(SIZE[0]*15,30))
def Init():
    '''
    Initialize the borad, the screen and some values
    '''
    global player,Anime,Borad,screen,Borad,loc,SIZE
    loc = False
    Borad = InitialiseBorad(SIZE)
    screen = pygame.display.set_mode((SIZE[0]*50+50, SIZE[1]*50+150), 0, 32)
    screen.fill((0,0,0))
    player = 0
    Anime = 0
def Start():
    '''
    For the Start bottom
    '''
    global Won
    global OnS
    global screen
    pygame.draw.rect(screen, (0,0,0), Rect((0,0),(450,100)))
    if Won:
        x, y = pygame.mouse.get_pos()
        font = pygame.font.Font('American Typewriter Medium BT.ttf', 20)
        k = font.render('START',True,(0,0,0))
        sx,sy = k.get_width(),k.get_height()
        size = (sx+10,sy)
        xGap,yGap = 10,20
        pos = (SIZE[0]*50+40-sx-xGap,yGap)
        if 0<=x-(SIZE[0]*50+40-sx-xGap)<=sx and 0<=y-yGap<=sy:
            color = (238,238,0)
            OnS = True
        else:
            color = (255,255,0)
            OnS = False
        pygame.draw.rect(screen, color, Rect(pos, size))
        pygame.draw.rect(screen, (255,255,224), Rect(pos, size),2)
        screen.blit(k,(SIZE[0]*50+45-sx-xGap,yGap))
class Drop():
    def __init__(self,start,pos,t0,play):
        self.start = start
        self.pos = pos
        self.t0 = t0
        self.play = play
    def down(self):
        global Borad
        global player,loc
        if time.time()-self.t0 >= 0.2:
            #每0.2s进行一次下落判定
            lower_pos = (self.start,self.pos+1)
            if lower_pos in Borad and Borad[lower_pos]<=0:
                #可以继续下落
                Borad[(self.start,self.pos)] = 0
                #清空当前位置
                self.pos+=1
                Borad[(self.start,self.pos)] = self.play
                #进入下方位置
                self.t0 = time.time()
            elif not lower_pos in Borad or Borad[lower_pos]>0:
                #无法继续下落则结束下落
                Borad[(self.start,self.pos)] = self.play
                player = self.play*(self.play-2)**2+1
                loc = (self.start,self.pos)
class FPS():
    def __init__(self,t0,count,fps):
        self.t0 = t0
        self.count = count
        self.fps = fps
    def display(self,dis):
        global screen
        font = pygame.font.Font('American Typewriter Medium BT.ttf', 10)
        surface = font.render(f'FPS:{self.fps}',True,(255,255,255))
        size = surface.get_width(),surface.get_height()
        t = time.time()
        pygame.draw.rect(screen, (0,0,0), Rect((0,0), size))
        self.count+=1
        #计数器每次加一，用于计算两次更新之间的帧数
        if dis and t-self.t0>=0.1:
            #每0.1s更新一次fps
            self.fps = int(self.count/(t-self.t0))
            self.t0 = time.time()
            self.count = 0
            screen.blit(surface,(0,0))
        elif dis and t-self.t0<0.1:
            #不更新时仍然显示
            screen.blit(surface,(0,0))
import pygame
from pygame.locals import *
from sys import exit
import time
import random
SIZE = eval(input('Borad size:'))
Init()
M=(0,0)
Won = True
pygame.init()
pygame.display.set_caption('Game of 4')
fps = FPS(time.time(),time.time(),0)
fps_display = [False,True] 
while True:
#游戏主循环
    Start()
    if player and M and Borad[M]<=0:
        Borad[M] = 0
    M = GetMouse(Borad)
    #获得鼠标位置
    if player and M and Borad[M]<=0:
        Borad[M] = -player
    #在鼠标所在位置展示棋子
    for event in pygame.event.get():
        if event.type == QUIT:
            #接收到退出事件后退出程序
            exit()
        if event.type == MOUSEBUTTONDOWN and OnS and Won:
            Init()
            player = random.randint(1,2)
            Won = False
            #点击Start后初始化
        if event.type == MOUSEBUTTONDOWN and M and Borad[M]<=0 and player:
            Anime = Drop(M[0],0,time.time(),player)
            player = False
            #点击空位后开始下落棋子
        if event.type == KEYDOWN and event.key == K_DOWN:
            fps_display.reverse()
            #点下键后显示/隐藏fps
    if not player and Anime:
        Anime.down()
        #演示下落动画
    ShoeState()#展示回合状态
    screen = DisplyBorad(Borad)
    if player and loc:
        #胜利判定
        a = CheckWin(Borad,loc)
        if a=='R':
            ShowWin((255,165,0))
        elif a=='B':
            ShowWin((72,118,255))
        elif a=='D':
            ShowWin('D')
    fps.display(fps_display[0])
    pygame.display.update()
    #刷新一下画面