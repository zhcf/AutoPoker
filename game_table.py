from gui_element import *
from gui_control import *


class GameAction:
    def __init__(self, action, bet_amount):
        self.action = action
        self.bet_amount = bet_amount

    def to_string(self):
        return "(%s, %f)" % (self.action, self.bet_amount)


class GameTable:
    def __init__(self, rect):
        self.rect = rect

    def get_cards(self):
        table_cards = []
        hand_cards = []
        table_card_rect = Rect(self.rect.x + TABLE_CARD_OFFSET_X,
            self.rect.y + TABLE_CARD_OFFSET_Y,
            TABLE_CARD_WIDTH,
            TABLE_CARD_HEIGHT)
        card_anchors = find_all_in_rect(CARD_ANCHOR, self.rect)
        for card_anchor in card_anchors:
            card = self.__get_card(card_anchor)
            if table_card_rect.is_point_in(card_anchor.x, card_anchor.y):
                table_cards.append(card)
            else:
                hand_cards.append(card)
        return (table_cards, hand_cards)

    def __get_card(self, anchor_rect):
        color_rect = Rect(anchor_rect.x + CARD_COLOR_OFFSET_X,
            anchor_rect.y + CARD_COLOR_OFFSET_Y,
            CARD_COLOR_WIDTH,
            CARD_COLOR_HEIGHT)
        color = self.__get_card_color(color_rect)
        if color is None:
            return None
        value_rect = Rect(anchor_rect.x + CARD_VALUE_OFFSET_X,
            anchor_rect.y + CARD_VALUE_OFFSET_Y,
            CARD_VALUE_WIDTH,
            CARD_VALUE_HEIGHT)
        value = self.__get_card_value(value_rect, color)
        if value is None:
            return None
        return (value, color)

    def __get_card_value(self, rect, color):
        if color == 'S' or color == 'C':
            color_index = 0
        if color == 'D' or color == 'H':
            color_index = 1
        card_value_dict = {
            'A': CARD_VALUE_A[color_index],
            '2': CARD_VALUE_2[color_index],
            '3': CARD_VALUE_3[color_index],
            '4': CARD_VALUE_4[color_index],
            '5': CARD_VALUE_5[color_index],
            '6': CARD_VALUE_6[color_index],
            '7': CARD_VALUE_7[color_index],
            '8': CARD_VALUE_8[color_index],
            '9': CARD_VALUE_9[color_index],
            '10': CARD_VALUE_10[color_index],
            'J': CARD_VALUE_J[color_index],
            'Q': CARD_VALUE_Q[color_index],
            'K': CARD_VALUE_K[color_index]
            }
        value_index = batch_compare_rect(rect, list(card_value_dict.values()))
        if value_index >= 0:
            return list(card_value_dict.keys())[value_index]
        return None

    def __get_card_color(self, rect):
        card_color_dict = {
            'C': CARD_COLOR_C,
            'D': CARD_COLOR_D,
            'H': CARD_COLOR_H,
            'S': CARD_COLOR_S
            }
        color_index = batch_compare_rect(rect, list(card_color_dict.values()))
        if color_index >= 0:
            return list(card_color_dict.keys())[color_index]
        return None

    def get_avail_actions(self):
        avail_actions = [];
        all_actions = [('bet', ACTION_BET),
            ('call', ACTION_CALL),
            ('check', ACTION_CHECK),
            ('fold', ACTION_FOLD),
            ('raise_to', ACTION_RAISE_TO)]
        for action in all_actions:
            action_rect = find_in_rect(action[1], self.rect)
            if action_rect is not None:
                if action_rect.h < ACTION_HEIGHT:
                    bet_amount = self.__get_action_bet_amount(action_rect)
                    avail_actions.append(GameAction(action[0], bet_amount))
                else:
                    avail_actions.append(GameAction(action[0], 0))
        return avail_actions

    def __get_action_bet_amount(self, action_rect):
        bet_amount_rect = Rect(action_rect.x,
            action_rect.y + action_rect.h,
            action_rect.w,
            ACTION_HEIGHT - action_rect.h)
        amount_str = get_string_from_rect(bet_amount_rect)
        amount_str = str.replace(amount_str, ',', '')
        return float(amount_str)
