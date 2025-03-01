#Task 01
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

bg_color = [1.0, 1.0, 1.0]
rain_xy = [[random.randint(0, 1280), random.randint(0, 720)] for i in range(100)]
rain_bend = 0
flag = False

def rain():
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(0.043, 0.271, 0.945)

    for i in range(len(rain_xy)):
        x, y = rain_xy[i]
        x2 = x + rain_bend  # Apply bending #initally 0 rakha
        y2 = y - 20  # Droplet falls down

        rain_xy[i] = [x, y2]  # Update position
        if y2 < 0:  # Reset rain if it goes below viewport
            rain_xy[i] = [random.randint(0, 1280), 720]

        glVertex2f(x, y)
        glVertex2f(x2, y2)  # Apply bent endpoint

    glEnd()

def iterate():
    glViewport(0, 0, 1280, 720)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1280, 0.0, 720, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def background():
    glClearColor(*bg_color, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
def house():
    
    #house_rectangle_part 
    #ami try korchi duita somokoni triangle diye rectangle drwa korte taile color fill korte parbo
    glBegin(GL_TRIANGLES)
    glColor3f(0.937, 0.89, 0.686)
    #1st somokoni triangle
    glVertex2f(480, 460)
    glVertex2f(800, 460)
    glVertex2f(480, 240)
    #2nd somokoni triangle
    glVertex2f(800, 460)
    glVertex2f(800, 240)
    glVertex2f(480, 240)
    glEnd()
    
    #window1
    #same duita somokoni niye window rectangle draw korechi
    glBegin(GL_TRIANGLES)
    glColor3f(0.604, 0.851, 0.918)
    #1st somokoni triangle
    glVertex2f(500, 440)
    glVertex2f(600, 440)
    glVertex2f(500, 360)
    #2nd somokoni triangle
    glVertex2f(600, 440)
    glVertex2f(600, 360)
    glVertex2f(500, 360)
    glEnd()
    
    
    #window1 rod
    glLineWidth(4)
    glBegin(GL_LINES)
    glColor3f(0.196, 0.42, 0.478)
    #both horizontal and vertical
    glVertex2f(550, 440)
    glVertex2f(550, 360)
    glVertex2f(500, 400)
    glVertex2f(600, 400)
    glEnd()
    
    #window2
    #same duita somokoni niye window rectangle draw korechi
    glBegin(GL_TRIANGLES)
    glColor3f(0.604, 0.851, 0.918)
    #1st somokoni triangle
    glVertex2f(680, 440)
    glVertex2f(780, 440)
    glVertex2f(680, 360)
    #2nd somokoni triangle
    glVertex2f(780, 440)
    glVertex2f(780, 360)
    glVertex2f(680, 360)
    glEnd()    
    
    #window2 rod
    glLineWidth(4)
    glBegin(GL_LINES)
    glColor3f(0.196, 0.42, 0.478)
    #both horizontal and vertical
    glVertex2f(730, 440)
    glVertex2f(730, 360)
    glVertex2f(680, 400)
    glVertex2f(780, 400)
    glEnd()
    
    #door
    #same duita somokoni niye window rectangle draw korechi
    glBegin(GL_TRIANGLES)
    glColor3f(0.604, 0.851, 0.918)
    #1st somokoni triangle
    glVertex2f(600, 340)
    glVertex2f(680, 340)
    glVertex2f(600, 240)
    #2nd somokoni triangle
    glVertex2f(680, 340)
    glVertex2f(680, 240)
    glVertex2f(600, 240)
    glEnd()    
    
    #tala or key
    glPointSize(10)
    glBegin(GL_POINTS)
    glColor3f(0.196, 0.42, 0.478)
    glVertex2f(670, 290)
    glEnd()
    
    #house top triangle
    glBegin(GL_TRIANGLES)
    glColor3f(0.929, 0.106, 0.141)
    glVertex2f(640, 600)
    glVertex2f(470, 455)
    glVertex2f(810, 455)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    background()
    house()
    rain()
    glutSwapBuffers()

def animate():
    global rain_xy
    for i in range(len(rain_xy)):
        if rain_xy[i][1] - 20 > 0:  # Still inside the viewport
            rain_xy[i][1] -= 20
        else:  # Reset raindrop to top when it falls out
            rain_xy[i][1] = 720

    glutPostRedisplay()

def specialKeyListener(key, m, n):
    global rain_bend
    if key == GLUT_KEY_LEFT:
        rain_bend -= 2  # Increase left bend
        print("Rain bending left")
        print(rain_bend)

    elif key == GLUT_KEY_RIGHT:
        rain_bend += 2  # Increase right bend
        print("Rain bending right")

    glutPostRedisplay()

def keyboardListener(key, m, n):
    global flag
    global bg_color
    if key == b'l':
        bg_color = [1.0, 1.0, 1.0]
        flag = False
    if key == b'd':
        if flag == False:
            bg_color = [0.62, 0.62, 0.62]
            flag = True
        elif flag == True:
            bg_color = [0.0, 0.0, 0.0]
    glutPostRedisplay()    

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1280, 720)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"24241215_Task01")
glutDisplayFunc(display)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)
glutMainLoop()

#Task 02
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

point = [] #all points information store korchi #[x,y,point_color,first_random_move_xy,speed]
point_available_move = [[-1,1],[-1,-1],[1,1],[1,-1]]
speed = 0.05
track_speed = [speed]
reset_color = False
space = False

def iterate():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1024.0, 0.0, 768.0, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_point():
    global point
    
    glPointSize(8)
    glBegin(GL_POINTS)
    
    if len(point)>0:
        for i in range(len(point)):
            r,g,b = point[i][2][0], point[i][2][1], point[i][2][2]
            glColor3f(r,g,b)
            glVertex2f(point[i][0], point[i][1]) 
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    if reset_color == True:
        reset_point_color()
    else:
        draw_point()
    glutSwapBuffers()
    
def animate1(): # Ignore this function:
    glutPostRedisplay()
    global point
    global speed
    
    if len(point)>0:
        for i in range(len(point)):
            x = point[i][0]
            y = point[i][1]
            random_move_x, random_move_y = point[i][3][0], point[i][3][1]
            
            if 0 <= (x + (random_move_x * speed)) <= 1024 and 0 <= (y + (random_move_y * speed)) <= 768: # both x and y are already in my viewport # so pass
                pass
            
            elif 0 <= (x + (random_move_x * speed)) <= 1024: # only x amar control e
                if (y + (random_move_y * speed)) > 768: # y 768 er cheye boro hoye geche # out of my viewport
                    if random_move_x == -1 and random_move_y == 1: #prev direction eita hole next move direction kirokom hobe
                        point[i][3][0] = -1
                        point[i][3][1] = -1
                        random_move_x, random_move_y = point[i][3][0], point[i][3][1]
                    elif random_move_x == 1 and random_move_y == 1: #prev direction eita hole next move direction kirokom hobe
                        point[i][3][0] = 1
                        point[i][3][1] = -1
                        random_move_x, random_move_y = point[i][3][0], point[i][3][1]
                
                elif (y + (random_move_y * speed)) < 0: # y 0 er cheye choto hoye geche # out of my viewport
                    if random_move_x == -1 and random_move_y == -1: #prev direction eita hole next move direction kirokom hobe
                        point[i][3][0] = -1
                        point[i][3][1] = 1
                        random_move_x, random_move_y = point[i][3][0], point[i][3][1]
                    elif random_move_x == 1 and random_move_y == -1: #prev direction eita hole next move direction kirokom hobe
                        point[i][3][0] = 1
                        point[i][3][1] = 1
                        random_move_x, random_move_y = point[i][3][0], point[i][3][1]
        
            elif 0 <= (y + (random_move_y * speed)) <= 768: #only y amar control e
                if (x + (random_move_x * speed)) > 1024: # x 1024 er cheye boro hoye geche # out of my viewport
                    if random_move_x == 1 and random_move_y == -1: #prev direction eita hole next move direction kirokom hobe
                        point[i][3][0] = -1
                        point[i][3][1] = -1
                        random_move_x, random_move_y = point[i][3][0], point[i][3][1]
                    elif random_move_x == 1 and random_move_y == 1: #prev direction eita hole next move direction kirokom hobe
                        point[i][3][0] = -1
                        point[i][3][1] = 1
                        random_move_x, random_move_y = point[i][3][0], point[i][3][1]
                
                elif (x + (random_move_x * speed)) < 0: # x 0 er cheye choto hoye geche # out of my viewport
                    if random_move_x == -1 and random_move_y == -1: #prev direction eita hole next move direction kirokom hobe
                        point[i][3][0] = 1
                        point[i][3][1] = -1
                        random_move_x, random_move_y = point[i][3][0], point[i][3][1]
                    elif random_move_x == -1 and random_move_y == 1: #prev direction eita hole next move direction kirokom hobe
                        point[i][3][0] = 1
                        point[i][3][1] = 1
                        random_move_x, random_move_y = point[i][3][0], point[i][3][1]
                
        
            #final x and y update
            x = x + (random_move_x*speed)
            y = y + (random_move_y*speed)
            point[i][0] = x
            point[i][1] = y        
            
def create_point(x,y):
    global point
    global point_available_move
    global speed
    color = [random.random(), random.random(), random.random()]
    random_first_move_arr_index = random.choice([0, 1, 2, 3]) #4 possible move amar point available move array te store kora ache
    random_first_move_xy = point_available_move[random_first_move_arr_index] #ekta random move select korlam array theke with the help of indexing
    point.append([x, y, color, random_first_move_xy, speed])

def reset_point_color():
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 0.0)
    
    glVertex2f(0, 768)
    glVertex2f(1024, 768)
    glVertex2f(0, 0)
    
    glVertex2f(1024, 768)
    glVertex2f(1024, 0)
    glVertex2f(0, 0)
    
    glEnd()
    
def mouseListener(key, state, x, y):
    global reset_color
    if key == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        create_point(x,768-y) #screen != window coordinate origin
    if key == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if reset_color == False: #kokhono color reset kora hoi nai
            reset_color = True
        elif reset_color == True:
            reset_color = False
    glutPostRedisplay()

def animate():
    glutPostRedisplay()
    global point, speed

    def update_position(p):
        x, y = p[0], p[1]
        move_x, move_y = p[3]

        # x, y new postion
        new_x = x + (move_x * speed)
        new_y = y + (move_y * speed)

        # handle x-axis boundary
        if new_x >= 1024 or new_x <= 0:
            move_x *= -1  # Reverse x direction

        # handle y-axis boundary
        if new_y >= 768 or new_y <= 0:
            move_y *= -1  # Reverse y direction

        # Return updated point with the new position and direction
        return [new_x, new_y, p[2], [move_x, move_y], p[4]]

    # Apply updates to all points at once
    point = list(map(update_position, point))

def specialKeyListener(key, x ,y):
    global speed
    if key==GLUT_KEY_UP:
        speed += 0.01
    if key== GLUT_KEY_DOWN:
        if speed - 0.01 > 0:
            speed -= 0.01
        else:
            print("Reached Most Minimum Speed")
    glutPostRedisplay()
    
def keyboardListener(key, x, y):
    global speed
    global space
    global track_speed
    
    if key == b' ':
        if space == False:
            track_speed[0] = speed
            speed = 0
            space = True
        else:
            speed = track_speed[0]
            space = False
    glutPostRedisplay()        

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1024, 768)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"24241215_Task02")
glutMouseFunc(mouseListener)
glutDisplayFunc(display)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)
glutMainLoop()