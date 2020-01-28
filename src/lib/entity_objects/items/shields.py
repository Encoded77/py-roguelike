import tcod as libtcod

from lib.enums.equipment_slots import EquipmentSlots
from lib.enums.render_order import RenderOrder

from lib.entity_objects.entity import Entity
from lib.entity_objects.components.equippable import Equippable


def shield(x, y):
    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
    return Entity(x, y, '[', libtcod.darker_orange, 'Shield', equippable=equippable_component,
                  render_order=RenderOrder.ITEM)
