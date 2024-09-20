import pygame
import random
from pygame import mixer
import time
#INITIALISING PYGAME

pygame.init()

start_time = time.time()
#SCREEN SIZE
height = 924
width = 600

#PLAYER MOVEMENT LIMIT
height_limit = 750
upper_width_limit = 450
lower_width_limit = 40

#LIMITS FOR PLAYER MOVEMENT
playerX_min_limit = 100
playerX_max_limit = 250



#CREATING THE SCREEN
screen = pygame.display.set_mode((height,width))


#WINDOW IMAGE AND TITLE
pygame.display.set_caption("PvZ")
icon = pygame.image.load('pvz.png')
pygame.display.set_icon(icon)


def reset_game():
      global playerX,playerY, playerYchange, playerxchange
      global bulletx,bullety, bullet_state
      global enemyX, enemyY, enemyxchange,enemyY
      global score_value, start_time
      
      playerX = 10
      playerY = lower_width_limit
      playerYchange = 0
      playerxchange = 0
      bulletx = playerX
      bullety = playerY
      bulletxchange = 5
      bullet_state = "ready" 
      score_value = 0   
      
      
      for i in range(num_of_enemies):
            enemyX[i] = 900
            enemyY[i] = random.randint(0, 439)
            enemyxchange[i] = -1
            enemyYchange[i] = 0
      
      

#PLAYER IMAGE AND POSITION
playerimg = pygame.image.load('OIP.png')
playerX = 10
playerY = lower_width_limit
playerYchange = 0
playerxchange = 0




#bullet
bulletimg = pygame.image.load('bullet.png')
bulletx = lower_width_limit
bullety = 0
bulletxchange = 5
bullet_state = "ready"  #ready = cant see the bullet on the screen
                        #fire = the bullet is currently moving

#Gamer over and Background
background = pygame.image.load('back1.jpg')

#BACKGROUND MUSIC
bgmusic = mixer.music.load("mainmusic2.mp3")
mixer.music.play(-1)
#ENEMY IMAGES
enemy_images = [pygame.image.load('zomb.png'),pygame.image.load('zomb1.png'),pygame.image.load('zomb2.png'), pygame.image.load('zomb3.png'), pygame.image.load('zomb4.png')]

#ENEMY 

enemyimg =[]
enemyX = []
enemyY = []
enemyxchange =[]
enemyYchange = []
num_of_enemies = len(enemy_images)
for i in range(num_of_enemies):
      enemyimg.append(enemy_images[i])
      enemyX.append(900)
      enemyY.append(random.randint(0,439))
      enemyxchange.append(-1)
      enemyYchange.append(0)



#DEFINING ELEMENTS

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textx = 10
texty = 10


#GAME OVER
overx = 200
overy = 100
 
def game_over(x,y):
      mixer.music.pause()
      gameoverimg = pygame.image.load('gameover.png') 
      screen.blit(gameoverimg, (overx,overy))
      over = mixer.Sound('lose.mp3')
      over.play()
      pygame.display.update()

      font= pygame.font.Font('freesansbold.ttf', 32)
      replay_text = font.render("Press R to replay or press Q to quit", True, (255,255,224))
      screen.blit(replay_text, (x-40, y+120))
      font = pygame.font.Font('freesansbold.ttf', 32)
      continue_text = font.render("Your score was :"+ str(score_value), True,(255,255,204) )
      screen.blit(continue_text, (x,y+420))
      pygame.display.update()
      
 #MILESTONES AND THEIR MUSIC     

      
def show_score(x,y):
      score = font.render("Score :" + str(score_value), True,(255,255,224) )
      screen.blit(score, (x,y))



def player(x,y):
       screen.blit(playerimg, (x, y))


def enemy(x,y,i):
       screen.blit(enemyimg[i], (x, y))

def fire_bullet(x,y):
      global bullet_state
      bullet_state = "fire"
      screen.blit(bulletimg, (x+50, y+10))
          
def iscollision(enemy_rect, bullet_rect):
      return enemy_rect.colliderect(bullet_rect)


#GAME LOOP 
running = True   
game_active = True

while running:
 elapsed_time = time.time() - start_time
 
 if game_active:
    #SCREEN COLOR
    screen.fill((245, 245, 220)) 
    screen.blit(background, (0,0))



    #HANDLE EVENTS  

    for  event in pygame.event.get():


      #GAME QUITS WHEN X IS CLICKED     
    
        if event.type == pygame.QUIT:
                    running = False 

      #IF KEYSTROKE IS PRESSED CHECK BETTER IT IS UP OR DOWN
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                  playerYchange +=2
            if event.key == pygame.K_UP: 
                  playerYchange -=2

            if event.key == pygame.K_RIGHT:
                  playerxchange += 2

            if event.key == pygame.K_LEFT:
                  playerxchange -= 2

            if event.key == pygame.K_SPACE:
                  if bullet_state == 'ready':
                        bulletx = playerX
                        bullety = playerY
                        fire_bullet(bulletx,bullety )      
                  gunshot = mixer.Sound("gunshot.mp3")
                  gunshot.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                  playerYchange = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                   playerxchange = 0  


               


    #PLAYER POSITION
    playerY += playerYchange
    playerX += playerxchange


    #GAME TRANSPORTS THE PLAYER BACK TO THE LIMITS
    if playerY < lower_width_limit:
          playerY = lower_width_limit

    elif playerY > upper_width_limit:
            playerY = upper_width_limit


    if playerX < playerX_min_limit:
          playerX = playerX_min_limit

    elif playerX > playerX_max_limit:
          playerX = playerX_max_limit

          
    #ENEMY POSITION CHANGE
    for i in range (num_of_enemies):
      enemy_speed = -1 - (elapsed_time//10) * 0.5
      enemyxchange[i] = enemy_speed 
    
      #GAME OVER  
      if enemyX[i] <= 10:
            for j in range(num_of_enemies):
                  enemyX[j] = 0
            game_over(overx,overy)
            game_active=False
            break   
      
      
      
      #AREA LIMIT FOR THE ENEMIES MOVEMENT

      if enemyY[i] <= 20 :  
            enemyYchange[i] *= -1
            enemyX[i] += enemyxchange[i]
      elif enemyY[i] >= 450:
            enemyYchange[i] *= -1
            enemyX[i] += enemyxchange[i]
          
          
      
      enemyX[i] += enemyxchange[i]      
      
       
      #CREATING RECTANGLES
      enemy_rect = pygame.Rect(enemyX[i], enemyY[i], enemyimg[i].get_width(), enemyimg[i].get_height())
      bullet_rect = pygame.Rect(bulletx, bullety, bulletimg.get_width(), bulletimg.get_height())        
      #Collision
      if iscollision(enemy_rect, bullet_rect):
            bulletx = lower_width_limit
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = 900
            enemyY[i] = random.randint(100, 440)
            point = mixer.Sound("point.mp3")
            point.play()
            

      #ENEMY IS DRAWN  
      for i in range (num_of_enemies):    
            enemy(enemyX[i],enemyY[i], i)     
      
      #movement of bullet
      if bulletx > 730:
            bulletx = lower_width_limit
            bullet_state = "ready"
                  
      if bullet_state == "fire":
            fire_bullet(bulletx,bullety)
            bulletx += bulletxchange
            
      #MUSIC ON SCORE 50  
      milestones = (50,100,200,300) 
      
      music50_played = False
      if score_value in milestones and not music50_played: 
            music50 = mixer.Sound('50.mp3') 
            mixer.music.pause()
            music50.play()
            mixer.music.unpause()
            music50_played = True
            
      if score_value not in milestones:      
            music50_played = False
      player(playerX,playerY)
      show_score(textx,texty)
      pygame.display.update()
      
            
 else: 
      for event in pygame.event.get():
             if event.type == pygame.QUIT:
                        running = False
             elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                              reset_game()
                              game_active = True
                              running = True
                              mixer.music.play(-1)
                              
                                    
                        elif event.key == pygame.K_q:
                              running = False
                  
      #UPDATES THE GAME SCREEN
    
      pygame.display.update()            
                                  
                                  
pygame.QUIT()


