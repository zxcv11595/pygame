import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Simulation")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class SmokeParticle:
    def __init__(self, x, y):
        self.x = x + random.uniform(-10, 10)
        self.y = y
        self.size = random.uniform(10, 30)
        self.lifetime = random.randint(1000, 1500)
        self.speed_y = random.uniform(-0.5, -0.2)
        self.expansion_rate = random.uniform(0.02, 0.05)
        self.wind_speed = 0
        self.wind_variation = random.uniform(-0.1, 0.1)

    def update(self):
        self.y += self.speed_y
        self.x += self.wind_speed + self.wind_variation
        self.size += self.expansion_rate
        self.lifetime -= 1

    def draw(self, surface):
        alpha = max(min(self.lifetime, 150), 0)
        smoke_color = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(smoke_color, (150, 150, 150, alpha), (int(self.size), int(self.size)), int(self.size))
        surface.blit(smoke_color, (int(self.x - self.size), int(self.y - self.size)))

class FireParticle:
    def __init__(self, x, y):
        self.x = x + random.uniform(-10, 10)
        self.y = y + random.uniform(-5, 5)
        self.size = random.randint(15, 30)
        self.lifetime = random.randint(300, 500)
        self.speed_y = random.uniform(-1.5, -0.8)
        self.color = [255, random.randint(100, 180), 0]

    def update(self):
        self.y += self.speed_y
        self.size *= 0.98
        self.lifetime -= 2
        self.color[1] = max(self.color[1] - 2, 0)

    def draw(self, surface):
        alpha = max(min(self.lifetime, 200), 0)
        fire_surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(fire_surface, (255, self.color[1], self.color[2], alpha), (int(self.size), int(self.size)), int(self.size))
        surface.blit(fire_surface, (int(self.x - self.size), int(self.y - self.size)))

class FluidParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-0.1, 0.1)
        self.vy = random.uniform(-0.1, 0.1)
        self.size = 15
        self.mass = 1
        self.pressure = 0
        self.density = 0

    def update(self, particles):
        self.density = 0
        self.pressure = 0
        h = 20
        k_pressure = 200
        k_viscosity = 0.1
        gravity = 0.2

        for particle in particles:
            dist = math.sqrt((self.x - particle.x)**2 + (self.y - particle.y)**2)
            if dist < h and dist > 0:
                q = dist / h
                self.density += (1 - q)**2
        self.pressure = k_pressure * (self.density - 1)
        ax, ay = 0, gravity
        for particle in particles:
            dist = math.sqrt((self.x - particle.x)**2 + (self.y - particle.y)**2)
            if dist < h and dist > 0:
                q = dist / h
                pressure_force = -(self.pressure + particle.pressure) * (1 - q)**2 / (2 * self.density)
                viscosity_force = k_viscosity * (particle.vx - self.vx + particle.vy - self.vy) * (1 - q)
                ax += (pressure_force + viscosity_force) * (self.x - particle.x) / dist
                ay += (pressure_force + viscosity_force) * (self.y - particle.y) / dist
        self.vx += ax * 0.01
        self.vy += ay * 0.01

        self.x = max(100, min(self.x + self.vx, 700))
        self.y = max(100, min(self.y + self.vy, 500)) 
        if self.y >= 500:
            self.vy = 0 
            self.size += 0.1 
        if self.x <= 100 or self.x >= 700:
            self.vx = 0  

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 0, 255), (int(self.x), int(self.y)), int(self.size))

smoke_particles = []
fire_particles = []
fluid_particles = [FluidParticle(random.randint(150, 650), random.randint(150, 200)) for _ in range(300)]

font = pygame.font.Font(None, 36)
def create_button(text, x, y, width, height):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, GRAY, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect

def draw_wind_arrows(surface):
    for i in range(5):
        x = WIDTH - 50 - (i * 100)
        y = HEIGHT // 2
        pygame.draw.polygon(surface, RED, [(x - 20, y), (x, y - 10), (x, y + 10)])

running = True
mode = "smoke"
wind_active = False
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            if smoke_button.collidepoint((mouse_x, mouse_y)):
                mode = "smoke"
                fire_particles.clear()
            elif fire_button.collidepoint((mouse_x, mouse_y)):
                mode = "fire"
                smoke_particles.clear()
            elif fluid_button.collidepoint((mouse_x, mouse_y)):
                mode = "fluid"
            elif wind_button.collidepoint((mouse_x, mouse_y)):
                wind_active = not wind_active

    smoke_button = create_button("Smoke", WIDTH - 200, 50, 150, 50)
    fire_button = create_button("Fire", WIDTH - 200, 120, 150, 50)
    fluid_button = create_button("Fluid", WIDTH - 200, 190, 150, 50)
    wind_button = create_button("Wind", WIDTH - 200, 260, 150, 50)

    if wind_active:
        draw_wind_arrows(screen)

    if mode == "smoke":
        for _ in range(5):
            smoke_particles.append(SmokeParticle(WIDTH // 2, HEIGHT))
    elif mode == "fire":
        for _ in range(10):
            fire_particles.append(FireParticle(WIDTH // 2, HEIGHT))

    if mode == "smoke":
        for particle in smoke_particles[:]:
            particle.wind_speed = -0.5 if wind_active else 0
            particle.update()
        for particle in smoke_particles[:]:
            particle.draw(screen)
            if particle.lifetime <= 0:
                smoke_particles.remove(particle)
    elif mode == "fire":
        for particle in fire_particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                fire_particles.remove(particle)
    elif mode == "fluid":
        for particle in fluid_particles:
            particle.update(fluid_particles)
            particle.draw(screen)

    pygame.display.flip()

pygame.quit()
