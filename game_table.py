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

    def get_hand_cards(self):
        rect = Rect(self.rect.x,
            self.rect.y + HAND_CARDS_Y_OFFSET,
            self.rect.w,
            self.rect.h - HAND_CARDS_Y_OFFSET)
        hand_cards = []
        card_anchor_rects = find_all_in_rect(CARD_ANCHOR, rect)
        for card_anchor_rect in card_anchor_rects:
            hand_cards.append(self.__get_card(card_anchor_rect))
        return hand_cards

    def __get_card(self, anchor_rect):
        color_rect = Rect(anchor_rect.x + CARD_COLOR_X_OFFSET,
            anchor_rect.y + CARD_COLOR_Y_OFFSET,
            CARD_COLOR_WIDTH,
            CARD_COLOR_HEIGHT)
        color = self.__get_card_color(color_rect)
        value_rect = Rect(anchor_rect.x + CARD_VALUE_X_OFFSET,
            anchor_rect.y + CARD_VALUE_Y_OFFSET,
            CARD_VALUE_WIDTH,
            CARD_VALUE_HEIGHT)
        value = self.__get_card_value(value_rect, color)
        return (value, color)

    def __get_card_value(self, rect, color):
        if color == 'S' or color == 'C':
            index = 0
        if color == 'D' or color == 'H':
            index = 1
        all_values = [('A', CARD_VALUE_A[index]),
            ('2', CARD_VALUE_2[index]),
            ('3', CARD_VALUE_3[index]),
            ('4', CARD_VALUE_4[index]),
            ('5', CARD_VALUE_5[index]),
            ('6', CARD_VALUE_6[index]),
            ('7', CARD_VALUE_7[index]),
            ('8', CARD_VALUE_8[index]),
            ('9', CARD_VALUE_9[index]),
            ('10', CARD_VALUE_10[index]),
            ('J', CARD_VALUE_J[index]),
            ('Q', CARD_VALUE_Q[index]),
            ('K', CARD_VALUE_K[index])]
        for value in all_values:
            if compare_rect(rect, value[1]):
                return value[0]
        return None

    def __get_card_color(self, rect):
        all_colors = [('C', CARD_COLOR_C),
            ('D', CARD_COLOR_D),
            ('H', CARD_COLOR_H),
            ('S', CARD_COLOR_S)]
        for color in all_colors:
            if compare_rect(rect, color[1]):
                return color[0]
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
