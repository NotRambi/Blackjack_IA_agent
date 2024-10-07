from threading import Thread
import pygame

# IMPOSTAZIONI DI SCHERMO
WIDTH, HEIGHT = 1920, 1080
TITLE_STRING = "Blackjack"
FPS = 60
BG_COLOR = (33, 124, 66)

class Screen:

    def __init__(self):    
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE_STRING)
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.SysFont('rockwellcondensedgrassetto', 40)
        self.table = Tavolo()

    def getTable(self):
        return self.table

    def run(self):

        self.start_time = pygame.time.get_ticks()

        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # altri click qui
            
            self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
            self.start_time = pygame.time.get_ticks()
            pygame.display.update()
            self.screen.fill(BG_COLOR)

            text = self.font.render('P1: 0', True, (255, 255, 255))
            self.screen.blit(text, (60, 670))
            text = self.font.render('P2: 0', True, (255, 255, 255))
            self.screen.blit(text, (285, 870))
            text = self.font.render('P3: 0', True, (255, 255, 255))
            self.screen.blit(text, (585, 940))
            text = self.font.render('P4: 0', True, (255, 255, 255))
            self.screen.blit(text, (885, 970))
            text = self.font.render('P5: 0', True, (255, 255, 255))
            self.screen.blit(text, (1185, 940))
            text = self.font.render('P6: 0', True, (255, 255, 255))
            self.screen.blit(text, (1485, 870))
            text = self.font.render('P7: 0', True, (255, 255, 255))
            self.screen.blit(text, (1710, 670))
            text = self.font.render('D: 0', True, (255, 255, 255))
            self.screen.blit(text, (885, 220))

            self.table.update()
            self.clock.tick(FPS)

class Card:
    def __init__(self, card):
        self.position = (0, 0)
        self.id = card
        self.img = f"assets/cards/{self.id}.png"
        self.card_rotation_angle = 0
        self.card_img = pygame.image.load(self.img)
        self.card_img = pygame.transform.scale(self.card_img, (self.card_img.get_width() * 1.5, self.card_img.get_height() * 1.5))
        self.card_rot = pygame.transform.rotate(self.card_img, self.card_rotation_angle)
        self.card_bounding_rect = self.card_rot.get_bounding_rect()
        self.card_surf = pygame.Surface(self.card_bounding_rect.size, pygame.SRCALPHA)

        # Calculate the position to blit the rotated image onto the surface
        blit_pos = (0, 0)
        self.card_surf.blit(self.card_rot, blit_pos)

class Tavolo:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.cards = []
        self.step = 30
        self.players = ((50, 500), (275, 700), (575, 770), (875, 800), (1175, 770), (1475, 700), (1700, 500))
        self.p_conts = [0,0,0,0,0,0,0]
        self.dealer = (875, 50)
        self.dealer_cont = 0

    def update(self):
    # Draw cards at current positions
        if len(self.cards) > 0:
            for c in self.cards:
                cardtype = c[0]
                card = Card(cardtype)
                pos = c[1]
                cont = c[2]
                self.display_surface.blit(card.card_surf, (pos[0] + cont * self.step, pos[1]))  
                
    def showCards(self, p, c):
        if p == 7:
            pos = self.dealer
            cont = self.dealer_cont
            self.dealer_cont += 1
        else:
            pos = self.players[p]
            cont = self.p_conts[p]
            self.p_conts[p] += 1
        self.cards.append((c, pos, cont))

    def clearTable(self):
        self.cards = []
        self.p_conts = [0,0,0,0,0,0,0]
        self.dealer_cont = 0

def gioco(tavolo):
    while True:
        p = int(input("Inserisci giocatore: "))
        if p == 10:
            tavolo.clearTable()
        c = input("Inserisci carta: ")
        tavolo.showCards(p, c)

if __name__ == '__main__':
    Window = Screen()
    tavolo = Window.getTable()
    t1 = Thread(target=gioco, args=(tavolo,))
    t1.start()
    Window.run()
    