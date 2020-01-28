from lib.enums.equipment_slots import EquipmentSlots


class Equipment:
    """
                        Equipement 'inventory'
            List all currently equipped items & empty slots
            Has method & properties to toggle equipments & show bonuses
    """
    def __init__(self, main_hand=None, off_hand=None, head=None,
                 body=None, legs=None, finger=None):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.head = head
        self.body = body
        self.legs = legs
        self.finger = finger

    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.max_hp_bonus

        if self.body and self.body.equippable:
            bonus += self.body.equippable.max_hp_bonus

        if self.legs and self.legs.equippable:
            bonus += self.legs.equippable.max_hp_bonus

        if self.finger and self.finger.equippable:
            bonus += self.finger.equippable.max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.power_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.power_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.power_bonus

        if self.body and self.body.equippable:
            bonus += self.body.equippable.power_bonus

        if self.legs and self.legs.equippable:
            bonus += self.legs.equippable.power_bonus

        if self.finger and self.finger.equippable:
            bonus += self.finger.equippable.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.defense_bonus

        if self.body and self.body.equippable:
            bonus += self.body.equippable.defense_bonus

        if self.legs and self.legs.equippable:
            bonus += self.legs.equippable.defense_bonus

        if self.finger and self.finger.equippable:
            bonus += self.finger.equippable.defense_bonus

        return bonus

    # TODO: Rework this to be more DRY
    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            # De-equip item if its already on
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    # De-equip previous items
                    results.append({'dequipped': self.main_hand})

                # Equip new item
                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        if slot == EquipmentSlots.OFF_HAND:
            # De-equip item if its already on
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    # De-equip previous items
                    results.append({'dequipped': self.off_hand})

                # Equip new item
                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        if slot == EquipmentSlots.HEAD:
            # De-equip item if its already on
            if self.head == equippable_entity:
                self.head = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.head:
                    # De-equip previous items
                    results.append({'dequipped': self.head})

                # Equip new item
                self.head = equippable_entity
                results.append({'equipped': equippable_entity})

        if slot == EquipmentSlots.BODY:
            # De-equip item if its already on
            if self.body == equippable_entity:
                self.body = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.body:
                    # De-equip previous items
                    results.append({'dequipped': self.body})

                # Equip new item
                self.body = equippable_entity
                results.append({'equipped': equippable_entity})

        if slot == EquipmentSlots.LEGS:
            # De-equip item if its already on
            if self.legs == equippable_entity:
                self.legs = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.legs:
                    # De-equip previous items
                    results.append({'dequipped': self.legs})

                # Equip new item
                self.legs = equippable_entity
                results.append({'equipped': equippable_entity})

        if slot == EquipmentSlots.FINGER:
            # De-equip item if its already on
            if self.finger == equippable_entity:
                self.finger = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.finger:
                    # De-equip previous items
                    results.append({'dequipped': self.finger})

                # Equip new item
                self.finger = equippable_entity
                results.append({'equipped': equippable_entity})

        return results
