import tcod as libtcod

from lib.enums.equipment_slots import EquipmentSlots
from lib.enums.render_order import RenderOrder

from lib.entity_objects.entity import Entity
from lib.entity_objects.components.equippable import Equippable


def leather_pants(x, y):
    equippable_component = Equippable(EquipmentSlots.LEGS, defense_bonus=1)
    return Entity(x, y, 'l', libtcod.dark_amber, 'Leather pants', equippable=equippable_component,
                  render_order=RenderOrder.ITEM)


def iron_pants(x, y):
    equippable_component = Equippable(EquipmentSlots.LEGS, defense_bonus=2)
    return Entity(x, y, 'l', libtcod.dark_amber, 'Iron pants', equippable=equippable_component,
                  render_order=RenderOrder.ITEM)
