import pygame

from .settings import ActionSettings


ACTION_CONFIG = ActionSettings()


def handle_quit_events():
    """
    Handle global quit / escape events.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            raise SystemExit
        yield event


def handle_manual_input(game):
    """
    Manual keyboard control.
    Arrow keys -> spaceship
    WASD -> Peach
    Space -> spaceship shoot
    """
    for event in handle_quit_events():
        if (
            game.spaceship is not None
            and event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
        ):
            game.spaceship.shoot()

    is_key_pressed = pygame.key.get_pressed()

    if game.spaceship is not None:
        if is_key_pressed[pygame.K_RIGHT]:
            game.spaceship.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            game.spaceship.rotate(clockwise=False)

        if is_key_pressed[pygame.K_UP]:
            game.spaceship.accelerate()

    if game.peach is not None:
        if is_key_pressed[pygame.K_d]:
            game.peach.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_a]:
            game.peach.rotate(clockwise=False)

        if is_key_pressed[pygame.K_w]:
            game.peach.accelerate()


def apply_agent_actions(game, ship_actions=None, peach_actions=None):
    """
    Apply AI/controller-generated actions.

    Expected format:
        [ACTION_CONFIG.clockwise_action, ACTION_CONFIG.accelerate_action]
        [ACTION_CONFIG.counter_clockwise_action]
        []
    """
    ship_actions = ship_actions or []
    peach_actions = peach_actions or []

    # Still process quit/escape events
    for _ in handle_quit_events():
        pass

    if game.spaceship is not None:
        if ACTION_CONFIG.clockwise_action in ship_actions:
            game.spaceship.rotate(clockwise=True)
        elif ACTION_CONFIG.counter_clockwise_action in ship_actions:
            game.spaceship.rotate(clockwise=False)

        if ACTION_CONFIG.accelerate_action in ship_actions:
            game.spaceship.accelerate()

        if ACTION_CONFIG.shoot_action in ship_actions:
            game.spaceship.shoot()

    if game.peach is not None:
        if ACTION_CONFIG.clockwise_action in peach_actions:
            game.peach.rotate(clockwise=True)
        elif ACTION_CONFIG.counter_clockwise_action in peach_actions:
            game.peach.rotate(clockwise=False)

        if ACTION_CONFIG.accelerate_action in peach_actions:
            game.peach.accelerate()
