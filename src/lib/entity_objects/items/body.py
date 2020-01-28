import tcod as libtcod

from lib.enums.equipment_slots import EquipmentSlots
from lib.enums.render_order import RenderOrder

from lib.entity_objects.entity import Entity
from lib.entity_objects.components.equippable import Equippable


def leather_armor(x, y):
    equippable_component = Equippable(EquipmentSlots.BODY, defense_bonus=2, max_hp_bonus=25)
    return Entity(x, y, 'a', libtcod.dark_amber, 'Leather armor', equippable=equippable_component,
                  render_order=RenderOrder.ITEM)


def iron_armor(x, y):
    equippable_component = Equippable(EquipmentSlots.BODY, defense_bonus=4, max_hp_bonus=50)
    return Entity(x, y, 'a', libtcod.dark_amber, 'Iron armor', equippable=equippable_component,
                  render_order=RenderOrder.ITEM)
