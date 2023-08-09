from math import cos, sin, radians
from sys import argv
class Projectile:

    def __init__(self, mass, x_coord):
        self.mass = mass
        self.x = x_coord
        self.y = 0

    def move(self, time, angle, initial_speed):
        g = 9.8
        angle_rad = radians(angle)
        self.x = initial_speed * cos(angle_rad) * time
        self.y = initial_speed * sin(angle_rad) * time - (1 / 2 * g) * (time ** 2)

    def shoot(self, angle, initial_speed):
        time = 0
        while True:
            print(f'{self.x}    {self.y}')
            time += 0.1
            self.move(time, angle, initial_speed)

            if self.y <= 0:
                break


angle =int(input('Input angle in degrees:'))
speed = int(input('Input initial speed:'))

Shell = Projectile(1,0)
Shell.shoot(angle, speed)