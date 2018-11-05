import logging
import time
import role_utils as utils
import threading

class PlayEngine:
    def __init__(self, code, table, poker):
        self.code = code
        self.table = table
        self.poker = poker
        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self.play)
        self.thread.start()

    def join(self):
        if self.thread is not None:
            self.thread.join()

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
            logging.info(self.__unique_output("Poker action: %s" % poker_action))
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
            logging.info(self.__unique_output("Real action: %s", action.to_string()))
            # Take action
            self.table.do_action(action)
            time.sleep(2)

    def __log_status(self, actions, table_cards, hand_cards, pot):
        temp_strs = []
        for action in actions:
            temp_strs.append(action.to_string())
        logging.info(self.__unique_output("Actions: %s" % ' '.join(temp_strs)))

        temp_strs = []
        for card in table_cards:
            temp_strs.append(str(card))
        logging.info(self.__unique_output("Table cards: %s" % ' '.join(temp_strs)))

        temp_strs = []
        for card in hand_cards:
            temp_strs.append(str(card))
        logging.info(self.__unique_output("Hand cards: %s" % ' '.join(temp_strs)))

        logging.info(self.__unique_output("Pot: %f" % pot))

    def __unique_output(self, output_str):
        return "[%s] %s" % (self.code, output_str)
