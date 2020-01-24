import tcod as libtcod

from lib.entity_objects.entity import Entity
from lib.entity_objects.components.ai import BasicMonster
from lib.entity_objects.components.fighter import Fighter
from lib.enums.render_order import RenderOrder


def create_troll(x, y):
    fighter_component = Fighter(hp=30, defense=2, power=8, xp=100)
    ai_component = BasicMonster()
    return Entity(x, y, 'T', libtcod.darker_green, 'Troll', True, render_order=RenderOrder.ACTOR,
                        fighter=fighter_component, ai=ai_component)
