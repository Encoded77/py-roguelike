import tcod as libtcod

from lib.game_messages import MessageLog
from lib.map_objects.game_map import GameMap
from lib.entity_objects.entity import Entity

from lib.enums.game_states import GameStates
from lib.enums.render_order import RenderOrder

from lib.entity_objects.components.level import Level
from lib.entity_objects.components.fighter import Fighter
from lib.entity_objects.components.equipment import Equipment
from lib.entity_objects.components.inventory import Inventory

from lib.entity_objects.items.weapons import dagger


def get_constants():
    window_title = 'Roguelike Tutorial Revised'

    screen_width = 80
    screen_height = 50

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    level_up_base = 200
    level_up_factor = 150

    max_monsters_per_room = 3
    max_items_per_room = 2

    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'level_up_base': level_up_base,
        'level_up_factor': level_up_factor,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
        'colors': colors
    }

    return constants


def get_game_variables(constants):
    # Player creation
    fighter_component = Fighter(hp=100, defense=1, power=3)
    inventory_component = Inventory(26)
    equipment_component = Equipment()

    level = Level(level_up_base=constants['level_up_base'], level_up_factor=constants['level_up_factor'])
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component, level=level, equipment=equipment_component)
    entities = [player]

    starter_weapon = dagger(0, 0)

    player.inventory.add_item(starter_weapon)
    player.equipment.toggle_equip(starter_weapon)

    # Map creation
    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
