import tcod as libtcod

from lib.enums.equipment_slots import EquipmentSlots
from lib.enums.render_order import RenderOrder

from lib.entity_objects.entity import Entity
from lib.entity_objects.components.equippable import Equippable


def sword(x, y):
    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
    return Entity(x, y, '/', libtcod.sky, 'Sword', equippable=equippable_component,
                  render_order=RenderOrder.ITEM)


def axe(x, y):
    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=4)
    return Entity(x, y, 'p', libtcod.sky, 'Axe', equippable=equippable_component,
                  render_order=RenderOrder.ITEM)


def dagger(x, y):
    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2)
    return Entity(0, 0, '-', libtcod.sky, 'Dagger', equippable=equippable_component,
                  render_order=RenderOrder.ITEM)
