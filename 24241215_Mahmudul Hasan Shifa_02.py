from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

def diamond_color_generate():
    r = random.uniform(0.5, 1)
    g = random.uniform(0.5, 1)
    b = random.uniform(0.5, 1)
    return [r,g,b] 

catcherX = 160 #eita only starting point of x and top line
catcherY = 25 #eita only starting point of y and top line
diamondX = random.randint(10, 390)
diamondY = 550
color_catcher = [0,0.196,1]
color_pause_play = [0.914,1,0]
color_cross = [1,0,0]
color_reset = [0,0.631,1]
color_diamond = diamond_color_generate()
play_flag = True 
pause_flag = False
reset_flag = False
score = 0
game_over = False
game_paused = False
before_pause_diamondX = 0
before_pause_diamondY = 0
falling_speed = 50  # initial speed (pixels per second) 50px 1 seconds e
last_time = time.time()  # initial time


def draw_point(x,y,obj):
    global color_catcher, color_pause_play, color_cross, color_reset, color_diamond 
    glPointSize(1)
    glBegin(GL_POINTS)
    
    if obj == "obj_catcher":
        glColor3f(color_catcher[0], color_catcher[1], color_catcher[2])
    if obj == "obj_pause" or obj == "obj_play":
        glColor3f(color_pause_play[0], color_pause_play[1], color_pause_play[2])
    if obj == "obj_cross":
        glColor3f(color_cross[0], color_cross[1], color_cross[2])
    if obj == "obj_reset":
        glColor3f(color_reset[0], color_reset[1], color_reset[2])
    if obj == "obj_diamond":
        glColor3f(color_diamond[0], color_diamond[1], color_diamond[2])

    glVertex2f(x,y)
    glEnd()

def zone_find(x1,y1,x2,y2):
    dx = x2-x1
    dy = y2-y1
    abs_dx = abs(dx)
    abs_dy = abs(dy)
    zone = 0

    if (abs_dx > abs_dy):
        if dx>0 and dy>0:
          zone = 0
        elif dx>0 and dy<0:
            zone = 7  
        elif dx<0 and dy>0:
            zone = 3
        elif dx<0 and dy<0:
            zone = 4
    
    elif (abs_dx < abs_dy):
        if dx>0 and dy>0:
          zone = 1
        elif dx<0 and dy>0:
            zone = 2
        elif dx<0 and dy<0:
            zone = 5
        elif dx>0 and dy<0:
            zone = 6
    
    return zone
            
def convert_zone_0(x1,y1,x2,y2):
    zone = zone_find(x1,y1,x2,y2)
    if zone == 0:
        pass
    elif zone == 1:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    elif zone == 2:
        x1, y1 = y1, x1*(-1)
        x2, y2 = y2, x2*(-1)
    elif zone == 3:
        x1, y1 = x1*(-1), y1
        x2, y2 = x2*(-1), y2
    elif zone == 4:
        x1, y1 = x1*(-1), y1*(-1)
        x2, y2 = x2*(-1), y2*(-1)
    elif zone == 5:
        x1, y1 = y1*(-1), x1*(-1)
        x2, y2 = y2*(-1), x2*(-1)
    elif zone == 6:
        x1, y1 = y1*(-1), x1
        x2, y2 = y2*(-1), x2
    elif zone == 7:
        x1, y1 = x1, y1*(-1)
        x2, y2 = x2, y2*(-1)
    
    converted_two_points = (x1,y1,x2,y2)
    original_origin = zone
    
    return converted_two_points, original_origin

def convert_original_zone(x1,y1,zone):
    if zone == 0:
        pass
    elif zone == 1:
        x1, y1 = y1, x1
    elif zone == 2:
        x1, y1 = y1*(-1), x1
    elif zone == 3:
        x1, y1 = x1*(-1), y1  
    elif zone == 4:
        x1, y1 = x1*(-1), y1*(-1)
    elif zone == 5:
        x1, y1 = y1*(-1), x1*(-1)
    elif zone == 6:
        x1, y1 = y1, x1*(-1)
    elif zone == 7:
        x1, y1 = x1, y1*(-1)

    return (x1,y1)
        
def line_draw(x1,y1,x2,y2,obj): #obj diye color identify korar jonno
    if x1 == x2:  # Vertical line case
        while y1 >= y2:
            draw_point(x1, y1, obj)
            y1 -= 1
    elif y1 == y2: #Horizontal line case
        while x1 <= x2:
            draw_point(x1, y1, obj)
            x1+=1
    else:
        converted_two_points, original_zone = convert_zone_0(x1,y1,x2,y2)
        x1,y1,x2,y2 = converted_two_points[0], converted_two_points[1], converted_two_points[2], converted_two_points[3]
        dx = x2-x1
        dy = y2-y1
        dE = 2*dy
        dNE = 2*dy - 2*dx
        d_init = 2*dy - dx
        
        while x1<=x2:
            if d_init>0:
                d_init+=dNE

                if original_zone != 0:
                    final_x1, final_y1 = convert_original_zone(x1,y1,original_zone)
                    draw_point(final_x1, final_y1, obj)
                else:
                    draw_point(x1, y1, obj)
            
                x1+=1
                y1+=1
                
            else:
                d_init+=dE
                
                if original_zone != 0:
                    final_x1, final_y1 = convert_original_zone(x1,y1,original_zone)
                    draw_point(final_x1, final_y1, obj)
                else:
                    draw_point(x1, y1, obj)
                    
                x1+=1
                y1+=0     
        
def iterate():
    glViewport(0, 0, 400, 600)
    glOrtho(0.0, 400, 0.0, 600, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    
def catcher():
    top = line_draw(catcherX, catcherY, catcherX+80, catcherY,"obj_catcher")
    down = line_draw(catcherX+10, catcherY-20, catcherX+70, catcherY-20,"obj_catcher")
    left = line_draw(catcherX, catcherY, catcherX+10, catcherY-20,"obj_catcher")
    right = line_draw(catcherX+80, catcherY, catcherX+70, catcherY-20,"obj_catcher")
    
def pause():
    left = line_draw(190,590,190,565,"obj_pause")
    right = line_draw(210,590,210,565,"obj_pause")

def play():
    left = line_draw(190,590,190,565,"obj_play")
    vertical1 = line_draw(190,590,210,577.5,"obj_play")
    vertical2 = line_draw(190,565,210,577.5, "obj_play")

def cross():
    line1 = line_draw(370,590,390,565, "obj_cross")
    line2 = line_draw(390,590,370,565, "obj_cross")

def reset():
    line1 = line_draw(10,577.5,40,577.5,"obj_reset")
    line2 = line_draw(25,590,10,577.5,"obj_reset")
    line3 = line_draw(10,577.5,25,565,"obj_reset")

def diamond():
    global diamondX, diamondY
    line1 = line_draw(diamondX,diamondY,diamondX-10,diamondY-15, "obj_diamond")
    line2 = line_draw(diamondX,diamondY,diamondX+10,diamondY-15, "obj_diamond")
    line3 = line_draw(diamondX-10,diamondY-15,diamondX,diamondY-30, "obj_diamond")
    line4 = line_draw(diamondX+10,diamondY-15,diamondX,diamondY-30, "obj_diamond")

def display():
    global color_catcher
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    if game_over == False:
        diamond() 
    
    catcher()
        
    if play_flag == True and pause_flag == False:
        pause()
    if pause_flag == True and play_flag == False:
        play()
    
    cross()
    reset()
    glutSwapBuffers()
    
def specialKeyboardListener(key, x, y):
    global catcherX, catcherY, play_flag, pause_flag, game_over, color_catcher
    if play_flag == True and pause_flag == False:
        if game_over == False:
            if key == GLUT_KEY_LEFT:
                if catcherX - 10 >= 0:
                    catcherX = catcherX - 10
                
            elif key == GLUT_KEY_RIGHT:
                if catcherX + 10 <= 320: #cause 320 staring point like emon (320,25), so ending point hobe (320+80,25) = (400,25) so fit my window
                    catcherX = catcherX + 10

    elif pause_flag == True and play_flag == False:
        pass  
    
    glutPostRedisplay()

def restart_game():
    global catcherX, catcherY, diamondX, diamondY, color_diamond, play_flag, pause_flag, score, game_over, falling_speed, color_catcher, last_time

    catcherX = 160
    catcherY = 25
    diamondX = random.randint(10, 390)
    diamondY = 550

    color_catcher = [0, 0.196, 1]
    color_diamond = diamond_color_generate()

    score = 0
    game_over = False
    falling_speed = 50
    last_time = time.time()
    play_flag = True
    pause_flag = False

    glutIdleFunc(animate)
    #glutPostRedisplay()

def mouseListener(button, state, x, y):
    global play_flag, pause_flag, diamondX, diamondY, game_over

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 190 <= x <= 210 and (600-590) <= y <= (600-565):
            if game_over == False:
                if play_flag == True:
                    pause_flag = True
                    play_flag = False
                    print("Game Paused")

                    
                elif play_flag == False:
                    play_flag = True
                    pause_flag = False
                    print("Game Resumed")

        if 370 <= x <= 390 and (600-590) <= y <= (600-565):
            print("Good Bye")
            glutLeaveMainLoop()
            
        
        if 10 <= x <= 25 and (600-590) <= y <= (600-565):
            print("Starting Over")
            restart_game()
            
    glutPostRedisplay()

def animate():
    global diamondX, diamondY, color_diamond, falling_speed, last_time, catcherX, catcherY, score, game_over, color_catcher, before_pause_diamondX, before_pause_diamondY, pause_flag, play_flag
    if play_flag == True:
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time

        diamondY -= falling_speed * delta_time  # Move based on time
        
        before_pause_diamondX = diamondX
        before_pause_diamondY = diamondY

        if diamondY<=0:
            print(f"Game Over! Score: {score}")
            score = 0
            game_over = True
            color_catcher = [1,0,0]
            glutIdleFunc(None)
            
            
        if 50<=diamondY<=55:
            if catcherX<=(diamondX+10)<=(catcherX+80) and catcherX<=(diamondX-10)<=(catcherX+80):
                score+=1
                print(f"Score: {score}")
                diamondY = 550
                diamondX = random.randint(10, 390)
                color_diamond = diamond_color_generate()
                falling_speed += 5
        
        # else:
        #     print('Game Over')
        #     print(f"Final Score: {score}")
        #     score = 0
        #     return
    else:
        last_time = time.time()
        diamondX = before_pause_diamondX
        diamondY = before_pause_diamondY
    
    glutPostRedisplay()

    
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(400, 600)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow(b"Diamond Catcher Game")
glutMouseFunc(mouseListener)
glutSpecialFunc(specialKeyboardListener)
glutDisplayFunc(display)
glutIdleFunc(animate)
glutMainLoop()