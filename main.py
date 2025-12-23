import pygame as pygame
import sys
from logger import log_state, log_event
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Set up background image
    background_image = pygame.image.load('background.jpg').convert()
    background_image = pygame.transform.smoothscale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # delta time
    dt = 0

    # Create groups
    asteroids = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    Shot.containers = (shots, updatable, drawable)

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    

    while True:
        log_state()
        # stop program if user closes window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        screen.blit(background_image, (0, 0))
        
        updatable.update(dt)
        for item in drawable:
            item.draw(screen)
        
        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
        pygame.display.flip()
        # One game tick is 1/60th of a second
        # Game will run at 60 fps
        time_passed = clock.tick(60)
        # convert time passed to milliseconds
        dt = time_passed / 1000

if __name__ == "__main__":
    main()
