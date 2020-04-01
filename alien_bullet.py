import pygame 
from bullet import Bullet

class AlienBullet(Bullet):
    
    def __init__(self, ai_settings, screen, alien):
        """Create a bullet shot by an alien."""
        super().__init__(ai_settings, screen, alien)
        self.rect.centerx = alien.rect.centerx
        self.rect.bottom = alien.rect.bottom
        self.y = float(self.rect.y)
        self.speed_factor *= - 1
        self.color = ai_settings.alien_bullet_color
        
