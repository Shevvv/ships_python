import sys

from random import randint

import pygame

from time import sleep

from bullet import Bullet
from alien import Alien
from alien_bullet import AlienBullet
from bonus import Bonus
from bonus import Shield

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
        (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def assign_bonuses(ai_settings, screen, alien, number_aliens_x, number_rows,
        bonuses, ship):
    """Randomly decide if an alien should be assigned a bonus."""
    if randint(0, number_aliens_x * number_rows) % (
            ai_settings.bonus_chance[0]) == ai_settings.bonus_chance[1]:
        if ai_settings.level in range (6, 11):
            bonus = Bonus(screen, ai_settings, alien, ship, True)
        else:
            bonus = Bonus(screen, ai_settings, alien, ship)
        bonuses.add(bonus)
        if ai_settings.level < 6:
            bonuses.empty()    

def create_alien(ai_settings, screen, aliens, alien_number, row_number,
        number_rows, number_aliens_x, bonuses, ship):
    """Create an alien with their bonuses and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.row_number = row_number
    alien.alien_number = alien_number
    if row_number == number_rows - 1:
        alien.bottommost = True
    else:
        alien.bottommost = False
    assign_bonuses(ai_settings, screen, alien, number_aliens_x, number_rows,
        bonuses, ship)
    aliens.add(alien)    

def create_fleet(ai_settings, screen, ship, aliens, bonuses):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)
    
    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                row_number, number_rows, number_aliens_x, bonuses, ship)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens:
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def close_the_game(stats):
    """Save the high score and close the game."""
    with open('highscore.txt', 'w') as highscore:
        highscore.write(str(stats.high_score))
    sys.exit()

def check_keydown_events(event, ai_settings, stats, sb, screen, ship, bullets,
        aliens, alien_bullets, bonuses):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        close_the_game(stats)
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(stats, sb, aliens, bullets, ai_settings, screen, ship,
            alien_bullets, bonuses)

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def prep_sb(sb):
    """Prepare the scoreboard."""
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

def empty_aliens_and_bullets(aliens, bullets, alien_bullets, bonuses):
    """Empty the list of aliens and bullets."""
    aliens.empty()
    bullets.empty()
    alien_bullets.empty()
    bonuses.empty()

def start_game(stats, sb, aliens, bullets, ai_settings, screen, ship,
        alien_bullets, bonuses):
    """Make all the necessary preparations to start the game."""
    # Reset the game settings.
    ai_settings.initialize_dynamic_settings()
    
    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)
    #Reset the game statistics.
    stats.reset_stats()
    stats.game_active = True
    
    prep_sb(sb)
    
    empty_aliens_and_bullets(aliens, bullets, alien_bullets, bonuses)

    
    # Create a new fleet and center the ship.
    create_fleet(ai_settings, screen, ship, aliens, bonuses)
    ship.center_ship()

def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
        aliens, bullets, alien_bullets, mouse_x, mouse_y, bonuses):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(stats, sb, aliens, bullets, ai_settings, screen, ship,
            alien_bullets, bonuses)
        
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
        bullets, alien_bullets, bonuses):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_the_game(stats)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                ship, aliens, bullets, alien_bullets, mouse_x, mouse_y,
                bonuses)
            
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, sb, screen, ship,
                bullets, aliens, alien_bullets, bonuses)
            
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets,
        alien_bullets, bonuses, shields):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1
        
        #Update scoreboard.
        sb.prep_ships()
    
        empty_aliens_and_bullets(aliens, bullets, alien_bullets, bonuses)
    
        #Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens, bonuses)
        ship.center_ship()
    
        # Pause
        sleep(0.5)
    
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
    shields.clear()

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def get_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets,
        alien_bullets, bonuses):
    """Increase the level when the fleet is taken down."""
    # If the entire fleet is destroyed, start a new level
    empty_aliens_and_bullets(aliens, bullets, alien_bullets, bonuses)
    ai_settings.increase_speed()
    
    # Increase level.
    sb.prep_level()
    create_fleet(ai_settings, screen, ship, aliens, bonuses)

def aliens_shooting(ai_settings, screen, aliens, alien_bullets):
    """Make bottommost aliens randomly shoot their own bullets."""
    for alien in aliens:
        if alien.bottommost and (
                randint (0, 10000) in (
                    range(0, int(ai_settings.alien_bullet_chance)))):
            alien_bullet = AlienBullet(ai_settings, screen, alien)
            alien_bullets.add(alien_bullet)
    alien_bullets.update()

def reassign_bottommost(aliens, col_aliens):
    """Reassign the first aliens above the shotdown ones as bottommost."""
    for alien in col_aliens.copy():
        row_number = alien.row_number
        alien_number = alien.alien_number
        rows = []
        for alien in aliens:
            if alien.alien_number == alien_number:
                rows.append(alien.row_number)
                rows.sort
        if rows:
            row = rows[-1]
            for alien in aliens:
                if alien.alien_number == alien_number and (
                        alien.row_number == row):
                    alien.bottommost = True
        
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        bullets, alien_bullets, aliens, bonuses):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for col_aliens in collisions.values():
            for bonus in bonuses:
                if bonus.alien in col_aliens:
                    bonus.active = True
            reassign_bottommost(aliens, col_aliens)
            stats.score += ai_settings.alien_points * len(col_aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        get_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets,
            alien_bullets, bonuses)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets,
        alien_bullets, bonuses, shields):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets,
                alien_bullets, bonuses, shields)
            break

def remove_bullets_beyond_screen(screen, bullets, alien_bullets):
    """Remove bullets that have gone beyond the screen Surface."""
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    for alien_bullet in alien_bullets.copy():
        if alien_bullet.rect.top >= screen.get_height():
            alien_bullets.remove(alien_bullet)

def update_bullets(ai_settings, screen, stats, sb, ship, bullets, aliens,
        alien_bullets, bonuses):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    aliens_shooting(ai_settings, screen, aliens, alien_bullets)
    
    # Get rid of bullets that have disappeared.
    remove_bullets_beyond_screen(screen, bullets, alien_bullets)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        bullets, alien_bullets, aliens, bonuses)

def check_hit_shield(alien_bullets, shields):
    """
      Check whether the shield has been hit and destroy it if it's been
      depleted.
    """
    hit_shields = None
    hit_shields = pygame.sprite.spritecollide(shields[0], alien_bullets,
        True)
    if hit_shields:
        shields[0].shield_hit()
    if shields[0].strength_left == 0:
        shields.clear()

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets,
        alien_bullets, bonuses, shields):
    """
      Check if the fleet is at an edge,
      and then update the positions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    if shields:
        check_hit_shield(alien_bullets, shields)
    
    
            
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens) or (
            pygame.sprite.spritecollideany(ship, alien_bullets)):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets,
            alien_bullets, bonuses, shields)
    #Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets,
        alien_bullets, bonuses, shields)

def update_bonuses(screen, ai_settings, stats, sb, ship, bonuses, shields):
    """Update bonuses and delete them when they're picked up."""
    collisions = pygame.sprite.spritecollide(ship, bonuses, True)
    if collisions:
        for bonus in collisions:
            if bonus.type == 'ship':
                stats.ships_left += 1
                sb.prep_ships()
            else:
                shield = Shield(screen, ai_settings, ship)
                shields.clear()
                shields.append(shield)
    bonuses.update()
    if shields:
        shields[0].update()

def update_screen(ai_settings, screen, stats, sb, ship, bullets, aliens,
        play_button, alien_bullets, bonuses, shields):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each passsthrough the loop.
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for alien_bullet in alien_bullets:
        alien_bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    for bonus in bonuses:
        if bonus.destroy:
            bonuses.remove(bonus)
        else:
            bonus.draw_bonus()
    
    if shields:
        shields[0].draw_shield()
    
    #Draw the score imformation.
    sb.show_score()
    
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()
