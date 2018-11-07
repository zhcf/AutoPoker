from gui_element import *
from gui_control import *
import logging

class GameAction:
    def __init__(self, action, bet_amount):
        self.action = action
        self.bet_amount = bet_amount

    def to_string(self):
        return "(%s, %f)" % (self.action, self.bet_amount)


class GameTable:
    def __init__(self, rect, queue):
        self.rect = rect
        self.queue = queue

    def wait_for_action(self):
        wait_for_any(self.rect, [BET_MIN, BET_MAX,
            ACTION_FOLD, ACTION_CHECK, ACTION_CALL,
            ACTION_BET, ACTION_RAISE_TO])

    def get_poker(self):
        balance = self.__get_poker_balance()
        return balance

    def __get_poker_balance(self):
        balance_rect = Rect(self.rect.x + POKER_OFFSET_X,
            self.rect.y + POKER_OFFSET_Y,
            PLAYER_BALANCE_WIDTH,
            PLAYER_BALANCE_HEIGHT)
        return get_number_from_rect(balance_rect)

    def get_players(self):
        players = dict()
        player_anchors_left = find_all_in_rect(PLAYER_ANCHOR_LEFT, self.rect)
        player_anchors_right = find_all_in_rect(PLAYER_ANCHOR_RIGHT, self.rect)
        player_anchors_combine = [('left', player_anchors_left), ('right', player_anchors_right)]
        for player_anchors in player_anchors_combine:
            direct = player_anchors[0]
            for anchor in player_anchors[1]:
                if self.__is_poker_myself(anchor):
                    continue
                code = self.__get_player_identity(anchor)
                balance = self.__get_player_balance(anchor, direct)
                if balance is not None:
                    players[code] = balance
        return players

    def __get_player_identity(self, anchor_rect):
        return "%dX%d" % (anchor_rect.x, anchor_rect.y)

    def __get_player_balance(self, anchor_rect, position):
        if position == 'left':
            balance_rect = Rect(anchor_rect.x + anchor_rect.w,
                anchor_rect.y,
                PLAYER_BALANCE_WIDTH,
                PLAYER_BALANCE_HEIGHT)
        if position == 'right':
            balance_rect = Rect(anchor_rect.x - PLAYER_BALANCE_WIDTH,
                anchor_rect.y,
                PLAYER_BALANCE_WIDTH,
                PLAYER_BALANCE_HEIGHT)
        balance_str = get_string_from_rect(balance_rect)
        if balance_str == 'Sitting Out':
            return None
        else:
            return get_number_from_rect(balance_rect)

    def __is_poker_myself(self, anchor_rect):
        check_rect = Rect(self.rect.x + POKER_OFFSET_X - POKER_RANGE_MARGIN,
            self.rect.y + POKER_OFFSET_Y - POKER_RANGE_MARGIN,
            PLAYER_BALANCE_WIDTH + 2 * POKER_RANGE_MARGIN,
            PLAYER_BALANCE_HEIGHT + 2 * POKER_RANGE_MARGIN)
        if check_rect.x <= anchor_rect.x and anchor_rect.x <= (check_rect.x + check_rect.w) \
            and check_rect.y <= anchor_rect.y and anchor_rect.y <= (check_rect.y + check_rect.h):
            return True
        else:
            return False

    def get_pot(self):
        pot_left_rect = find_in_rect(POT_LEFT, self.rect)
        if pot_left_rect is None:
            return None
        MARGIN = 10
        search_rect = Rect(pot_left_rect.x,
            pot_left_rect.y - MARGIN,
            (self.rect.x + self.rect.w) - (pot_left_rect.x + pot_left_rect.w),
            MARGIN * 2)
        pot_right_rect = find_in_rect(POT_RIGHT, search_rect)
        if pot_right_rect is None:
            return None
        pot_rect = Rect(pot_left_rect.x + pot_left_rect.w,
            pot_left_rect.y,
            (pot_right_rect.x + pot_right_rect.w) - (pot_left_rect.x + pot_left_rect.w),
            pot_left_rect.h)
        pot = get_number_from_rect(pot_rect)
        return pot

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
            'T': CARD_VALUE_T[color_index],
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
        bet_amount = get_number_from_rect(bet_amount_rect)
        return bet_amount

    def do_action(self, action):
        if action.action == 'fold':
            #click_in_rect(self.rect, ACTION_FOLD)
            self.queue.put(('click', self.rect, ACTION_FOLD))
        elif action.action == 'check':
            #click_in_rect(self.rect, ACTION_CHECK)
            self.queue.put(('click', self.rect, ACTION_CHECK))
        elif action.action == 'call':
            #click_in_rect(self.rect, ACTION_CALL)
            self.queue.put(('click', self.rect, ACTION_CALL))
        elif action.action == 'bet':
            #click_in_rect(self.rect, ACTION_BET)
            self.queue.put(('click', self.rect, ACTION_BET))
        elif action.action == 'raise_to':
            #click_in_rect(self.rect, ACTION_RAISE_TO)
            self.queue.put(('click', self.rect, ACTION_RAISE_TO))
        else:
            logging.error("Invalid action: %s" % action.to_string())
