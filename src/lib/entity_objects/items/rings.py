import tcod as libtcod

from lib.enums.equipment_slots import EquipmentSlots
from lib.enums.render_order import RenderOrder

from lib.entity_objects.entity import Entity
from lib.entity_objects.components.equippable import Equippable


def iron_ring_force(x, y):
    equippable_component = Equippable(EquipmentSlots.FINGER, power_bonus=2)
    return Entity(x, y, 'o', libtcod.gold, 'Iron ring of force', equippable=equippable_component,
                  render_order=RenderOrder.ITEM)


def iron_ring_life(x, y):
    equippable_component = Equippable(EquipmentSlots.FINGER, max_hp_bonus=15)
    return Entity(x, y, 'o', libtcod.gold, 'Iron ring of life', equippable=equippable_component,
                  render_order=RenderOrder.ITEM)
