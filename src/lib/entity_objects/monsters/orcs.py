import tcod as libtcod

from lib.entity_objects.entity import Entity
from lib.entity_objects.components.ai import BasicMonster
from lib.entity_objects.components.fighter import Fighter
from lib.render_functions import RenderOrder


def create_orc(x, y):
    fighter_component = Fighter(hp=10, defense=0, power=3, xp=35)
    ai_component = BasicMonster()

    return Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', True, render_order=RenderOrder.ACTOR,
                        fighter=fighter_component, ai=ai_component)
