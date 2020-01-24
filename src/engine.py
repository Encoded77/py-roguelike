import tcod as libtcod

# imports
from lib.game_states import GameStates
from lib.game_messages import MessageLog, Message
from lib.map_objects.game_map import GameMap
from lib.entity_objects.entity import Entity, get_blocking_entities_at_location
from lib.entity_objects.components.fighter import Fighter
from lib.entity_objects.components.inventory import Inventory

from lib.fov_functions import initialize_fov, recompute_fov
from lib.input_handlers import handle_keys, handle_mouse
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
    max_items_per_room = 2

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
    inventory_component = Inventory(26)
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white, 'Player', 
                    render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component)
    entities = [player]

    # Assign custom tileset/fonts & init console
    libtcod.console_set_custom_font('./src/assets/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, 'my-py-roguelike', False)

    # Screen inits
    con = libtcod.console_new(screen_width, screen_height)
    panel = libtcod.console_new(screen_width, panel_height)

    # init game map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, 
                        player, entities, max_monsters_per_room, max_items_per_room)

    # Init fov
    fov_recompute = True
    fov_map = initialize_fov(game_map)

    # Init messages log
    message_log = MessageLog(message_x, message_width, message_height)

    # Mouse & keys infos
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state
    targeting_item = None

    # Game loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            # Recompute fov map
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)


        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
                   bar_width, panel_height, panel_y, mouse, colors, game_state)
        fov_recompute = False

        libtcod.console_flush() # Update window to display current state
        clear_all(con, entities)

        # Get actions from user inputs
        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        move = action.get('move')
        exit = action.get('exit')
        wait = action.get('wait')
        fullscreen = action.get('fullscreen')

        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')
        

        # Keep tracks a players actions/results
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

        elif wait and game_state == GameStates.PLAYERS_TURN:
            player.fighter.heal(1)
            game_state = GameStates.ENEMY_TURN
        

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))


        if show_inventory and game_state != GameStates.SHOW_INVENTORY:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY


        if drop_inventory and game_state != game_state.DROP_INVENTORY:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY


        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                player.inventory.items): 
            item = player.inventory.items[inventory_index]
            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))


        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click
                
                item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})


        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                return True


        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


        for player_turn_result in player_turn_results:
            
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_dropped = player_turn_result.get('item_dropped')
            item_consumed = player_turn_result.get('item_consumed')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')


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


            if item_added:
                # Delete picked item from entity list
                entities.remove(item_added)
                game_state = GameStates.ENEMY_TURN
            

            if item_consumed:
                game_state = GameStates.ENEMY_TURN


            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN


            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(targeting_item.item.targeting_message)


            if targeting_cancelled:
                game_state = previous_game_state
                message_log.add_message(Message('Targeting cancelled !'))


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
