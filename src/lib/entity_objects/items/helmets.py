import tcod as libtcod

from lib.enums.equipment_slots import EquipmentSlots
from lib.enums.render_order import RenderOrder

from lib.entity_objects.entity import Entity
from lib.entity_objects.components.equippable import Equippable


def leather_helmet(x, y):
    equippable_component = Equippable(EquipmentSlots.HEAD, defense_bonus=1)
    return Entity(x, y, 'h', libtcod.dark_amber, 'Leather helmet', equippable=equippable_component,
                  render_order=RenderOrder.ITEM)


def iron_helmet(x, y):
    equippable_component = Equippable(EquipmentSlots.HEAD, defense_bonus=2)
    return Entity(x, y, 'h', libtcod.dark_amber, 'Iron helmet', equippable=equippable_component,
                  render_order=RenderOrder.ITEM)
