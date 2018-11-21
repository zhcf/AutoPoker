import logging
import time
import math
from gui.control import *
from game.elements import *
from game.roles import *

class GameAction:
    def __init__(self, action, bet):
        self.action = action
        self.bet = bet

    def to_string(self):
        return "(%s, %f)" % (self.action, self.bet)


class GamePlayer:
    def __init__(self, code, position, balance):
        self.code = code
        self.position = position
        self.balance = balance

    def to_string(self):
        if self.position[1] > 0:
            return ("(%s, %s+%d, %f)" % (self.code, self.position[0], self.position[1], self.balance))
        else:
            return ("(%s, %s, %f)" % (self.code, self.position[0], self.balance))

class GameTable:
    def __init__(self, max_players, rect, queue):
        self.rect = rect
        self.queue = queue
        self.max_players = max_players

    def wait_for_action(self):
        wait_for_any(self.rect, [BET_MIN, BET_MAX,
            ACTION_FOLD, ACTION_CHECK, ACTION_CALL,
            ACTION_BET, ACTION_RAISE])
        # Wait 1 seconds for bet animation
        time.sleep(1)

    def get_players(self):
        players = []
        poker = None
        opponents = []
        if self.max_players == 6:
            player_regions = PLAYERS_6_REGION_LIST
        elif self.max_players == 9:
            player_regions = PLAYERS_9_REGION_LIST
        assert player_regions is not None
        # Look for btn position
        btn_anchor = find_in_rect(BTN_ANCHOR, self.rect)
        assert btn_anchor is not None
        # Set players
        btn_exist = False
        for player_region in player_regions:
            player_region_rect = Rect(self.rect.x + player_region[0],
                self.rect.y + player_region[1],
                PLAYER_REGION_WIDTH,
                PLAYER_REGION_HEIGHT)
            player = None
            if poker is None:
                player = self.__get_poker(player_region_rect)
                poker = player
            else:
                player = self.__get_opponent(player_region_rect)
                opponents.append(player)
            if not btn_exist and player_region_rect.is_rect_in(btn_anchor):
                player.position = (POSITION_BTN, 0)
                btn_exist = True
            players.append(player)
        # Set position
        assert btn_exist == True
        while players[-1].position is None or players[-1].position[0] != POSITION_BTN:
            player = players.pop(0)
            players.append(player)
        positions = get_player_positions(self.max_players)
        for index, position in enumerate(positions):
            players[index].position = position
        return (poker, opponents)

    def __get_poker(self, region_rect):
        poker_anchors = find_all_in_rect(POKER_ANCHOR, region_rect)
        assert len(poker_anchors) == 2
        if poker_anchors[0].x < poker_anchors[1].x:
            poker_anchor = poker_anchors[0]
        else:
            poker_anchor = poker_anchors[1]
        balance = self.__get_poker_balance(poker_anchor)
        poker = GamePlayer('poker', None, balance)
        return poker

    def __get_poker_balance(self, anchor_rect):
        if self.max_players == 6:
            poker_balance_offset_x = POKER_BALANCE_LEFT_OFFSET_X
        elif self.max_players == 9:
            poker_balance_offset_x = POKER_BALANCE_RIGHT_OFFSET_X
        balance_rect = Rect(anchor_rect.x + poker_balance_offset_x,
            anchor_rect.y + POKER_BALANCE_OFFSET_Y,
            BALANCE_WIDTH,
            BALANCE_HEIGHT)
        return self.__get_balance(balance_rect)

    def __get_opponent(self, region_rect):
        anchor = find_in_rect(OPPONENT_ANCHOR, region_rect)
        if anchor is None:
            code = None
            balance = 0
        else:
            code = self.__get_opponent_identity(anchor)
            balance = self.__get_opponent_balance(anchor)
        return GamePlayer(code, None, balance)

    def __get_opponent_identity(self, anchor_rect):
        return "%dX%d" % (anchor_rect.x, anchor_rect.y)

    def __get_opponent_balance(self, anchor_rect):
        if anchor_rect.x <= self.rect.x + self.rect.w / 2:
            balance_offset_x = OPPONENT_BALANCE_LEFT_OFFSET_X
        else:
            balance_offset_x = OPPONENT_BALANCE_RIGHT_OFFSET_X
        balance_rect = Rect(anchor_rect.x + balance_offset_x,
            anchor_rect.y + OPPONENT_BALANCE_OFFSET_Y,
            BALANCE_WIDTH,
            BALANCE_HEIGHT)
        return self.__get_balance(balance_rect)

    def __get_balance(self, rect):
        try:
            return get_number_from_rect(rect)
        except Exception as e:
            str = get_string_from_rect(rect)
            if str.upper() == 'ALL IN':
                return 0
            else:
                raise e

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
        community_cards = []
        hand_cards = []
        river_rect = Rect(self.rect.x + RIVER_OFFSET_X,
            self.rect.y + RIVER_OFFSET_Y,
            RIVER_WIDTH,
            RIVER_HEIGHT)
        card_anchors = find_all_in_rect(CARD_ANCHOR, self.rect)
        for card_anchor in card_anchors:
            card = self.__get_card(card_anchor)
            if river_rect.is_point_in(card_anchor.x, card_anchor.y):
                community_cards.append(card)
            else:
                hand_cards.append(card)
        return (community_cards, hand_cards)

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
        return get_card(suit, rank)

    def __get_card_rank(self, rect, suit):
        if suit == SUIT_SPADE or suit == SUIT_CLUB:
            suit_index = 0
        if suit == SUIT_DIAMOND or suit == SUIT_HEART:
            suit_index = 1
        card_rank_dict = {
            RANK_2: CARD_RANK_2[suit_index],
            RANK_3: CARD_RANK_3[suit_index],
            RANK_4: CARD_RANK_4[suit_index],
            RANK_5: CARD_RANK_5[suit_index],
            RANK_6: CARD_RANK_6[suit_index],
            RANK_7: CARD_RANK_7[suit_index],
            RANK_8: CARD_RANK_8[suit_index],
            RANK_9: CARD_RANK_9[suit_index],
            RANK_T: CARD_RANK_T[suit_index],
            RANK_J: CARD_RANK_J[suit_index],
            RANK_Q: CARD_RANK_Q[suit_index],
            RANK_K: CARD_RANK_K[suit_index],
            RANK_A: CARD_RANK_A[suit_index]
            }
        rank_index = batch_compare_rect(rect, list(card_rank_dict.values()))
        if rank_index >= 0:
            return list(card_rank_dict.keys())[rank_index]
        return None

    def __get_card_suit(self, rect):
        card_suit_dict = {
            SUIT_CLUB: CARD_SUIT_C,
            SUIT_DIAMOND: CARD_SUIT_D,
            SUIT_HEART: CARD_SUIT_H,
            SUIT_SPADE: CARD_SUIT_S
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
            ('raise', ACTION_RAISE)]
        for action in all_actions:
            action_rect = find_in_rect(action[1], self.rect)
            if action_rect is not None:
                if action_rect.h < ACTION_HEIGHT:
                    bet = self.__get_action_bet(action_rect)
                    avail_actions.append(GameAction(action[0], bet))
                else:
                    avail_actions.append(GameAction(action[0], 0))
        return avail_actions

    def __get_action_bet(self, action_rect):
        bet_rect = Rect(action_rect.x,
            action_rect.y + action_rect.h,
            action_rect.w,
            ACTION_HEIGHT - action_rect.h)
        bet = get_number_from_rect(bet_rect)
        return bet

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
        elif action.action == 'raise':
            #click_in_rect(self.rect, ACTION_RAISE)
            self.queue.put(('click', self.rect, ACTION_RAISE))
        else:
            logging.error("Invalid action: %s" % action.to_string())
