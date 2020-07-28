import pandas as pd
import pygame, sys, random
from sklearn.neighbors import KNeighborsRegressor


def ball_animation():

    global v_ball_x, v_ball_y, player_score, ai_score

    # Initialize ball velocity
    ball.x += v_ball_x
    ball.y += v_ball_y

    # Define edge conditions
    if ball.top <= 0 or ball.bottom >= screen_height:
        v_ball_y *= -1
    if ball.left <= 0:
        player_score += 1
        game_restart()
    if ball.right >= screen_width:
        ai_score += 1
        game_restart()

    # Bounce off paddles
    if ball.colliderect(right_paddle) or ball.colliderect(left_paddle):
        v_ball_x *= -1

def right_paddle_player():

    global right_paddle

    right_paddle.y += v_right_paddle
    if right_paddle.top <= 0:
        right_paddle.top = 0
    if right_paddle.bottom >= screen_height:
        right_paddle.bottom = screen_height

def left_paddle_dumb_ai():
    
    global left_paddle

    if left_paddle.top < ball.y:
        left_paddle.top += v_left_paddle
    if left_paddle.bottom > ball.y:
        left_paddle.bottom -= v_left_paddle
    if left_paddle.top <= 0:
        left_paddle.top = 0
    if left_paddle.bottom >= screen_height:
        left_paddle.bottom = screen_height

    playerbehavior = open("training_data.csv", "w")
    print("ball x, ball y, velocity x, velocity y, right paddle", file = playerbehavior)

def left_paddle_ai():

    global left_paddle, shouldMove

    # Regression prediction
    if left_paddle.top < shouldMove:
        left_paddle.top += v_left_paddle
    if left_paddle.bottom > shouldMove:
        left_paddle.bottom -= v_left_paddle
    if left_paddle.top <= 0:
        left_paddle.top = 0
    if left_paddle.bottom >= screen_height:
        left_paddle.bottom = screen_height

def game_restart():

    global v_ball_x, v_ball_y

    ball.center = (screen_width/2, screen_height/2)
    v_ball_y *= random.choice((1, -1))
    v_ball_x *= random.choice((1, -1))

# Setup Pygame
pygame.init()
clock = pygame.time.Clock()

# Initialize display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('AI Pong')

# Define Objects
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 20, 20)
right_paddle = pygame.Rect(screen_width - 40, screen_height/2 - 70, 20, 160)
left_paddle = pygame.Rect(20, screen_height/2 - 70, 20, 160)

# Define variables
black = (0, 0, 0)
white = (255, 255, 255)
grey = (32, 32, 32)
v_ball_x = 5 * random.choice((1, -1))
v_ball_y = 7 * random.choice((1, -1))
v_right_paddle = 0
v_left_paddle = 9
player_score = 0
ai_score = 0
font = pygame.font.SysFont('cour.ttf',36)

"""
# Training
training_data = pd.read_csv('training_data.csv')
training_data = training_data.drop_duplicates()

for ind, row in training_data.iterrows():
    training_data.loc[ind, "ball x rev"] = 800 - row['ball x'] 

y = training_data[' right paddle']
X = training_data.drop(columns = [" right paddle", "ball x"])

clf = KNeighborsRegressor(n_neighbors=3)
clf = clf.fit(X, y)
"""

playerbehavior = open("training_data.csv", "w")
print("ball x, ball y, velocity x, velocity y, right paddle", file = playerbehavior)

# Execution loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                v_right_paddle += 10
            if event.key == pygame.K_UP:
                v_right_paddle -= 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                v_right_paddle -= 10
            if event.key == pygame.K_UP:
                v_right_paddle += 10

    """
    df = pd.DataFrame(columns = ['ball y', 'velocity x', 'velocity y', 'ball x rev'])
    toPredict = df.append({'ball y' : ball.y, 'velocity x' : v_ball_x, 'velocity y' : v_ball_y, 'ball x rev' : ball.x}, ignore_index = True)
    shouldMove = clf.predict(toPredict)
    """

    ball_animation()
    right_paddle_player()
    left_paddle_dumb_ai()   # matches paddle to the y value of the ball and records player behavior 
    #left_paddle_ai()        # uses linear regression model to match players behavior 

    # Draw objects
    screen.fill(black)
    pygame.draw.rect(screen, white, right_paddle)
    pygame.draw.rect(screen, white, left_paddle)
    pygame.draw.ellipse(screen, white, ball)
    pygame.draw.aaline(screen, grey, (screen_width/2, 0), (screen_width/2, screen_height))
    
    # Draw score
    ai_text = font.render(f"{ai_score}", False, grey)
    screen.blit(ai_text, (screen_width/4, screen_height/2))
    player_text = font.render(f"{player_score}", False, grey)
    screen.blit(player_text, (3*(screen_width/4) , screen_height/2))

    # Record to csv
    print("{}, {}, {}, {}, {}".format(ball.x, ball.y, v_ball_x, v_ball_y, right_paddle.y), file = playerbehavior)

    # Render the display at a speed
    pygame.display.flip()
    clock.tick(60)

