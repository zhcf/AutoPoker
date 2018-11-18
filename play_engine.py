import logging
import time
import role_utils as utils
import uuid
import os
from gui_control import *

class PlayEngine:
    def __init__(self, window, table, poker, logger):
        self.window = window
        self.table = table
        self.poker = poker
        self.logger = logger

    def play(self):
        while True:
            self.table.wait_for_action()
            # Save screenshot
            screenshot_basename = '%s.png' % uuid.uuid1()
            screenshot_filename = os.path.join(self.logger.log_dir, screenshot_basename)
            capture_rect(self.window, screenshot_filename)
            self.logger.info("Screenshot: %s" % screenshot_basename)
            # Get game status
            t1 = time.time()
            avail_actions = self.table.get_avail_actions()
            (table_cards, hand_cards) = self.table.get_cards()
            pot = self.table.get_pot()
            bet = self.__get_bet_from_actions(avail_actions)
            (poker, opponents) = self.table.get_players()
            self.__log_status(avail_actions, table_cards, hand_cards, pot, opponents, poker)
            # Get decision from poker
            poker_decision = self.poker.on_turn(hand_cards, table_cards, pot, bet, opponents, poker)
            self.logger.info("Poker decision: %s" % poker_decision)
            # Transfer decision to action
            poker_action = self.__get_action_from_decision(poker_decision, avail_actions)
            self.logger.info("Real action: %s" % poker_action.to_string())
            t2 = time.time()
            self.logger.info("Turn time: %d" % (t2 - t1))
            # Take action
            self.table.do_action(poker_action)
            time.sleep(2)

    def __get_action_from_decision(self, decision, avail_actions):
        action = None
        sorted_avail_actions = utils.sort_actions(avail_actions)
        for avail_action in sorted_avail_actions:
            if self.__compare_decision_with_action(decision, avail_action) >= 0:
                action = avail_action
            elif action is None:
                action = avail_action
                break
            else:
                break
        if action is None:
            action = sorted_avail_actions[0]
        return action

    def __compare_decision_with_action(self, decision, action):
        return utils.compare_action(decision, action.action)

    def __get_bet_from_actions(self, actions):
        sorted_actions = utils.sort_actions(actions)
        bets = []
        for action in sorted_actions:
            if action.bet > 0:
                bets.append(action.bet)
        if len(bets) == 0:
            return 0
        return min(bets)

    def __log_status(self, actions, table_cards, hand_cards, pot, opponents, poker):
        temp_strs = []
        for action in actions:
            temp_strs.append(action.to_string())
        self.logger.info("Actions: %s" % ' '.join(temp_strs))

        temp_strs = []
        for card in table_cards:
            temp_strs.append(utils.format_card(card))
        self.logger.info("Community Cards: %s" % ' '.join(temp_strs))

        temp_strs = []
        for card in hand_cards:
            temp_strs.append(utils.format_card(card))
        self.logger.info("Hand Cards: %s" % ' '.join(temp_strs))

        self.logger.info("Pot: %f" % pot)

        temp_strs = []
        for opponent in opponents:
            temp_strs.append(opponent.to_string())
        self.logger.info("Opponents: %s" % ' '.join(temp_strs))

        self.logger.info("Poker: %s" % poker.to_string())
