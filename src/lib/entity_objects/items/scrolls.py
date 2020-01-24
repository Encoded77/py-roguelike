import tcod as libtcod

from lib.game_messages import Message
from lib.render_functions import RenderOrder
from lib.entity_objects.entity import Entity
from lib.entity_objects.components.item import Item
from lib.item_functions import cast_fireball, cast_confuse, cast_lightning


def fireball_scroll(x, y):
    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
        'Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan), damage=12, radius=3)
    return Entity(x, y, '#', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                  item=item_component)


def confusion_scroll(x, y):
    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan))
    return Entity(x, y, '#', libtcod.light_cyan, 'Confusion scroll', render_order=RenderOrder.ITEM, item=item_component)


def lightning_scroll(x, y):
    item_component = Item(use_function=cast_lightning, damage=20, maximum_range=5)
    return Entity(x, y, '#', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                  item=item_component)
