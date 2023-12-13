import pygame
import sys
import numpy as np

# 초기화
pygame.init()

# 화면 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("OBB Collision Detection")

# 색깔 정의
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# OBB 충돌 검사 함수 수정
def check_collision(shape1, shape2):
    if hasattr(shape1, 'get_obb_rect') and hasattr(shape2, 'get_obb_rect'):
        obb_rect1 = shape1.get_obb_rect()
        obb_rect2 = shape2.get_obb_rect()
        return obb_rect1.colliderect(obb_rect2)
    elif hasattr(shape1, 'points') and hasattr(shape2, 'points'):
        poly1 = pygame.draw.polygon(screen, (0, 0, 0), shape1.points, 0)
        poly2 = pygame.draw.polygon(screen, (0, 0, 0), shape2.points, 0)
        return poly1.colliderect(poly2)
    return False

# 도형 클래스 정의
class Shape:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.selected = False
        self.velocity = [0, 0]

    def draw(self):
        pass

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def get_obb_rect(self):
        return pygame.Rect(self.x, self.y, 0, 0)

# 사각형 클래스
class Rectangle(Shape):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, color)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, 0)

    def update(self):
        super().update()
        self.rect.topleft = (self.x, self.y)

    def get_obb_rect(self):
        rotated_rect = pygame.Rect(0, 0, self.width, self.height)
        rotated_rect.center = self.rect.center
        return rotated_rect

# 원 클래스
class Circle(Shape):
    def __init__(self, x, y, radius, color, mass=1.0):
        super().__init__(x, y, color)
        self.radius = radius
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.mass = mass

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)

    def update(self):
        super().update()
        self.rect.topleft = (self.x - self.radius, self.y - self.radius)

    def get_obb_rect(self):
        return self.rect

# 삼각형 클래스
class Triangle(Shape):
    def __init__(self, x, y, side_length, color):
        super().__init__(x, y, color)
        self.side_length = side_length
        self.angle = 0 
        self.points = self.calculate_triangle_points()

    def draw(self):
        pygame.draw.polygon(screen, self.color, self.points, 0)

    def update(self):
        super().update()
        self.points = self.calculate_triangle_points()

    def calculate_triangle_points(self):
        angle_rad = np.radians(self.angle)
        x1 = self.x
        y1 = self.y - self.side_length // 2

        x2 = self.x - int(self.side_length * np.cos(angle_rad))
        y2 = self.y + self.side_length // 2

        x3 = self.x + int(self.side_length * np.cos(angle_rad))
        y3 = y2

        return [(x1, y1), (x2, y2), (x3, y3)]

    def get_obb_rect(self):
        rotated_points = self.rotate_points()
        x_values, y_values = zip(*rotated_points)
        min_x, max_x = min(x_values), max(x_values)
        min_y, max_y = min(y_values), max(y_values)
        return pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def rotate_points(self):
        angle_rad = np.radians(self.angle)
        rotated_points = []
        for x, y in [(self.x, self.y - self.side_length // 2),
                     (self.x - int(self.side_length * np.cos(angle_rad)), self.y + self.side_length // 2),
                     (self.x + int(self.side_length * np.cos(angle_rad)), self.y + self.side_length // 2)]:
            rotated_x = self.x + (x - self.x) * np.cos(angle_rad) - (y - self.y) * np.sin(angle_rad)
            rotated_y = self.y + (x - self.x) * np.sin(angle_rad) + (y - self.y) * np.cos(angle_rad)
            rotated_points.append((rotated_x, rotated_y))
        return rotated_points

# 오각형 클래스
class Pentagon(Shape):
    def __init__(self, x, y, side_length, color):
        super().__init__(x, y, color)
        self.side_length = side_length
        self.angle = 0 
        self.points = self.calculate_pentagon_points()

    def draw(self):
        pygame.draw.polygon(screen, self.color, self.points, 0)

    def update(self):
        super().update()
        self.points = self.calculate_pentagon_points()

    def calculate_pentagon_points(self):
        angle_offset = np.radians(72)
        points = []
        for i in range(5):
            angle = i * angle_offset + np.radians(self.angle)
            x = self.x + int(self.side_length * np.cos(angle))
            y = self.y + int(self.side_length * np.sin(angle))
            points.append((x, y))
        return points

    def get_obb_rect(self):
        rotated_points = self.rotate_points()
        x_values, y_values = zip(*rotated_points)
        min_x, max_x = min(x_values), max(x_values)
        min_y, max_y = min(y_values), max(y_values)
        return pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def rotate_points(self):
        angle_rad = np.radians(self.angle)
        rotated_points = []
        for i in range(5):
            x, y = self.calculate_pentagon_points()[i]
            rotated_x = self.x + (x - self.x) * np.cos(angle_rad) - (y - self.y) * np.sin(angle_rad)
            rotated_y = self.y + (x - self.x) * np.sin(angle_rad) + (y - self.y) * np.cos(angle_rad)
            rotated_points.append((rotated_x, rotated_y))
        return rotated_points

# 메인 루프
clock = pygame.time.Clock()

# 도형 생성
rectangles = [Rectangle(50, 50, 50, 50, black),
              Rectangle(200, 100, 60, 40, black),
              Rectangle(400, 150, 80, 60, black)]

circles = [Circle(100, 300, 30, black, mass=1.0),
           Circle(300, 400, 40, black, mass=1.0),
           Circle(500, 300, 50, black, mass=1.0)]

triangles = [Triangle(150, 150, 50, black),
             Triangle(300, 250, 60, black),
             Triangle(500, 150, 70, black)]

pentagons = [Pentagon(150, 400, 40, black),
             Pentagon(300, 500, 50, black),
             Pentagon(500, 400, 60, black)]

shapes = rectangles + circles + triangles + pentagons

# 랜덤 속도 설정
for shape in shapes:
    shape.velocity = [np.random.randint(-5, 5), np.random.randint(-5, 5)]

selected_shape = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for shape in shapes:
                if hasattr(shape, 'get_obb_rect') and shape.get_obb_rect().collidepoint(event.pos):
                    selected_shape = shape
                    selected_shape.selected = True
                    selected_shape.dragging = True
                    selected_shape.offset_x = event.pos[0] - selected_shape.x
                    selected_shape.offset_y = event.pos[1] - selected_shape.y
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_shape:
                selected_shape.selected = False
                selected_shape.dragging = False
                selected_shape = None
        elif event.type == pygame.MOUSEMOTION:
            if selected_shape and selected_shape.dragging:
                selected_shape.x = event.pos[0] - selected_shape.offset_x
                selected_shape.y = event.pos[1] - selected_shape.offset_y

    screen.fill(white)

    for shape in shapes:
        shape.update()
        shape.draw()
        if hasattr(shape, 'get_obb_rect'):
            pygame.draw.rect(screen, red, shape.get_obb_rect(), 2)

    # OBB 충돌 검사 및 튕겨나가기
    for i in range(len(shapes)):
        for j in range(i + 1, len(shapes)):
            shape1 = shapes[i]
            shape2 = shapes[j]
            if check_collision(shape1, shape2):
                dx = shape2.x - shape1.x
                dy = shape2.y - shape1.y
                angle = np.arctan2(dy, dx)
                speed1 = np.sqrt(shape1.velocity[0]**2 + shape1.velocity[1]**2)
                speed2 = np.sqrt(shape2.velocity[0]**2 + shape2.velocity[1]**2)

                new_speed1_x = speed2 * np.cos(angle)
                new_speed1_y = speed2 * np.sin(angle)
                new_speed2_x = speed1 * np.cos(angle + np.pi)
                new_speed2_y = speed1 * np.sin(angle + np.pi)

                shape1.velocity[0] = -new_speed1_x
                shape1.velocity[1] = -new_speed1_y
                shape2.velocity[0] = -new_speed2_x
                shape2.velocity[1] = -new_speed2_y

    # 화면 밖으로 나가지 않도록
    for shape in shapes:
        if shape.x < 0 or shape.x > width:
            shape.velocity[0] *= -1
        if shape.y < 0 or shape.y > height:
            shape.velocity[1] *= -1

    pygame.display.flip()
    clock.tick(60)