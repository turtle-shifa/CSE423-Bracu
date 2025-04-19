from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Camera-related variables
camera_pos = (0, 410, 500)  # 410 for stating screen looks more realistic; no white boundary
camera_angle = 0  # Angle of camera rotation around the scene (in degrees)
is_first_person = False  # Flag to track camera mode: False for third-person, True for first-person
follow_gun_view = False

fovY = 120  # Field of view
character_pos = [0, 0, 0]  # x, y, z position of character
gun_angle = 90  # Gun and character rotation angle because character movement across gun direction
movement_angle = 90  # Separate angle for consistent movement in cheat mode
move_speed = 5  # character movement speed

# Cheat mode variables
cheat_mode = False
auto_rotation_speed = 3  # Degrees per frame
last_auto_fire_time = 0
auto_fire_delay = 15  # Frames between automatic shots

enemy_scale_min = 0.5
enemy_scale_max = 1
enemy_scale_steps = 20 #20*0.025 = 0.5 hoye jacche
enemy_scale_increment =  0.025 #enemy scale increment korlam 1+0.025 = 1.025 #(enemy_scale_max - enemy_scale_min) / enemy_scale_steps
enemy_scale_increase_or_decrease = 1  # 1 for increasing, -1 for decreasing
scale_timer = 0  # Timer to control scale switching
scale_interval = 100  # Number of frames for full scale cycle (slowed down)

score = 0
bullets_missed = 0
life = 5
game_over = False

num_enemies = 5
enemy_positions = []
enemy_scales = []
enemy_speed = 0.1

min_spawn_distance = 250  # Distance from character to prevent close spawns #taratari out hoye jai

bullets = []
bullet_size = 10
bullet_speed = 15
max_bullets_missed = 10  # Maximum allowed missed bullets

# Initialize enemies
for i in range(num_enemies):
    #jotokhon nah amar character er theke far distance e enemy create na hocche
    #totkhon jeno random point generate hoi
    while True:
        pos = [random.randint(-550, 550), random.randint(-550, 550), 0]
        if math.sqrt((pos[0]-character_pos[0])**2 + (pos[1]-character_pos[1])**2) >= min_spawn_distance:
            #calculate Euclidean distance formula Root((x1-x2)**2+(y1-y2)**2)
            break
    
    enemy_positions.append(pos)
    enemy_scales.append(1.0)  # Start at 1.0

def distance(p1, p2):
    #calculate Euclidean distance formula Root((x1-x2)**2+(y1-y2)**2) but eita hocche 3d version
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    """Draw text on the screen"""
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def is_enemy_in_sight(enemy_pos):
    """
    Determines if an enemy is in the line of sight of the character's gun.
    Returns True if enemy is in line of sight, False otherwise.
    """
    # Calculate gun direction vector
    angle_radians = math.radians(gun_angle)
    gun_dir_x = -math.cos(angle_radians)
    gun_dir_y = -math.sin(angle_radians)
    
    # Vector from character to enemy
    dx = enemy_pos[0] - character_pos[0]
    dy = enemy_pos[1] - character_pos[1]
    
    # Calculate distance to enemy (in xy plane)
    distance_to_enemy = math.sqrt(dx*dx + dy*dy)
    
    if distance_to_enemy < 1:  # Avoid division by zero
        return False
    
    # Normalize the vector
    dx /= distance_to_enemy
    dy /= distance_to_enemy
    
    # Calculate dot product (cos of angle between vectors)
    dot_product = gun_dir_x * dx + gun_dir_y * dy
    
    # If dot product is close to 1, vectors are pointing in the same direction
    # This means the enemy is in the line of sight
    # Using 0.95 allows for some aiming error (about 18 degrees)
    #game development e eita use hoi
    # 1 → exact same direction (angle = 0°)
    # 0 → perpendicular (angle = 90°)
    # -1 → exactly opposite (angle = 180°)
    return dot_product > 0.95

def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global gun_angle, character_pos, move_speed, game_over, cheat_mode, movement_angle, follow_gun_view

    if game_over:
        if key == b'r':
            reset_game()
        return

    # Toggle cheat mode with 'c' key
    if key == b'c':
        cheat_mode = not cheat_mode
        movement_angle = gun_angle
    
    # Toggle camera following gun with 'v' key when in first-person and cheat mode
    if key == b'v' and is_first_person and cheat_mode:
        follow_gun_view = not follow_gun_view
    
    # Only process manual rotation when not in cheat mode
    if not cheat_mode:
        if key == b'a':
            gun_angle += 5
            movement_angle = gun_angle
            if gun_angle >= 360:
                gun_angle -= 360
                movement_angle = gun_angle
        
        if key == b'd':
            gun_angle -= 5
            movement_angle = gun_angle
            if gun_angle < 0:
                gun_angle += 360
                movement_angle = gun_angle
    
    # In cheat mode, use a stable movement direction regardless of gun rotation
    move_direction_angle = movement_angle if cheat_mode else gun_angle
    
    # Movement is allowed in both modes
    if key == b'w':  # Forward movement
        angle_radians = math.radians(move_direction_angle)
        dx = move_speed * math.cos(angle_radians)
        dy = move_speed * math.sin(angle_radians)
        new_x = character_pos[0] - dx
        new_y = character_pos[1] - dy
        
        if -560 <= new_x <= 560 and -560 <= new_y <= 560:
            character_pos[0] = new_x
            character_pos[1] = new_y
    
    if key == b's':  # Backward movement
        angle_radians = math.radians(move_direction_angle)
        dx = move_speed * math.cos(angle_radians)
        dy = move_speed * math.sin(angle_radians)
        new_x = character_pos[0] + dx
        new_y = character_pos[1] + dy
        
        if -560 <= new_x <= 560 and -560 <= new_y <= 560:
            character_pos[0] = new_x
            character_pos[1] = new_y
    
    if key == b'r':  # Reset game
        reset_game()
    
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera position and angle:
    - UP/DOWN: Move camera up and down
    - LEFT/RIGHT: Rotate camera around the scene
    """
    global camera_pos, camera_angle, is_first_person
    
    # Only allow camera adjustments in third-person mode
    if not is_first_person:
        x, y, z = camera_pos
        
        if key == GLUT_KEY_UP:
            # Move camera up (increase z)
            if z < 800:  # Limit maximum height
                z += 20
        
        elif key == GLUT_KEY_DOWN:
            # Move camera down (decrease z)
            if z > 200:  # Don't go below ground level
                z -= 20
        
        elif key == GLUT_KEY_LEFT:
            # Rotate camera counterclockwise around the scene
            camera_angle += 5
            if camera_angle >= 360:
                camera_angle -= 360
                
        elif key == GLUT_KEY_RIGHT:
            # Rotate camera clockwise around the scene
            camera_angle -= 5
            if camera_angle < 0:
                camera_angle += 360
        
        # Update camera position with new coordinates
        camera_pos = (x, y, z)
    
    glutPostRedisplay()

def fire_bullet():
    global bullets, gun_angle, character_pos, cheat_mode, enemy_positions
    angle_radians = math.radians(gun_angle)
    
    gun_length = 80 #Because I set it earlier
    gun_offset_x = -math.cos(angle_radians) * gun_length #rcos(theta) #minus cause amar left right typical coordiante x er moton nah
    gun_offset_y = -math.sin(angle_radians) * gun_length #rcos(theta) #minus cause amar inside outside typical coordiante y er moton nah
    
    #gun theke + amar character theke kotodure bullet ber hobe
    start_x = character_pos[0] + gun_offset_x
    start_y = character_pos[1] + gun_offset_y
    start_z = character_pos[2] + 100  # gun z-position 
    
    # Direction vector for bullet movement
    dx = -math.cos(angle_radians) * bullet_speed
    dy = -math.sin(angle_radians) * bullet_speed
    
    # Find the closest enemy in the firing direction if in cheat mode
    #auto target set korar jonno
    target_index = -1
    if cheat_mode:
        # Find an enemy that's in line of sight
        for i, enemy_pos in enumerate(enemy_positions):
            if is_enemy_in_sight(enemy_pos):
                target_index = i
                break
    
    # Add bullet to active bullets list
    bullets.append({
        'position': [start_x, start_y, start_z],
        'direction': [dx, dy, 0],
        'active': True,
        'homing': cheat_mode,  # Enable homing for cheat mode
        'target_enemy_index': target_index  # Set target enemy index
    })

def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and camera mode toggle (right click)
    """
    global game_over, is_first_person
    
    if game_over:
        return
        
    # Left mouse button fires a bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()
        glutPostRedisplay()
    
    # Right mouse button toggles camera mode
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if is_first_person == True:
            is_first_person = False
        elif is_first_person == False:
            is_first_person = True
        glutPostRedisplay()

def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    global is_first_person, character_pos, gun_angle, camera_pos, camera_angle, follow_gun_view
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    if is_first_person:
        gluPerspective(100, 1.25, 0.1, 1500)
    else:
        gluPerspective(fovY, 1.25, 0.1, 1500)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if is_first_person:
        # First-person camera: Position at character's head
        eye_x = character_pos[0]
        eye_y = character_pos[1]
        eye_z = character_pos[2] + 150  # Height of character's head
        
        # Determine which direction to look
        if cheat_mode and not follow_gun_view:
            # Default in cheat mode: Fixed forward view (90 degrees)
            fixed_angle = math.radians(90)
            look_x = eye_x - math.cos(fixed_angle) * 100
            look_y = eye_y - math.sin(fixed_angle) * 100
        else:
            # Follow gun rotation: either not in cheat mode, or in cheat mode with V toggled
            angle_radians = math.radians(gun_angle)
            look_x = eye_x - math.cos(angle_radians) * 100
            look_y = eye_y - math.sin(angle_radians) * 100
        
        look_z = eye_z  # Keep looking horizontally
        
        # Position the first-person camera
        gluLookAt(eye_x, eye_y, eye_z,
                  look_x, look_y, look_z,
                  0, 0, 1)  # Up vector (z-axis)
    else:
        # Third-person camera
        x, y, z = camera_pos
        angle_rad = math.radians(camera_angle)
        radius = 600
        x = radius * math.cos(angle_rad)
        y = radius * math.sin(angle_rad)
        
        gluLookAt(x, y, z,
                  0, 0, 0,
                  0, 0, 1)

def idle():
    global enemy_positions, bullets, score, bullets_missed, life, enemy_scales, game_over
    global enemy_scale_increment, enemy_scale_increase_or_decrease, scale_timer, enemy_scale_min, enemy_scale_max
    global gun_angle, cheat_mode, last_auto_fire_time
    
    if game_over:
        glutPostRedisplay()
        return
    
    # Cheat mode automatic rotation and firing
    if cheat_mode:
        # Automatically rotate gun
        gun_angle += auto_rotation_speed
        if gun_angle >= 360:
            gun_angle -= 360
        
        # Check for enemies in line of sight
        last_auto_fire_time += 1
        if last_auto_fire_time >= auto_fire_delay:  # Limit fire rate
            for i, enemy_pos in enumerate(enemy_positions):
                if is_enemy_in_sight(enemy_pos):
                    # Adjust gun angle to precisely target this enemy for better accuracy
                    dx = enemy_pos[0] - character_pos[0]
                    dy = enemy_pos[1] - character_pos[1]
                    target_angle = math.degrees(math.atan2(dy, dx)) + 180
                    if target_angle >= 360:
                        target_angle -= 360
                    
                    # Set gun to exact angle for perfect aim
                    gun_angle = target_angle
                    
                    fire_bullet()
                    last_auto_fire_time = 0
                    break
    
    scale_timer += 1
    if scale_timer >= scale_interval // enemy_scale_steps:  # Divide interval by steps for smoother transitions
        scale_timer = 0
        #ami chacchi every 5 frames por por jeno scale increment hoi
        #100//20 = 5 means 5 frame hole scale size 0.025 increment or decrement hobe
        # Update all enemy scales
        for i in range(len(enemy_scales)):
            new_scale = enemy_scales[i] + (enemy_scale_increment * enemy_scale_increase_or_decrease)

            if new_scale >= enemy_scale_max:
                new_scale = enemy_scale_max
                enemy_scale_increase_or_decrease = -1  # Switch to decreasing
            elif new_scale <= enemy_scale_min:
                new_scale = enemy_scale_min
                enemy_scale_increase_or_decrease = 1   # Switch to increasing
                
            enemy_scales[i] = new_scale
    
    # Move enemies towards player
    for i in range(len(enemy_positions)):
        # Calculate direction to player
        dx = character_pos[0] - enemy_positions[i][0]
        dy = character_pos[1] - enemy_positions[i][1]
        
        # Normalize direction #distance ta ke 1 kore means magnitude
        #Consistent Movement Speed
        #If dx = 3, dy = 4:        
        # Length = sqrt(3² + 4²) = 5
        # Normalized:
        # dx = 3/5 = 0.6,
        # dy = 4/5 = 0.8
        # Now (0.6, 0.8) is a direction vector pointing the same way as (3, 4) but with length 1.
        
        length = math.sqrt(dx*dx + dy*dy) 
        if length > 0:
            dx /= length
            dy /= length
        
        # Move enemy towards player
        enemy_positions[i][0] += dx * enemy_speed
        enemy_positions[i][1] += dy * enemy_speed
        
        # Check for collision with player
        enemy_collision_radius = 60 * enemy_scales[i]  # Enemy radius
        player_collision_radius = 30  # Approximate player radius
        
        if distance(character_pos, enemy_positions[i]) < enemy_collision_radius + player_collision_radius:
            # Player hit by enemy
            #enemy and character er radius add kore ami dekhbo enemy and character er distance theke kom
            life -= 1
            
            # Respawn enemy at random position away from character
            while True:
                new_pos = [random.randint(-550, 550), random.randint(-550, 550), 0]
                if distance(character_pos, new_pos) >= min_spawn_distance:
                    enemy_positions[i] = new_pos
                    break
            
            if life <= 0:
                game_over = True
    
    # Update bullet positions and check for collisions
    bullets_to_remove = []
    
    for i, bullet in enumerate(bullets): #enumerate diye track index and element both at a single time
        if not bullet['active']:
            bullets_to_remove.append(i)
            continue
        
        # Handle homing bullets in cheat mode
        if bullet.get('homing', False) and cheat_mode:
            # If bullet has a target
            if bullet.get('target_enemy_index', -1) >= 0 and bullet.get('target_enemy_index', -1) < len(enemy_positions):
                target = enemy_positions[bullet['target_enemy_index']]
                
                # Calculate direction to target
                dx = target[0] - bullet['position'][0]
                dy = target[1] - bullet['position'][1]
                dz = 30 - bullet['position'][2]  # Aim at enemy body height
                
                # Normalize direction
                length = math.sqrt(dx*dx + dy*dy + dz*dz)
                if length > 0:
                    dx /= length
                    dy /= length
                    dz /= length
                
                # Set bullet direction with increased speed for homing
                bullet['direction'] = [dx * bullet_speed * 1.5, dy * bullet_speed * 1.5, dz * bullet_speed]
            else:
                # Find a new target if original is gone
                for j, enemy_pos in enumerate(enemy_positions):
                    bullet['target_enemy_index'] = j
                    break
            
        # Move bullet
        bullet['position'][0] += bullet['direction'][0]
        bullet['position'][1] += bullet['direction'][1]
        bullet['position'][2] += bullet['direction'][2]
        
        # Check if bullet is outside game boundaries
        if (bullet['position'][0] < -600 or bullet['position'][0] > 600 or
            bullet['position'][1] < -600 or bullet['position'][1] > 600):
            
            # Only count as missed if not in cheat mode
            if not cheat_mode:
                bullets_missed += 1
            
            bullet['active'] = False
            bullets_to_remove.append(i)
            
            if bullets_missed >= max_bullets_missed:
                game_over = True
            
            continue
        
        # Check for collisions with enemies - IMPROVED DETECTION
        hit_detected = False
        for j, enemy_pos in enumerate(enemy_positions):
            enemy_collision_radius = 60 * enemy_scales[j]  # Enemy radius scaled
            
            # Debug for collision detection
            bullet_pos = bullet['position']
            
            # Calculate distance in 2D (x-y plane)
            dx = bullet_pos[0] - enemy_pos[0]
            dy = bullet_pos[1] - enemy_pos[1]
            dist_2d = math.sqrt(dx*dx + dy*dy)
            
            # Check if bullet is at appropriate height (z-axis)
            # Enemy body is around z=0 to z=60, head is higher
            # Bullet is at z=100 (gun height)
            # Allow generous z-range for bullet to hit enemy
            z_diff = abs(bullet_pos[2] - 30)  # Check against middle of enemy
            
            if dist_2d < enemy_collision_radius and z_diff < 100:  # More generous z-range for hits
                # Bullet hit enemy - increase score!
                score += 1
                bullet['active'] = False
                bullets_to_remove.append(i)
                hit_detected = True
                
                # Respawn enemy at random position away from character
                while True:
                    new_pos = [random.randint(-550, 550), random.randint(-550, 550), 0]
                    if distance(character_pos, new_pos) >= min_spawn_distance:
                        enemy_positions[j] = new_pos
                        break
                break
                
        if hit_detected:
            continue
    
    # Remove inactive bullets
    for index in sorted(bullets_to_remove, reverse=True): #naile vul index remove hoye jacche
        if index < len(bullets):
            bullets.pop(index)
    
    glutPostRedisplay()

def reset_game():
    """Reset the game state to start a new game"""
    global character_pos, gun_angle, score, bullets_missed, life, bullets, game_over, enemy_positions, enemy_scales
    global enemy_scale_increase_or_decrease, scale_timer, is_first_person, camera_pos, camera_angle, cheat_mode
    global movement_angle  # Reset movement angle too
    
    character_pos = [0, 0, 0]
    gun_angle = 90
    movement_angle = 90  # Reset movement angle to match gun angle
    score = 0
    bullets_missed = 0
    life = 5
    bullets.clear() #all elements remove kore dilam
    game_over = False
    enemy_scale_increase_or_decrease = 1
    is_first_person = False  # Reset to third-person view
    camera_pos = (0, 410, 500)  # Reset camera to default position
    camera_angle = 0  # Reset camera rotation angle
    cheat_mode = False  # Disable cheat mode when game is reset
    follow_gun_view = False
    # Reset enemies
    enemy_positions.clear()
    enemy_scales.clear()
    
    for i in range(num_enemies):
        while True:
            pos = [random.randint(-550, 550), random.randint(-550, 550), 0]
            if math.sqrt((pos[0]-character_pos[0])**2 + (pos[1]-character_pos[1])**2) >= min_spawn_distance:
                break
        
        enemy_positions.append(pos)
        enemy_scales.append(1.0)

def game_floor():
    glBegin(GL_QUADS)
    x_point = 600
    y_point = -600
    current_grid_color = ''
    for row in range(12):  # 12 grids for easier calculation
        x_point = 600
        for col in range(12):
            if current_grid_color == '' or current_grid_color == 'p':  # p means purple and '' means starting so no color set yet
                glColor3f(1, 1, 1)
                glVertex3f(x_point-100, y_point+100, 0)
                glVertex3f(x_point, y_point+100, 0)
                glVertex3f(x_point, y_point, 0)
                glVertex3f(x_point-100, y_point, 0)
                current_grid_color = 'w'
            
            elif current_grid_color == 'w':
                glColor3f(0.776, 0.4, 1)
                glVertex3f(x_point-100, y_point+100, 0)
                glVertex3f(x_point, y_point+100, 0)
                glVertex3f(x_point, y_point, 0)
                glVertex3f(x_point-100, y_point, 0)
                current_grid_color = 'p'
                           
            x_point-=100
        
        if current_grid_color == 'p':
            current_grid_color = 'w'
        elif current_grid_color == 'w':
            current_grid_color = 'p'
        
        y_point+=100
    
    glEnd()

def floor_boundary():
    glBegin(GL_QUADS)
    
    # green
    glColor3f(0.18, 1, 0.204)
    glVertex3f(-600, 600, 100)
    glVertex3f(-600, 600, 0)
    glVertex3f(-600, -600, 0)
    glVertex3f(-600, -600, 100)
    
    # cyan
    glColor3f(0.18, 0.957, 1)
    glVertex3f(-600, -600, 0)
    glVertex3f(600, -600, 0)
    glVertex3f(600, -600, 100)
    glVertex3f(-600, -600, 100)
    
    # blue
    glColor3f(0, 0, 1)
    glVertex3f(600, 600, 100)
    glVertex3f(600, -600, 100)
    glVertex3f(600, -600, 0)
    glVertex3f(600, 600, 0)
    
    # white
    glColor3f(1, 1, 1)
    glVertex3f(-600, 600, 100)
    glVertex3f(600, 600, 100)
    glVertex3f(600, 600, 0)
    glVertex3f(-600, 600, 0)
    
    glEnd()

def player():
    glPushMatrix()
    glTranslatef(character_pos[0], character_pos[1], character_pos[2])  # Position the character
    glRotatef(gun_angle, 0, 0, 1)  # Rotate character based on gun angle along Z axis

    # Hide character model in first-person mode (except for gun)
    if is_first_person:
        # Only draw the gun in first-person mode
        # gun
        glColor3f(0.753, 0.753, 0.753)
        glPushMatrix()
        glTranslatef(0, 0, 100)
        glRotatef(-90, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 12, 7, 80, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
        glPopMatrix()
    else:
        # Draw full character model in third-person mode
        # body
        glColor3f(0.333, 0.42, 0.184)
        glPushMatrix()
        glTranslatef(0, 0, 90)
        glutSolidCube(60)
        glPopMatrix()
        
        # head
        glColor3f(0, 0, 0)
        glPushMatrix()
        glTranslatef(0, 0, 150)
        gluSphere(gluNewQuadric(), 25, 10, 10)  # parameters are: quadric, radius, slices, stacks
        glPopMatrix()
        
        # left leg
        glColor3f(0, 0, 1)
        glPushMatrix()
        glTranslatef(-20, -15, 0)
        gluCylinder(gluNewQuadric(), 7, 12, 60, 10, 10)
        glPopMatrix()
        
        # right leg
        glColor3f(0, 0, 1)
        glPushMatrix()
        glTranslatef(-20, 15, 0)
        gluCylinder(gluNewQuadric(), 7, 12, 60, 10, 10)
        glPopMatrix()
        
        # gun
        glColor3f(0.753, 0.753, 0.753)
        glPushMatrix()
        glTranslatef(0, 0, 100)
        glRotatef(-90, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 12, 7, 80, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
        glPopMatrix()
        
        # left hand
        glColor3f(1, 0.878, 0.741)
        glPushMatrix()
        glTranslatef(-20, -15, 100)
        glRotatef(-90, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 10, 6, 30, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
        glPopMatrix()
        
        # right hand
        glColor3f(1, 0.878, 0.741)
        glPushMatrix()
        glTranslatef(-20, 15, 100)
        glRotatef(-90, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 10, 6, 30, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
        glPopMatrix()
    
    glPopMatrix()

def lay_down_player():
    """Draws the player laying down on the floor after game over"""
    glPushMatrix()
    glTranslatef(character_pos[0], character_pos[1], character_pos[2])  # Position the character
    
    # Body - rotated to lay flat on ground
    glColor3f(0.333, 0.42, 0.184)
    glPushMatrix()
    glTranslatef(0, 0, 30)  # Lower height since laying down
    glRotatef(90, 1, 0, 0)  # Rotate 90 degrees around x-axis to lay flat
    glutSolidCube(60)
    glPopMatrix()
    
    # Head - positioned to side of body
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, -50, 30)  # Position head next to body
    gluSphere(gluNewQuadric(), 25, 10, 10)
    glPopMatrix()
    
    # Left leg - extended out
    glColor3f(0, 0, 1)
    glPushMatrix()
    glTranslatef(-20, 30, 15)  # Position at one end of body
    glRotatef(-90, 1, 0, 0)  # Rotate to lay flat
    gluCylinder(gluNewQuadric(), 12, 7, 60, 10, 10)
    glPopMatrix()
    
    # Right leg - extended out
    glColor3f(0, 0, 1)
    glPushMatrix()
    glTranslatef(20, 30, 15)  # Position at one end of body
    glRotatef(-90, 1, 0, 0)  # Rotate to lay flat
    gluCylinder(gluNewQuadric(), 12, 7, 60, 10, 10)
    glPopMatrix()
    
    # Gun - pointing upward perpendicular to floor
    glColor3f(0.753, 0.753, 0.753)
    glPushMatrix()
    glTranslatef(0, 0, 30)  # Position at middle of body
    gluCylinder(gluNewQuadric(), 12, 7, 80, 10, 10)  # Pointing straight up
    glPopMatrix()
    
    # Left hand - following gun direction, upward
    glColor3f(1, 0.878, 0.741)
    glPushMatrix()
    glTranslatef(-20, 0, 30)  # Start at side of body
    glRotatef(-10, 0, 1, 0)  # Angle toward gun
    #glRotatef(90, 1, 0, 0)  # Point upward
    gluCylinder(gluNewQuadric(), 10, 6, 60, 10, 10)
    glPopMatrix()
    
    # Right hand - following gun direction, upward
    glColor3f(1, 0.878, 0.741)
    glPushMatrix()
    glTranslatef(20, 0, 30)  # Start at other side of body
    glRotatef(10, 0, 1, 0)  # Angle toward gun
    #glRotatef(90, 1, 0, 0)  # Point upward
    gluCylinder(gluNewQuadric(), 10, 6, 60, 10, 10)
    glPopMatrix()
    
    glPopMatrix()
    
def draw_bullets():
    for bullet in bullets:
        if bullet['active']:
            glPushMatrix()
            glTranslatef(bullet['position'][0], bullet['position'][1], bullet['position'][2])
            
            # Change bullet color in cheat mode
            if bullet.get('homing', False):
                glColor3f(1, 0, 0)
            else:
                glColor3f(1, 0, 0)  # Red for normal bullets
                
            glutSolidCube(bullet_size)
            glPopMatrix()

def draw_enemies():
    global enemy_positions, enemy_scales
    
    for i, pos in enumerate(enemy_positions):
        current_scale = enemy_scales[i]
        
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        glScalef(current_scale, current_scale, current_scale)
        
        # body
        glColor3f(1, 0, 0)
        gluSphere(gluNewQuadric(), 60, 10, 10)
        
        # head
        glColor3f(0, 0, 0)
        glTranslatef(0, 0, 70)
        gluSphere(gluNewQuadric(), 30, 10, 10)
        
        glPopMatrix()

def showScreen():
    """
    Display function to render the game scene
    """
    global score, bullets_missed, life, game_over, is_first_person, camera_angle, cheat_mode, follow_gun_view
    
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()
    
    game_floor()
    floor_boundary()
    
    if game_over == False:
        player()
    elif game_over == True:
        lay_down_player()
    
    draw_bullets()
    draw_enemies()
    
    if game_over == False:
        # Display game status text
        draw_text(10, 770, f"Game Score: {score}")
        draw_text(10, 740, f"Player Bullets Missed: {bullets_missed}/{max_bullets_missed}")
        draw_text(10, 710, f"Player Life Remaining: {life}/5")
        
        # Display cheat mode status
        if cheat_mode:
            draw_text(10, 680, "CHEAT MODE: ON (C to toggle)")
        else:
            draw_text(10, 680, "CHEAT MODE: OFF (C to toggle)")
        
        if is_first_person:
            draw_text(10, 650, "FIRST PERSON MODE: ON (Right Click to toggle)")
        else:
            draw_text(10, 650, "FIRST PERSON MODE: OFF (Right Click to toggle)")
        
    if game_over:
        draw_text(400, 400, "GAME OVER")
        draw_text(350, 370, "Press 'R' to restart")
        draw_text(10, 770, f"Game is Over: Your Score is {score}.")
        draw_text(10, 740, f"Press 'R' to RESTART the Game")
        
    glutSwapBuffers()

def initGL():
    """Initialize OpenGL settings"""
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Set background color to black
    glEnable(GL_DEPTH_TEST)  # Enable depth testing

# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"Bullet Frenzy")  # Create the window

    initGL()  # Initialize OpenGL settings
    
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function for game updates

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()