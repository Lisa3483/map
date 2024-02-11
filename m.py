import pygame
import requests
from io import BytesIO

api_key = "547a17ec-d32c-4296-b64c-70fc2c5e00ba"
map_api_server = "http://static-maps.yandex.ru/1.x/"
location = "Австралия"
ll_1 = 37.627723
ll_2 = 55.750815
z = 12
l = 'map'
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
pygame.init()
screen = pygame.display.set_mode((800, 550))

running = True


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.text = text

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class SearchButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.text = text

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def search(self, query):
        print("Search query:", query)


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.text = ""

    def draw(self, screen):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=self.rect.topleft)
        screen.blit(self.image, self.rect)
        screen.blit(text_surface, text_rect)

    def add_text(self, char):
        self.text += char

    def delete_text(self):
        self.text = self.text[:-1]


def get_map():
    global ll_1
    global ll_2
    global z
    global map_api_server
    global l
    map_params = {

        "ll": f'{ll_1},{ll_2}',
        "l": l,
        "z": z
    }

    response = requests.get(map_api_server, params=map_params)

    image_data = BytesIO(response.content)
    img = pygame.image.load(image_data)
    screen.blit(img, (0, 0))

    pygame.display.flip()


get_map()
button = Button(600, 0, 200, 100, "смена слоя")
input_box = TextInputBox(0, 450, 600, 100)
search_button = SearchButton(600, 450, 200, 100, "поиск")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                ll_1 += 0.01
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                ll_1 -= 0.01
            elif pygame.key.get_pressed()[pygame.K_UP]:
                ll_2 += 0.01
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                ll_2 -= 0.01
            elif event.key == pygame.K_PAGEUP:
                if z > 1:
                    z -= 1
            elif event.key == pygame.K_BACKSPACE:
                input_box.delete_text()

            elif pygame.key.get_pressed()[pygame.K_PAGEDOWN]:
                if z < 21:
                    z += 1
            else:
                input_box.add_text(event.unicode)
            get_map()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button.rect.collidepoint(event.pos):
                if l == 'map':
                    l = 'sat'
                elif l == 'sat':
                    l == 'hybrid'
                else:
                    l == 'map'
            elif search_button.rect.collidepoint(event.pos):
                search_button.search(input_box.text)

            get_map()
    button.draw(screen)
    input_box.draw(screen)
    search_button.draw(screen)
    pygame.display.flip()

pygame.quit()
