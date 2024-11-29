import pygame
import time
import random
pygame.font.init() #for rendering text

WIDTH,HEIGHT = 1000,800 #You can change based on your window
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) 

#the actual headding which you want to display
pygame.display.set_caption("Space Dodge") 

# setting our baground image to bg
# to fit to our screen we use scale function
BG =pygame.transform.scale( pygame.image.load("bg.jpg"),(WIDTH,HEIGHT))

# player
PLAYER_WIDTH=40
PLAYER_HEIGHT=60

PLAYER_VEL = 5 #move 5px  whn clicked any key
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3




FONT  = pygame.font.SysFont("comicsans",30) #for rendering text (name,size)

BUTTON_FONT = pygame.font.SysFont("comicsans", 40) #for restart button

# Global variable to track high score
high_score = 0

# to put in on screen
def draw(player, elapsed_time, stars, current_score, best_score):
    
    WIN.blit(BG,(0,0))#blit is a inbuilt func which is used to extract
    
    time_text = FONT.render(f"Time : {round(elapsed_time)}s",1,"white") #we are rounding of the time and setting the colour
    
    WIN.blit(time_text, (10, 10)) #to render on the screen
    
    
    # Display current and high score
    current_score_text = FONT.render(f"Score: {current_score}", 1, "white")
    high_score_text = FONT.render(f"High Score: {best_score}", 1, "white")
    
    WIN.blit(current_score_text, (WIDTH - 200, 10))
    WIN.blit(high_score_text, (WIDTH - 200, 50))
    
    # you are drawing the player on the [window, red colour, player with his height and width]
    pygame.draw.rect(WIN,"red",player)
    
    for star in stars : 
        pygame.draw.rect(WIN,"white",star)
    
    pygame.display.update()
    
    
    
#adding a restart func
def draw_restart_button():
    restart_text = BUTTON_FONT.render("Restart", 1, "white")
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(WIN, (0, 128, 0), button_rect)
    WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))
    pygame.display.update()
    return button_rect 

# to make sure that that window stays until you exit it , you can try with a for loop
def main():
    
    global high_score  # Access the global high score
    run = True
    
    # creating a character to move around
    player = pygame.Rect(200,HEIGHT-PLAYER_HEIGHT,PLAYER_WIDTH,PLAYER_HEIGHT)
    
    # to maintain the speed of the movement
    clock = pygame.time.Clock()
    
    start_time = time.time()
    elapsed_time=0
    
    
    # for projectiles
    star_add_increment = 2000 #create for every 2000ms
    star_count = 0
    
    
    stars = [] #for storing
    hit = False
    
    while run:
        
        # generate projec
        star_count += clock.tick(60)
        
        # clock.tick(60) #mentioning the num of frames per sec / to delay the while loop
        elapsed_time= time.time() - start_time
        current_score = round(elapsed_time * 10)  # Score increases over time
        
        
        if star_count> star_add_increment:
            for _ in range(3):
                star_x = random.randint(0,WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, - STAR_HEIGHT,STAR_WIDTH,STAR_HEIGHT) #-ve height to make sure the proj cms above the screen
                stars.append(star)
            
            star_add_increment = max(200,star_add_increment - 50)    
            star_count=0    
        
        for event in pygame.event.get():
          
          # to close the window if the player click the close button (x button)
          if event.type == pygame.QUIT:
              run = False
              break
          
        #   to make the player move left of right based on what he clicked (left/rigth)
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >=0: #to make sure the player doesnt go outside the screen
            player.x-= PLAYER_VEL #move 5px backward whn clicked left key
            
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH: 
            player.x += PLAYER_VEL    
        
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break    
            
        if hit:
            high_score = max(high_score, current_score)  # Update high score if needed
            lost_text = FONT.render("You Lost !",1,"white")
            WIN.blit(lost_text,(WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))    
            pygame.display.update()
            # pygame.time.delay(4000)
            button_rect = draw_restart_button()  # Draw and get button rectangle
            # break
        
         # Wait for restart button click
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        waiting = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if button_rect.collidepoint(event.pos):
                            main()  # Restart the game
                            return
            break  # Exit the loop and end the game
                
          
        draw(player, elapsed_time, stars, current_score, high_score)
          
    pygame.quit()  
 
#to make sure that even if imported this file, main will not run automatically

# makin sure that main func runs only when this file is executed
if __name__ == "__main__":
     main()