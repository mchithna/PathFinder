import pygame
from settings import *

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont('Segoe UI, Helvetica Neue, Arial', 18, bold=True)

        self.shadow_rect = pygame.Rect(x + 2, y + 4, width, height)


    def draw(self, screen, is_active=False):
        # button hovering effect
        mouse_pos = pygame.mouse.get_pos()

        if is_active:
            color = ACTIVE_BUTTON_COLOUR
            text_color = ACTIVE_TEXT_COLOUR
        elif self.rect.collidepoint(mouse_pos):
            color = BUTTON1H_COLOUR
            text_color = TEXT_COLOUR
        else:
            color = BUTTON1_COLOUR
            text_color = TEXT_COLOUR
        
        # draw the drop shadow
        pygame.draw.rect(screen, BUTTON_SHADOW, self.shadow_rect, border_radius=6)

        # draw the rounded button
        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        
        # draw border
        pygame.draw.rect(screen, BUTTON1H_COLOUR, self.rect, 2, border_radius=6) 


        # 4. Draw the text 
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        # check if the left mouse is clicked 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                if self.rect.collidepoint(event.pos):
                    return True
        return False

def draw_sidebar(screen):
    # draw a background
    rect = pygame.Rect(MAZE_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT)
    pygame.draw.rect(screen, SIDEBAR_COLOUR, rect)

    pygame.draw.line(screen, BUTTON1_COLOUR, (MAZE_WIDTH, 0), (MAZE_WIDTH, HEIGHT), 2)