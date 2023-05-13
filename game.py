import pygame
import random
from network import Network


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.imageWidth = 75
        self.imageHeight = 10
        self.image = pygame.Surface((self.imageWidth, self.imageHeight))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedX = 10

    # #def update(self):
    #     width = 1080
    #     height = 720
    #     keyState = pygame.key.get_pressed()
    #     if keyState[pygame.K_LEFT]:
    #         self.rect.x -= self.speedX
    #     if keyState[pygame.K_RIGHT]:
    #         self.rect.x += self.speedX
    #     if self.rect.x > width-self.imageWidth:
    #         self.rect.x = width-75
    #     if self.rect.x < 0:
    #         self.rect.x = 0


class Canvas:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("NowOnlineS!")
        self.screen.fill((255, 255, 255))

    @staticmethod
    def update():
        pygame.display.update()
        pygame.display.flip()

    def getCanvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((0, 0, 0))


class Ball(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.radius = 10
        pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)
        self.rect.x = width / 2
        self.rect.y = 500
        self.speedX = 0
        self.speedList = [-10, 10]
        self.speedY = random.choice(self.speedList)

    def update(self):
        width = 1080
        height = 720
        self.rect.x += self.speedX
        self.rect.y += self.speedY
        if self.rect.x >= width-50:
            self.speedX *= -1
        elif self.rect.x <= 0:
            self.speedX *= -1

    def collide_with_player1(self, centerCoordinate):
        ballCenter = self.rect.center[0]
        if -5 <= centerCoordinate - ballCenter <= 5:
            self.speedX = 0
            self.speedY *= -1
        if 16.25 < centerCoordinate - ballCenter < 50:
            self.speedX = -4
            self.speedY *= -1
        if 5 < centerCoordinate - ballCenter < 16.25:
            self.speedX = -2
            self.speedY *= -1
        if -50 < centerCoordinate - ballCenter < -16.25:
            self.speedX = 4
            self.speedY *= -1
        if -16.25 < centerCoordinate - ballCenter < -5:
            self.speedX = 2
            self.speedY *= -1

    def collide_with_player2(self, centerCoordinate):
        ballCenter = self.rect.center[0]
        if -5 <= centerCoordinate - ballCenter <= 5:
            self.speedX = 0
            self.speedY *= -1
        if 16.25 < centerCoordinate - ballCenter < 50:
            self.speedX = -4
            self.speedY *= -1
        if 5 < centerCoordinate - ballCenter < 16.25:
            self.speedX = -2
            self.speedY *= -1
        if -50 < centerCoordinate - ballCenter < -16.25:
            self.speedX = 4
            self.speedY *= -1
        if -16.25 < centerCoordinate - ballCenter < -5:
            self.speedX = 2
            self.speedY *= -1


class Game:

    def __init__(self, width, height):
        self.net = Network()
        self.width = width
        self.height = height
        self.player1 = Player(width/2, height-10)
        self.player2 = Player(width/2, 0)
        self.ball = Ball(width, height)
        self.canvas = Canvas(width, height)
        self.all_sprites = pygame.sprite.Group()
        self.player1Group = pygame.sprite.Group()
        self.player2Group = pygame.sprite.Group()
        self.player1Group.add(self.player1)
        self.player2Group.add(self.player2)
        self.all_sprites.add(self.ball)
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)

    def run(self):

        clock = pygame.time.Clock()
        running = True
        while running:
            '''events'''
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            '''updating'''
            keyState = pygame.key.get_pressed()
            if keyState[pygame.K_LEFT]:
                self.player1.rect.x -= self.player1.speedX
            if keyState[pygame.K_RIGHT]:
                self.player1.rect.x += self.player1.speedX
            if self.player1.rect.x > self.width - self.player1.imageWidth:
                self.player1.rect.x = self.width - 75
            if self.player1.rect.x < 0:
                self.player1.rect.x = 0

            if (self.ball.rect.y > 730) or (self.ball.rect.y < -20):
                running = False
            self.player1.update()
            if pygame.sprite.spritecollide(self.ball, self.player1Group, False):
                self.ball.collide_with_player1(self.player1.rect.center[0])
            if pygame.sprite.spritecollide(self.ball, self.player2Group, False):
                self.ball.collide_with_player2(self.player2.rect.center[0])
            temp = 0
            #self.ball.update()
            self.player2.rect.x, self.ball.rect.x, self.ball.rect.y = self.parseData(self.send_data())
            self.ball.update()
            # print(self.parseData(self.send_data()))
            # self.player2.rect.x = self.parseData(self.send_data())[0]
            '''visualising'''
            self.canvas.draw_background()
            self.all_sprites.draw(self.canvas.getCanvas())
            self.canvas.update()
        
        pygame.quit()

    def send_data(self):
        data = str(self.net.id) + ":" + str(self.player1.rect.x) + "," + str(self.ball.rect.x) + "," + str(self.ball.rect.y)
        print(data)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parseData(data):
        try:
            #print(data)
            d = data.split(":")[1].split(",")
           # print(d[2])
            return int(d[0]), int(d[1]), int(d[2])

        except:
            return 0, 0
