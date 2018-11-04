import logging
import time
import role_utils as utils

class PlayEngine:
    def __init__(self, table, poker):
        self.table = table
        self.poker = poker

    def play(self):
        while True:
            self.table.wait_for_action()
            # Get game status
            avail_actions = self.table.get_avail_actions()
            (table_cards, hand_cards) = self.table.get_cards()
            pot = self.table.get_pot()
            self.__log_status(avail_actions, table_cards, hand_cards, pot)
            # Get action from poker
            poker_action = self.poker.on_turn(hand_cards, table_cards, pot)
            logging.info("Poker action: %s" % poker_action)
            sorted_avail_actions = utils.sort_actions(avail_actions)
            # Transfer action
            action = None
            for avail_action in sorted_avail_actions:
                if utils.compare_action(poker_action, avail_action.action) >= 0:
                    action = avail_action
                elif action is None:
                    action = avail_action
                    break
                else:
                    break
            if action is None:
                action = sorted_avail_actions[0]
            logging.info("Real action: %s", action.to_string())
            # Take action
            self.table.do_action(action)
            time.sleep(2)

    def __log_status(self, actions, table_cards, hand_cards, pot):
        temp_strs = []
        for action in actions:
            temp_strs.append(action.to_string())
        logging.info("Actions: %s" % ' '.join(temp_strs))

        temp_strs = []
        for card in table_cards:
            temp_strs.append(str(card))
        logging.info("Table cards: %s" % ' '.join(temp_strs))

        temp_strs = []
        for card in hand_cards:
            temp_strs.append(str(card))
        logging.info("Hand cards: %s" % ' '.join(temp_strs))

        logging.info("Pot: %f" % pot)
