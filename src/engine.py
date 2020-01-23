import tcod as libtcod

# imports
from lib.entity_objects.entity import Entity, get_blocking_entities_at_location
from lib.map_objects.game_map import GameMap
from lib.game_states import GameStates

from lib.input_handlers import handle_keys
from lib.fov_functions import initialize_fov, recompute_fov
from lib.render_functions import render_all, clear_all

def main():
    # Set screen size
    screen_width = 80
    screen_height = 50

    # Tilemap size
    map_width = 80
    map_height = 45

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

    # Init some entities
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white, 'Player')
    entities = [player]

    # Assign custom tileset/fonts & init console
    libtcod.console_set_custom_font('./src/assets/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, 'my-py-roguelike', False)

    con = libtcod.console_new(screen_width, screen_height)

    # init game map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    # Init fov
    fov_recompute = True
    fov_map = initialize_fov(game_map)

    # Mouse & keys infos
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    # Game loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            # Recompute fov map
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)


        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        fov_recompute = False

        libtcod.console_flush() # Update window to display current state
        clear_all(con, entities)

        # Get action from key presses
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')


        # ACTIONS
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    print('You bump into ' + target.name + ' !')
                else:
                    player.move(dx, dy)
                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity != player:
                    print('The ' + entity.name + ' ponders the meaning of its existence.')

            game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    main()
