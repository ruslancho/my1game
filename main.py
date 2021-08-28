"""
my github: https://github.com/ruslancho
my email: r.melkovskiy@ukr.net
"""

import pygame

#розмір ігрового поля
gameArea = (700, 399)

#ініціалізація вікна
pygame.init()

#встановлюємо розмір ігрового поля
win = pygame.display.set_mode(gameArea)

#встановлюємо надпис на вікні
pygame.display.set_caption('My1Game')

#створюємо список з спрайтів в право
walkRight = [pygame.image.load('img/right_1.png'), pygame.image.load('img/right_2.png'), pygame.image.load('img/right_3.png'), pygame.image.load('img/right_4.png'), pygame.image.load('img/right_5.png'), pygame.image.load('img/right_6.png')]

#створюємо список з спрайтів в ліво
walkLeft = [pygame.image.load('img/left_1.png'), pygame.image.load('img/left_2.png'), pygame.image.load('img/left_3.png'), pygame.image.load('img/left_4.png'), pygame.image.load('img/left_5.png'), pygame.image.load('img/left_6.png')]

#об'являємо задній фон
bg = pygame.image.load('img/background.jpg')

#спрайт гравця при створенні гри
playerStand = pygame.image.load('img/def.png')


clock = pygame.time.Clock()

#опції гравця
width = 60
height = 80
speed = 5

#позиція гравця при ініціалізації ігрового поля
x = 5
y = gameArea[1] - height - 25

#значення при ініціалізаці ігрового поля
isJump = False #за замовчуванням гравець не пригає
jumpCountMax = 10 #максимальна висота прижка гравця
jumpCountMin = -10 #мінімальна висота прижка гравця
Jump = 1
right = False #поворот гравця
left = False #поворот гравця
animCount = 0

run = True #True - гра триває, False - гра закривається

bullets = [] #створюєм порожній список пуль
lastMove = "right" #дефолтове значення напрямку стрільби гравця


def playerJumpDown(jumpCountMax):
    global y
    y += (jumpCountMax ** 2) / 2

def playerJumpUp(jumpCountMax):
    global y
    y -= (jumpCountMax ** 2) / 2

class snaryad():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

def drawWindow():
    global animCount

    win.blit(bg, (0, 0))

    if animCount + 1 >= 30:
        animCount = 0

    if left:
        win.blit(walkLeft[animCount // 5], (x, y))
        animCount += 1
    elif right:
        win.blit(walkRight[animCount // 5], (x, y))
        animCount += 1
    else:
        win.blit(playerStand, (x, y))

    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update() #оновлення вікна гри


while run:
    clock.tick(30)

    pygame.time.delay(50) #затримка циклу

    for event in pygame.event.get(): #перебираєм pygame.event.get()
        if event.type == pygame.QUIT: #якщо event.type довінює pygame.QUIT
            run = False #змінній run присвоюємо значення False, при наступній ітерації циклу гра завершиться

    for bullet in bullets:
        if bullet.x < gameArea[0] and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed() #отримання списка нажатих кнопок

    if keys[pygame.K_f]: #якщо нажата кнопка "f"

        if lastMove == 'right':
            facing = 1
        else:
            facing = -1

        if len(bullets) < 5: #якщо кількість куль менше 5
            bullets.append(snaryad(round(x + width // 2), round(y + height // 2), 5, (255, 0, 0), facing)) #додаємо ще одну кулю

    #переміщення гравця
    if keys[pygame.K_LEFT] and x > 5: #якщо натиснута клавиша "стрілка в ліво" і позиція гравця більше 5
        x -= speed #переміщаємо гравця по координаті x вліво на значення змінної 'speed'
        left = True #гравець повернутий вліво
        right = False #не в право
        lastMove = "left" #останній раз повернутий вліво
    elif keys[pygame.K_RIGHT] and x < gameArea[0] - width - 5: # #якщо натиснута клавиша "стрілка в право" і позиція гравця менше gameArea[0] - width - 5
        x += speed #переміщаємо гравця по координаті x вправо на значення змінної 'speed'
        left = False #гравець повернутий вправо
        right = True #не вліво
        lastMove = "right" #останній раз повернутий вправо
    else:
        right = False
        left = False
        animcount = 0
        lastMove = "right"
    if not(isJump):
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCountMax >= jumpCountMin:
            if jumpCountMax < 0:
                playerJumpDown(jumpCountMax)
            elif jumpCountMax > jumpCountMin:
                playerJumpUp(jumpCountMax)
            jumpCountMax -= 1
        elif jumpCountMax == -11:
            jumpCountMax = 6
            jumpCountMin = -6
            jump = 2
        elif jump == 2:
            jumpCountMax = 3
            jumpCountMin = -3
            jump = 1
        else:
            isJump = False
            jumpCountMax = 10
            jumpCountMin = -10
    drawWindow()
pygame.quit()
