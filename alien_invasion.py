import sys

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

def run_game():
    # Initialize pygame, settings and screen objects.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    #Make the Play button.
    play_button = Button(ai_settings, screen, "Play!")
    
    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    alien_bullets = Group()
    bonuses = Group()
    shields = []
    
    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens, bonuses)
    
    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
            aliens, bullets, alien_bullets, bonuses)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, bullets,
                aliens, alien_bullets, bonuses)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens,
                bullets, alien_bullets, bonuses, shields)
            gf.update_bonuses(screen, ai_settings, stats, sb, ship, bonuses,
                shields)
        
        gf.update_screen(ai_settings, screen, stats, sb, ship, bullets, aliens,
            play_button, alien_bullets, bonuses, shields)

run_game()
