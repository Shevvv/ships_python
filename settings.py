class Settings():
    """A class to store all settings for Alien Invasion."""
    
    def __init__(self):
        """Initialize the game's static ettings."""
        # Screen settings
        self.screen_width = 1366
        self.screen_height = 768
        self.bg_color = (2, 0, 24)
        
        # Ship settings
        self.ship_limit = 3
        
        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 230, 230, 230
        self.bullets_allowed = 3
        
        # Alien settings
        self.fleet_drop_speed = 10
        self.alien_bullet_color = 0, 255, 255
        
        # Shield bonus settings
        self.edge_width = 5
        self.edge_color = 0, 255, 255
        self.shield_strength = 2
        self.bonus_chance = 37, 7
        self.bonus_time_limit = 200
                
        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.alien_bullet_chance = 1
        self.bonus_speed = 2
        
        # Scoring
        self.alien_points = 50
        
        # Fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        
        # Starting level
        self.level = 1
    
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_bullet_chance += 0.2
        self.bonus_speed *= self.speedup_scale
        self.bonus_time_limit -= 2
        
        self.alien_points = int(self.alien_points * self.score_scale)
        
        self.level += 1
