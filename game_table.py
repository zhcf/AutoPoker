from gui_element import *
from gui_control import *
import logging
import role_utils as utils

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
        poker_anchor = find_in_rect(POKER_ANCHOR, self.rect)
        balance = self.__get_poker_balance(poker_anchor)
        return balance

    def __get_poker_balance(self, anchor_rect):
        balance_rect = Rect(anchor_rect.x + POKER_BALANCE_OFFSET_X,
            anchor_rect.y + POKER_BALANCE_OFFSET_Y,
            BALANCE_WIDTH,
            BALANCE_HEIGHT)
        return get_number_from_rect(balance_rect)

    def get_players(self):
        players = dict()
        player_anchors = find_all_in_rect(PLAYER_ANCHOR, self.rect)
        for anchor in player_anchors:
            code = self.__get_player_identity(anchor)
            balance = self.__get_player_balance(anchor)
            if balance is not None:
                players[code] = balance
        return players

    def __get_player_identity(self, anchor_rect):
        return "%dX%d" % (anchor_rect.x, anchor_rect.y)

    def __get_player_balance(self, anchor_rect):
        balance_rect = Rect(anchor_rect.x + PLAYER_BALANCE_OFFSET_X,
            anchor_rect.y + PLAYER_BALANCE_OFFSET_Y,
            BALANCE_WIDTH,
            BALANCE_HEIGHT)
        return get_number_from_rect(balance_rect)
        # balance_str = get_string_from_rect(balance_rect)
        # if balance_str == 'Sitting Out':
        #     return None
        # else:
        #     return get_number_from_rect(balance_rect)

    # def __is_poker_myself(self, anchor_rect):
    #     check_rect = Rect(self.rect.x + POKER_OFFSET_X - POKER_RANGE_MARGIN,
    #         self.rect.y + POKER_OFFSET_Y - POKER_RANGE_MARGIN,
    #         PLAYER_BALANCE_WIDTH + 2 * POKER_RANGE_MARGIN,
    #         PLAYER_BALANCE_HEIGHT + 2 * POKER_RANGE_MARGIN)
    #     if check_rect.x <= anchor_rect.x and anchor_rect.x <= (check_rect.x + check_rect.w) \
    #         and check_rect.y <= anchor_rect.y and anchor_rect.y <= (check_rect.y + check_rect.h):
    #         return True
    #     else:
    #         return False

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
        river_cards = []
        hand_cards = []
        river_rect = Rect(self.rect.x + RIVER_OFFSET_X,
            self.rect.y + RIVER_OFFSET_Y,
            RIVER_WIDTH,
            RIVER_HEIGHT)
        card_anchors = find_all_in_rect(CARD_ANCHOR, self.rect)
        for card_anchor in card_anchors:
            card = self.__get_card(card_anchor)
            if river_rect.is_point_in(card_anchor.x, card_anchor.y):
                river_cards.append(card)
            else:
                hand_cards.append(card)
        return (river_cards, hand_cards)

    def __get_card(self, anchor_rect):
        suit_rect = Rect(anchor_rect.x + CARD_SUIT_OFFSET_X,
            anchor_rect.y + CARD_SUIT_OFFSET_Y,
            CARD_SUIT_WIDTH,
            CARD_SUIT_HEIGHT)
        suit = self.__get_card_suit(suit_rect)
        if suit is None:
            return None
        rank_rect = Rect(anchor_rect.x + CARD_RANK_OFFSET_X,
            anchor_rect.y + CARD_RANK_OFFSET_Y,
            CARD_RANK_WIDTH,
            CARD_RANK_HEIGHT)
        rank = self.__get_card_rank(rank_rect, suit)
        if rank is None:
            return None
        return utils.get_card(suit, rank)

    def __get_card_rank(self, rect, suit):
        if suit == utils.SUIT_SPADE or suit == utils.SUIT_CLUB:
            suit_index = 0
        if suit == utils.SUIT_DIAMOND or suit == utils.SUIT_HEART:
            suit_index = 1
        card_rank_dict = {
            utils.RANK_2: CARD_RANK_2[suit_index],
            utils.RANK_3: CARD_RANK_3[suit_index],
            utils.RANK_4: CARD_RANK_4[suit_index],
            utils.RANK_5: CARD_RANK_5[suit_index],
            utils.RANK_6: CARD_RANK_6[suit_index],
            utils.RANK_7: CARD_RANK_7[suit_index],
            utils.RANK_8: CARD_RANK_8[suit_index],
            utils.RANK_9: CARD_RANK_9[suit_index],
            utils.RANK_T: CARD_RANK_T[suit_index],
            utils.RANK_J: CARD_RANK_J[suit_index],
            utils.RANK_Q: CARD_RANK_Q[suit_index],
            utils.RANK_K: CARD_RANK_K[suit_index],
            utils.RANK_A: CARD_RANK_A[suit_index]
            }
        rank_index = batch_compare_rect(rect, list(card_rank_dict.values()))
        if rank_index >= 0:
            return list(card_rank_dict.keys())[rank_index]
        return None

    def __get_card_suit(self, rect):
        card_suit_dict = {
            utils.SUIT_CLUB: CARD_SUIT_C,
            utils.SUIT_DIAMOND: CARD_SUIT_D,
            utils.SUIT_HEART: CARD_SUIT_H,
            utils.SUIT_SPADE: CARD_SUIT_S
            }
        suit_index = batch_compare_rect(rect, list(card_suit_dict.values()))
        if suit_index >= 0:
            return list(card_suit_dict.keys())[suit_index]
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
