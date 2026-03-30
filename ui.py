import pygame
from settings import *

class Button:
    def __init__(self, x, y, width, height, text, sub_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.sub_text = sub_text
        # fonts
        self.font = pygame.font.SysFont('Segoe UI, Helvetica Neue, Arial', 18, bold=True)
        self.sub_font = pygame.font.SysFont(['poppins', 'segoe ui', 'helvetica', 'arial'], 11, bold=True)

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


        # 4. draw the 2 lines of text 
        if self.sub_text:
            text_surf = self.font.render(self.text, True, text_color)
            sub_surf = self.sub_font.render(self.sub_text, True, text_color)
            
            # center the text
            text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery - 8))
            sub_rect = sub_surf.get_rect(center=(self.rect.centerx, self.rect.centery + 10))
            
            screen.blit(text_surf, text_rect)
            screen.blit(sub_surf, sub_rect)
        else:
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

class SteppedSlider:
    def __init__(self, x, y, width, height, options, start_index):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options 
        self.index = start_index
        self.font = pygame.font.SysFont('Segoe UI, Helvetica Neue, Arial', 16, bold=True)
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, BUTTON1_COLOUR, self.rect, border_radius=self.rect.height//2)
        
        step_width = self.rect.width / (len(self.options) - 1)
        thumb_x = self.rect.x + (self.index * step_width)
        thumb_rect = pygame.Rect(thumb_x - 10, self.rect.y - 8, 20, self.rect.height + 16)
        
        pygame.draw.rect(screen, BUTTON_SHADOW, (thumb_rect.x + 2, thumb_rect.y + 2, thumb_rect.width, thumb_rect.height), border_radius=5)
        pygame.draw.rect(screen, ACTIVE_BUTTON_COLOUR, thumb_rect, border_radius=5)
        
        text_surf = self.font.render(self.options[self.index][0], True, TEXT_COLOUR)
        screen.blit(text_surf, (self.rect.x + self.rect.width + 20, self.rect.y - 6))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            step_width = self.rect.width / (len(self.options) - 1)
            thumb_x = self.rect.x + (self.index * step_width)
            thumb_rect = pygame.Rect(thumb_x - 10, self.rect.y - 8, 20, self.rect.height + 16)
            
            if self.rect.collidepoint(event.pos) or thumb_rect.collidepoint(event.pos):
                self.dragging = True
                self.update_index(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_index(event.pos[0])

    def update_index(self, mouse_x):
        rel_x = mouse_x - self.rect.x
        rel_x = max(0, min(rel_x, self.rect.width))
        step_width = self.rect.width / (len(self.options) - 1)
        self.index = round(rel_x / step_width)
        
    def get_value(self):
        return self.options[self.index][1]
    
def draw_sidebar(screen):
    # draw a background
    rect = pygame.Rect(MAZE_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT)
    pygame.draw.rect(screen, SIDEBAR_COLOUR, rect)

    pygame.draw.line(screen, BUTTON1_COLOUR, (MAZE_WIDTH, 0), (MAZE_WIDTH, HEIGHT), 2)

def draw_status_bar(screen, status_text="Idle", status_color=STATUS_IDLE, scanned=0, path=0, efficiency=0):
    # draw background
    bar_rect = pygame.Rect(0, MAZE_HEIGHT, MAZE_WIDTH, HEIGHT - MAZE_HEIGHT)
    pygame.draw.rect(screen, BOTTOM_BAR_COLOUR, bar_rect)
    
    # draw top border
    pygame.draw.line(screen, BUTTON1_COLOUR, (0, MAZE_HEIGHT), (MAZE_WIDTH, MAZE_HEIGHT), 2)

    font = pygame.font.SysFont('Segoe UI, Helvetica Neue, Arial', 16, bold=True)
    
    # draw status badge 
    text_color = TEXT_COLOUR if status_color == STATUS_IDLE else ACTIVE_TEXT_COLOUR
    status_surf = font.render(status_text, True, text_color)
    
    badge_width = status_surf.get_width() + 30
    badge_rect = pygame.Rect(20, MAZE_HEIGHT + 10, badge_width, 30)
    pygame.draw.rect(screen, status_color, badge_rect, border_radius=6)
    
    screen.blit(status_surf, (badge_rect.centerx - status_surf.get_width()//2, badge_rect.centery - status_surf.get_height()//2))

    # draw analytics
    scan_surf = font.render(f"Scanned Cells:  {scanned}", True, TEXT_COLOUR)
    screen.blit(scan_surf, (220, MAZE_HEIGHT + 14))

    path_surf = font.render(f"Path Length:  {path}", True, TEXT_COLOUR)
    screen.blit(path_surf, (430, MAZE_HEIGHT + 14))

    eff_surf = font.render(f"Efficiency:  {efficiency}%", True, TEXT_COLOUR)
    screen.blit(eff_surf, (620, MAZE_HEIGHT + 14))

def draw_legend(screen, x, y):
    font = pygame.font.SysFont(['poppins', 'segoe ui', 'helvetica', 'arial'], 14)
    title_font = pygame.font.SysFont(['poppins', 'segoe ui', 'helvetica', 'arial'], 12, bold=True)
    
    # legend Title
    title_surf = title_font.render("LEGEND", True, BUTTON1H_COLOUR)
    screen.blit(title_surf, (x, y))
    
    # legend items
    items = [
        (SCAN_COLOUR, "Explored cells"),
        (PATH_COLOUR, "Solution path"),
        (START_COLOUR, "Start node"),
        (END_COLOUR, "End node")
    ]
    
    start_y = y + 25
    for i, (color, text) in enumerate(items):
        col = i % 2
        row = i // 2
        
        item_x = x + (col * 150)
        item_y = start_y + (row * 28)
        
        # draw box
        pygame.draw.rect(screen, color, (item_x, item_y, 14, 14), border_radius=3)
        
        # draw text
        text_surf = font.render(text, True, TEXT_COLOUR)
        screen.blit(text_surf, (item_x + 22, item_y - 2))