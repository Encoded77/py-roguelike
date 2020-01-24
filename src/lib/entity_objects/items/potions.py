import tcod as libtcod

from lib.enums.render_order import RenderOrder
from lib.entity_objects.entity import Entity
from lib.entity_objects.components.item import Item
from lib.item_functions import heal


def healing_potion(x, y):
    # Healing potion
    item_component = Item(use_function=heal, amount=8)
    return Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                  item=item_component)
