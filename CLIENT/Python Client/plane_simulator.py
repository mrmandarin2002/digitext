import pygame, math
import font_info
from pygame import gfxdraw

pygame.init()

window_resolution_x = 1280
window_resolution_y = 720

class game():

    is_running = True
    buddy_created = False

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_p] and not self.buddy_created):
            self.buddy_created = True
            self.world.add_object(controller = self, obj = buddy(self))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def update(self):
        self.world.update_world(self)
        self.world.update_collisions(self)

    def draw(self):
        self.game_window.fill(font_info.BLACK)
        self.world.draw_objects(self)
        pygame.display.update()

    def __init__ (self, resolution_x, resolution_y):

        self.resolution_x = resolution_x
        self.resolution_y = resolution_y
        self.game_window = pygame.display.set_mode([1280, 720])
        pygame.display.set_caption("Interactive Kelsch")

        self.world = world(self)
        self.buddy = buddy(self)
        self.clock = pygame.time.Clock()
        while(self.is_running):
            #IMPORTANT!
            self.dt = self.clock.tick(60)
            self.dt = 1 / float(self.dt)
            self.handle_events()
            self.update()
            self.draw()

class world():

    land_height = 600
    land_thickness = 10
    land_color = font_info.WHITE
    gravity = 9.8

    objects = []

    def draw_objects(self, controller):
        for cnt, obj in enumerate(self.objects):
            obj.draw(controller)

    def update_world(self, controller):
        #print(self.objects)
        for cnt, obj in enumerate(self.objects):
            obj.update(controller)

    def update_collisions(self, controller):
        for cnt, obj1 in enumerate(self.objects):
            for x in range(cnt + 1, len(self.objects)):
                obj2 = self.objects[x];
                if(self.check_collision(obj1, obj2)):
                    pass

    def check_collision(self, obj1, obj2):
        #if both objects are circles
        if(obj1.is_circle and obj2.is_circle):
            if(math.sqrt(abs(obj1.pos_x - obj2.pos_x) ** 2 + abs(obj1.pos_y - obj2.pos_y) ** 2) < obj1.radius + obj2.radius):
                print("CIRCLE COLLISION!")
                return True
        else:
            if(obj1.Left < obj2.Right and obj1.Right > obj2.Left and obj1.Top < obj2.Bottom and obj1.Bottom > obj2.Top):
                print("REGULAR COLLISION!")
                return True

    def add_object(self, controller, obj):
        self.objects.append(obj)

    def __init__(self, controller):
        self.add_object(controller, land(controller))

class land():

    mobility = False
    land_height = 600
    land_thickness = 20
    land_color = font_info.WHITE        
    velocity_x = 0
    velocity_y = 0
    mass = 1000000
    elastic = True
    k_coefficient = 100
    left_bound = 0
    Left = 0
    Right = 0
    Top = 0
    Bottom = 0
    initialized = False
    is_circle = False

    def draw(self, controller):
        pygame.draw.lines(controller.game_window, self.land_color, False, ((0, self.land_height), (window_resolution_x, self.land_height)), self.land_thickness)

    def update(self, controller):
        if(not self.initialized):
            self.initialized = True
            self.Left = 0
            self.Right = window_resolution_x
            self.Top = self.land_height
            self.Bottom = self.land_height + self.land_thickness

    def __init__ (self, controller):
        self.update( controller)
        print("LAND CREATED!")

class buddy():

    pos_x = window_resolution_x / 2
    pos_y = 100
    velocity_x = 0
    velocity_y = 0
    radius = 15
    mass = 100
    elastic = False
    Left = 0
    Right = 0
    Top = 0
    Bottom = 0
    is_circle = True

    def draw(self, controller):
        pygame.gfxdraw.aacircle(controller.game_window, int(self.pos_x), int(self.pos_y), self.radius, font_info.WHITE)
        pygame.gfxdraw.filled_circle(controller.game_window, int(self.pos_x), int(self.pos_y), self.radius, font_info.WHITE)

    def update(self, controller):
        self.velocity_y += world.gravity
        #print(self.velocity_y)
        self.pos_x += self.velocity_x * controller.dt
        self.pos_y += self.velocity_y * controller.dt
        self.Left = self.pos_x - self.radius
        self.Right = self.pos_x + self.radius
        self.Top = self.pos_y - self.radius
        self.Bottom = self.pos_y + self.radius
    
    def __init__ (self, controller):
        print("CREATED!")

interactive_kelsch = game(resolution_x = window_resolution_x, resolution_y = window_resolution_y)

        
