from random import getrandbits as grb

import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group

class Border(Sprite):
    
    def __init__(self, bonus, edge_index):
        """Create edges for a shield bonus or a shield."""
        super().__init__()
        self.bonus = bonus
        self.edge_index = edge_index
        self.edge_width = bonus.ai_settings.edge_width
        self.bonus_height = bonus.rect.height
        self.bonus_width = bonus.rect.width
        self.edge_color = bonus.ai_settings.edge_color
        if self.edge_index % 2 == 0:
            self.rect = pygame.Rect(0, 0, self.bonus.rect.width,
                self.edge_width)
        else:
            self.rect = pygame.Rect(0, 0, self.edge_width,
                self.bonus.rect.height)
        self.update()
        
    def update(self):
        """Update positions of the edges."""
        if self.edge_index - 2 < 0:
            self.rect.topleft = self.bonus.rect.topleft
        else:
            self.rect.bottomright = self.bonus.rect.bottomright

class Bonus(Sprite):
    
    def __init__(self, screen, ai_settings, alien, ship,
            type_bool=None):
        """
          Create a bonus sprite (extra ship bonus by default),
          align it with the alien.
        """
        super().__init__()
        self.screen = screen
        self.alien = alien
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.rect = pygame.Rect(0, 0, ship.rect.width, ship.rect.height)
        self.rect.center = alien.rect.center
        self.centery = self.alien.rect.centery
        self.active = False
        self.edges = Group()
        self.destroy = False
        self.time_spent = 0
        if type_bool is None:
            type_bool = bool(grb(1))
        if type_bool:
            self.type = 'ship'
            self.get_ship_bonus_image()
        else:
            self.type = 'shield'
            for edge_index in range(0, 4):
                border = Border(self, edge_index)
                self.edges.add(border)
            
    def get_ship_bonus_image(self):
        """Create a ship image for the ship bonus."""
        self.ship_image = pygame.image.load('images\ship.bmp')
        self.ship_image_rect = self.ship_image.get_rect()
        self.ship_image_width = self.ship_image_rect.width
        self.ship_image_height = self.ship_image_rect.height
        self.image = pygame.transform.smoothscale(self.ship_image,
            (int(self.ship_image_width / 2), int(self.ship_image_height / 2)))
        self.image_rect = self.image.get_rect()
    
    def update(self):
        """
          If the bonus is inactive, make its position the same, as the aliens,
          otherwise make it fall to the bottom and lie there for a while.
        """
        if self.active == True:
            if self.rect.bottom < self.screen_rect.height:
                self.centery += self.ai_settings.bonus_speed
                self.rect.centery = self.centery
            elif self.rect.bottom >= self.screen_rect.height:
                self.rect.bottom = self.screen_rect.height
                self.time_spent += 1
                if self.time_spent == self.ai_settings.bonus_time_limit:
                    self.destroy = True
        else:
            self.centery = float(self.alien.rect.centery)
            self.rect.centerx = self.alien.rect.centerx
            self.rect.centery = self.centery
        if self.edges:
            self.edges.update()
    
    def draw_bonus(self):
        """Draw the bonus as is defined by its type."""
        if self.active == True:
            if self.type == 'ship':
                self.draw_ship_bonus()
            else:
                self.draw_shield_bonus()
    
    def draw_ship_bonus(self):
        """Draw the ship bonus."""
        self.image_rect.centery = self.centery
        self.image_rect.centerx = self.alien.rect.centerx
        self.screen.fill(self.ai_settings.bg_color, self.rect)
        self.screen.blit(self.image, self.image_rect)
    
    def draw_shield_bonus(self):
        """Draw the shield bonus."""
        for border in self.edges:
            self.screen.fill(border.edge_color, border.rect)

class Shield():
    
    def __init__(self, screen, ai_settings, ship):
        """A class that defines a picked up shield."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.ship = ship
        self.rect = pygame.Rect(0, 0,
            ship.rect.width + 2 * ai_settings.edge_width,
            ship.rect.height + 2 * ai_settings.edge_width)
        self.borders = Group()
        for edge_index in [0, 1, 3]:
            border = Border(self, edge_index)
            self.borders.add(border)
        self.strength_left = ai_settings.shield_strength
        self.color_change = []
        for i in range(0, 3):
            self.color_change.append(int((ai_settings.edge_color[i] -
                ai_settings.bg_color[i]) / self.strength_left))
        self.color_change = tuple(self.color_change)
        self.update()
    
    def shield_hit(self):
        """Decrease shield's strength once it's hit."""
        self.strength_left -= 1
        for b in range(0, len(self.borders)):
            color = []
            for i in range(0, len(self.borders.sprites()[b].edge_color)):
                color.append(self.borders.sprites()[b].edge_color[i] - (
                    self.color_change[i]))
            self.borders.sprites()[b].edge_color = tuple(color)
    
    def update(self):
        """Make the shield follow the ship."""
        self.rect.center = self.ship.rect.center
        self.borders.update()
    
    def draw_shield(self):
        """Draw the edges of the shield."""
        for border in self.borders:
            self.screen.fill(border.edge_color, border.rect)
        
