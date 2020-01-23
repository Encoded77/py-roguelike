import tcod as libtcod

# imports
from lib.game_states import GameStates
from lib.game_messages import MessageLog
from lib.map_objects.game_map import GameMap
from lib.entity_objects.entity import Entity, get_blocking_entities_at_location
from lib.entity_objects.components.fighter import Fighter

from lib.fov_functions import initialize_fov, recompute_fov
from lib.input_handlers import handle_keys
from lib.death_functions import kill_monster, kill_player
from lib.render_functions import render_all, clear_all, RenderOrder

def main():
    # Set screen size
    screen_width = 80
    screen_height = 50

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    # Tilemap size
    map_width = 80
    map_height = 43

    # Dungeon
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_monsters_per_room = 3

    # fov vars
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    # Map colors
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50),
    }

    # Init player entity
    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white, 'Player', render_order=RenderOrder.ACTOR, fighter=fighter_component)
    entities = [player]

    # Assign custom tileset/fonts & init console
    libtcod.console_set_custom_font('./src/assets/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, 'my-py-roguelike', False)

    # Screen inits
    con = libtcod.console_new(screen_width, screen_height)
    panel = libtcod.console_new(screen_width, panel_height)

    # init game map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    # Init fov
    fov_recompute = True
    fov_map = initialize_fov(game_map)

    # Init messages log
    message_log = MessageLog(message_x, message_width, message_height)

    # Mouse & keys infos
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    # Game loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            # Recompute fov map
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)


        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
                   bar_width, panel_height, panel_y, colors)
        fov_recompute = False

        libtcod.console_flush() # Update window to display current state
        clear_all(con, entities)

        # Get action from key presses
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        player_turn_results = []

        # ACTIONS & PLAYER TURN
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    # Player death
                    message, game_state = kill_player(dead_entity)
                else:
                    # Monster death
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

        # ENEMY TURN
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                # Player death
                                message, game_state = kill_player(dead_entity)
                            else:
                                # Monster death
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    main()
