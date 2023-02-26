#classic minesweeper
import random
import pygame
import sys
import time
import tkinter

def show_mine(arr,maze_size):
    for j in range(0,maze_size):
        for i in range(0,maze_size):
            if(arr[i][j]==1):
                print('⬜',end='')
            elif(arr[i][j]==0):
                print('⬛',end='')
        print()
    
def show_prox(arr,maze_size):
    for j in range(0,maze_size):
        for i in range(0,maze_size):
            print(arr[i][j],end='')
        print()

def mineplant(prox,x,y,fieldsize):
    for i in range (-1,2):
        for j in range (-1,2):
            tx=x+i
            ty=y+j
            if(tx<0) or (tx>fieldsize-1) or (ty<0) or (ty>fieldsize-1):
                continue
            prox[tx][ty]+=1
    return prox

def mainmaze(mazesize,count):
    # limit=int(input("Enter border size:"))
    limit=1
    # maze_size=int(input("Enter maze size:"))
    # maze_size=15
    field_size=mazesize
    mine =[[0 for i in range(field_size)]for j in range(field_size)]
    prox =[[0 for i in range(field_size)]for j in range(field_size)]
    flag=0
    x,y=0,0
    check=True
    setval=[]
    end_point=[]
    for i in range(0,field_size):
        setval.append(int(i))
    count
    loop=count
    while(loop>0):
        x=random.choice(setval)
        y=random.choice(setval)
        if(mine[x][y]==0):
            mine[x][y]=1
            prox=mineplant(prox,x,y,field_size)
            loop-=1
            continue
    
    show_mine(mine,field_size)  
    # show_prox(prox,field_size)

    return mine,prox,count



def val_tile(ch,field_size,mine,prox,tx,ty,border,space_count,tilesize,screen):
    if(tx>=field_size or ty>=field_size):
        return space_count,prox
    if(tx<0 or ty<0):
        return space_count,prox
    if(prox[tx][ty]==-1):
        return space_count,prox
    if(mine[tx][ty]>2):
        return space_count,prox
    font=pygame.font.init()
    font=pygame.font.Font('freesansbold.ttf', int(2*tilesize/3)-2)
    if(ch==1):
        text = font.render('1', True, (0,0,0), (120,120,120))
    elif(ch==2):
        text = font.render('2', True, (143, 0, 255), (120,120,120))
    elif(ch==3):
        text = font.render('3', True, (0,0,255), (120,120,120))
    elif(ch==4):
        text = font.render('4', True, (0,255,0), (120,120,120))
    elif(ch==5):
        text = font.render('5', True, (255,255,0), (120,120,120))
    elif(ch==6):
        text = font.render('6', True, (225, 193, 110), (120,120,120))
    elif(ch==7):
        text = font.render('7', True, (255,160,0), (120,120,120))
    elif(ch==8):
        text = font.render('8', True, (255,0,0), (120,120,120))
    textRect=text.get_rect()
    pygame.draw.rect(screen, (120,120,120), pygame.Rect((tx+0.166)*tilesize+border,(ty+0.166)*tilesize+border,2*tilesize/3,2*tilesize/3))  

    textRect.center=(((tx+0.5)*tilesize+border),((ty+0.5)*tilesize+border))
    screen.blit(text,textRect)
    # print("Attempted to print Number tile")
    prox [tx][ty]=-1
    space_count-=1
    return space_count,prox





def zero_tile(mine,prox,field_size,tx,ty,border,space_count,tilesize,screen):
    if(tx>=field_size or ty>=field_size):
        return space_count,prox
    if(tx<0 or ty<0):
        return space_count, prox
    if(prox[tx][ty]==-1):
        return space_count,prox
    if(prox[tx][ty]==0):
        pygame.draw.rect(screen, (120,120,120), pygame.Rect((tx+0.1667)*tilesize+border,(ty+0.1667)*tilesize+border,2*tilesize/3,2*tilesize/3))  
        # print("Attempted to print zero tile")
        space_count-=1
        prox[tx][ty]=-1
        space_count,prox = zero_tile(mine,prox,field_size,tx-1,ty-1,border,space_count,tilesize,screen) 
        space_count,prox = zero_tile(mine,prox,field_size,tx-1,ty,border,space_count,tilesize,screen)
        space_count,prox = zero_tile(mine,prox,field_size,tx-1,ty+1,border,space_count,tilesize,screen)
        space_count,prox = zero_tile(mine,prox,field_size,tx,ty+1,border,space_count,tilesize,screen)
        space_count,prox = zero_tile(mine,prox,field_size,tx,ty-1,border,space_count,tilesize,screen) 
        space_count,prox = zero_tile(mine,prox,field_size,tx+1,ty-1,border,space_count,tilesize,screen)
        space_count,prox = zero_tile(mine,prox,field_size,tx+1,ty,border,space_count,tilesize,screen) 
        space_count,prox = zero_tile(mine,prox,field_size,tx+1,ty+1,border,space_count,tilesize,screen)
    else:
        space_count,prox = val_tile(prox[tx][ty],field_size,mine,prox,tx,ty,border,space_count,tilesize,screen)
    return space_count,prox


    
    

def click(mine,x,y,prox,space_count,tile_size,border,field_size,screen):
        # print("in click")
        tx=int((x-border)/tile_size)
        ty=int((y-border)/tile_size)
        if(tx>=field_size or ty>=field_size):
            
            # print("click condition 1",tx,tile_size,field_size)
            
            return False,space_count,prox
        if(tx<0 or ty<0):
            # print("click condition 2")
            return False,space_count,prox
        if(mine[tx][ty]>2):
            # print("click condition 3")
            return False,space_count,prox
        if(mine[tx][ty]==1):
            scr=tile_size*field_size
            font=pygame.font.init()
            font=pygame.font.Font('freesansbold.ttf', int(scr*0.05))
            text = font.render('You Lost!', True, (255,0,0), (180,180,180))
            textRect=text.get_rect()
            pygame.draw.rect(screen, (180,180,180), pygame.Rect(0,0,scr,scr))
            textRect.center=(scr/2,scr/2)
            screen.blit(text,textRect)
            pygame.display.flip()
            time.sleep(1)
            print("You clicked a mine")

            return True,space_count,prox
            #need to put the retry value here
            pygame.quit()
            quit()
        
        # print("click condition passed")
        if(prox[tx][ty]==0):
            space_count,prox=zero_tile(mine,prox,field_size,tx,ty,border,space_count,tile_size,screen)
        else:
            ch =prox[tx][ty]
            space_count,prox=val_tile(ch,field_size,mine,prox,tx,ty,border,space_count,tile_size,screen)
        return False,space_count,prox

def bordering(screen,sizet,tile_size,scr):
    for i in range (1,sizet):
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(i*tile_size-1,0,2,scr))
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(0,i*tile_size-1,scr,2))
        # print(i,scr)

def make_flag(screen,mine,prox,x,y,tile_size,border,field_size):

    tx=int((x-border)/tile_size)
    ty=int((y-border)/tile_size)
    if(tx>=field_size or ty>=field_size):
        return mine
    if(tx<0 or ty<0):
        return mine
    if(prox[tx][ty]==-1):
        return mine
    if(mine[tx][ty]>2):
        return del_flag(screen,mine,x,y,tile_size,border,field_size)
    mine[tx][ty]+=10
    img = pygame.image.load("flag.png")
    img= pygame.transform.scale(img, (2*tile_size/3,2*tile_size/3))
    
    imgRect=img.get_rect()
    pygame.draw.rect(screen, (120,120,120), pygame.Rect((tx+0.166)*tile_size+border,(ty+0.166)*tile_size+border,2*tile_size/3,2*tile_size/3)) 
    imgRect.center=(((tx+0.5)*tile_size+border),((ty+0.5)*tile_size+border))
    screen.blit(img,imgRect)
    print("flag",tx,ty)
    return mine



def del_flag(screen,mine,x,y,tile_size,border,field_size):
    tx=int((x-border)/tile_size)
    ty=int((y-border)/tile_size)
    if(tx>=field_size or ty>=field_size):
        return mine
    if(tx<0 or ty<0):
        return mine
    if(mine[tx][ty]<2):
        return mine
    mine[tx][ty]-=10
    pygame.draw.rect(screen, (150,150,150), pygame.Rect((tx+0.166)*tile_size+border,(ty+0.166)*tile_size+border,2*tile_size/3,2*tile_size/3)) 
    print("unflag",tx,ty)
    return mine

def the_game(sizet,tile_size,count):
    pygame.init()  
    screen = pygame.display.set_mode((tile_size*sizet,tile_size*sizet))
    # screen = pygame.display.set_mode((tile_size*sizet,tile_size*sizet),pygame.FULLSCREEN)    
    done = True
    x=int(tile_size/2)
    y=int(tile_size/2)
    recwidth=tile_size
    recheight=tile_size
    quit_game=False
    scr=tile_size*sizet
    font=pygame.font.init()
    font=pygame.font.Font('freesansbold.ttf',int(scr*0.05))
    retry_button=0
    while not quit_game:
            
        mine,prox,count=mainmaze(sizet,count)
        time.sleep(0.5)
        border= 0
        done=True
        space_count=sizet*sizet - count
        background=pygame.Surface([tile_size*sizet+(2*border),tile_size*sizet+(2*border)])
        pygame.Surface.fill(background,(150,150,150))

        screen.blit(background,(0,0))

        bordering(screen,sizet,tile_size,scr)

        clock=pygame.time.Clock()
        pygame.display.flip()
        retry_screen=False
        while done:
            if(retry_screen) and retry_button == 0:
                text_retry = font.render('Retry', True, (255,175,0), (25,25,180))
                RetryRect=text_retry.get_rect()
                RetryRect.center=(scr/2,scr/2+100)
                screen.blit(text_retry,RetryRect)
                pygame.display.flip()
                retry_button=1
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    (x,y)=event.pos
                    if(x>=scr-border or y>=scr-border):
                        continue
                    if(x<border or y<border):
                        continue
                    # print("CLICK")
                    if not retry_screen:
                        if(event.button == 1):
                            retry_screen,space_count,prox=click(mine,x,y,prox,space_count,tile_size,border,sizet,screen)
                            # print("1 press")
                            # print("Space=",space_count)
                        # event.button returns 1 for left click and 3 fo right click
                        elif(event.button == 3):
                            mine=make_flag(screen,mine,prox,x,y,tile_size,border,sizet)
                    else:
                        
                        if(event.button==1):
                            if ((x,y)>=RetryRect.topleft ) and ((x,y)<=RetryRect.bottomright):
                                retry_screen=False
                                done=False
                                retry_button=0
            pygame.display.flip()  
            if(space_count==0) and not retry_screen:
                time.sleep(3)
                text = font.render('You Won!', True, (255,0,0), (180,180,180))
                textRect=text.get_rect()
                pygame.draw.rect(screen, (180,180,180), pygame.Rect(0,0,scr,scr))
                textRect.center=(scr/2,scr/2)
                screen.blit(text,textRect)
                pygame.display.flip()
                # time.sleep(3)
                print("Well Done")
                retry_screen=True

                
            clock.tick(60) 
    

val=10
al=""
with open("siz.txt",mode="r") as MyFile:
    for x in MyFile:
        al=al+x
val=int(al)
scrsize=750
count=int(val*1.2)
the_game(val,int(scrsize/(val)),count)
# mainmaze(val)
print("Congrats")
