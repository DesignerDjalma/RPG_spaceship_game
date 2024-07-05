from typing import Callable, List, Tuple
import pygame
import sys
from typing import Optional
from pygame import Surface, font


class Button:
    def __init__(
        self,
        image: Optional[Surface],
        pos: tuple[int, int],
        text_input: str,
        font: font.Font,
        base_color: tuple[int, int, int] | str,
        hovering_color: tuple[int, int, int] | str,
    ) -> None:
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.center_pos = (self.x_pos, self.y_pos)
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.font = font
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=self.center_pos)
        self.text_rect = self.text.get_rect(center=self.center_pos)

    def update(self, screen: Surface) -> None:
        """Blit the button text or image to the screen."""
        if self.image:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, m_pos: tuple[int, int]) -> bool:
        """Return True if mouse position is over the button, else False."""
        if self.rect.collidepoint(m_pos):
            return True
        return False

    def changeColor(self, m_pos: tuple[int, int]) -> None:
        """Change the button's text color when the mouse hovers over it."""
        if self.rect.collidepoint(m_pos):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


pygame.init()
SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test Interface")
FONT = pygame.font.SysFont("Courier", 25)
BGC = (33, 33, 33)


def createButton(list_names: list, m_pos) -> List[Tuple[Button, Callable[[], None]]]:
    list_btns = []
    for idx, btn in enumerate(list_names):
        my_btn = Button(
            image=None,
            pos=(400, 250 + idx * 40),
            text_input=btn[0],
            font=FONT,
            base_color="White",
            hovering_color="Green",
        )
        my_btn.changeColor(m_pos)
        my_btn.update(SCREEN)
        list_btns.append((my_btn, btn[1]))
    return list_btns


def menu_new_game():
    while True:
        SCREEN.fill(BGC)
        new_game_text = FONT.render("Novo Jogo", True, "White")
        new_game_rect = new_game_text.get_rect(center=(400, 300))
        SCREEN.blit(new_game_text, new_game_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Volta ao menu principal

        pygame.display.update()


def menu_continue():
    while True:
        SCREEN.fill(BGC)
        continue_text = FONT.render("Continuar", True, "White")
        continue_rect = continue_text.get_rect(center=(400, 300))
        SCREEN.blit(continue_text, continue_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Volta ao menu principal

        pygame.display.update()


def config_controls():
    while True:
        SCREEN.fill(BGC)
        controls_text = FONT.render("Configurações de Controles", True, "White")
        controls_rect = controls_text.get_rect(center=(400, 300))
        SCREEN.blit(controls_text, controls_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()


def config_screen():
    while True:
        SCREEN.fill(BGC)
        screen_text = FONT.render("Configurações de Tela", True, "White")
        screen_rect = screen_text.get_rect(center=(400, 300))
        SCREEN.blit(screen_text, screen_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()


def config_audio():
    while True:
        SCREEN.fill(BGC)
        audio_text = FONT.render("Configurações de Áudio", True, "White")
        audio_rect = audio_text.get_rect(center=(400, 300))
        SCREEN.blit(audio_text, audio_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()


def config_graphics():
    while True:
        SCREEN.fill(BGC)
        graphics_text = FONT.render("Configurações de Gráficos", True, "White")
        graphics_rect = graphics_text.get_rect(center=(400, 300))
        SCREEN.blit(graphics_text, graphics_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()


def menu_config():
    while True:
        m_pos = pygame.mouse.get_pos()
        SCREEN.fill(BGC)
        config_text = FONT.render("Configurações", True, "White")
        config_rect = config_text.get_rect(center=(400, 100))
        SCREEN.blit(config_text, config_rect)

        btns = createButton(
            [
                ("Controles", config_controls),
                ("Tela", config_screen),
                ("Áudio", config_audio),
                ("Gráficos", config_graphics),
            ],
            m_pos,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Volta ao menu principal
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    if btn[0].checkForInput(m_pos):
                        btn[1]()  # Chama a função associada ao botão

        pygame.display.update()


def menu_about():
    while True:
        SCREEN.fill(BGC)
        about_text = FONT.render("Sobre", True, "White")
        about_rect = about_text.get_rect(center=(400, 300))
        SCREEN.blit(about_text, about_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Volta ao menu principal

        pygame.display.update()


def menu_quit():
    pygame.quit()
    sys.exit()


def menu():
    while True:
        m_pos = pygame.mouse.get_pos()
        SCREEN.fill(BGC)
        menu_text = FONT.render("ESSE É O MENU", True, "White")
        menu_rect = menu_text.get_rect(center=(400, 100))
        SCREEN.blit(menu_text, menu_rect)

        btns = createButton(
            [
                ("Iniciar Novo Jogo", menu_new_game),
                ("Continuar", menu_continue),
                ("Configurações", menu_config),
                ("Sobre", menu_about),
                ("Quit", menu_quit),
            ],
            m_pos,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    if btn[0].checkForInput(m_pos):
                        btn[1]()  # Chama a função associada ao botão

        pygame.display.update()


if __name__ == "__main__":
    menu()
