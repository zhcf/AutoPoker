import logging
import time
import role_utils as utils

class PlayEngine:
    def __init__(self, code, table, poker):
        self.code = code
        self.table = table
        self.poker = poker

    def play(self):
        while True:
            self.table.wait_for_action()
            # Get game status
            t1 = time.time()
            avail_actions = self.table.get_avail_actions()
            (table_cards, hand_cards) = self.table.get_cards()
            pot = self.table.get_pot()
            players = self.table.get_players()
            poker = self.table.get_poker()
            self.__log_status(avail_actions, table_cards, hand_cards, pot, players, poker)
            # Get decision from poker
            poker_decision = self.poker.on_turn(hand_cards, table_cards, pot, players, poker)
            logging.info(self.__unique_output("Poker decision: %s" % poker_decision))
            # Transfer decision to action
            poker_action = self.__get_action_from_decision(poker_decision, avail_actions)
            logging.info(self.__unique_output("Real action: %s" % poker_action.to_string()))
            t2 = time.time()
            logging.info(self.__unique_output("Turn time: %d" % (t2 - t1)))
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

    def __log_status(self, actions, table_cards, hand_cards, pot, players, poker):
        temp_strs = []
        for action in actions:
            temp_strs.append(action.to_string())
        logging.info(self.__unique_output("Actions: %s" % ' '.join(temp_strs)))

        temp_strs = []
        for card in table_cards:
            temp_strs.append(utils.format_card(card))
        logging.info(self.__unique_output("Table cards: %s" % ' '.join(temp_strs)))

        temp_strs = []
        for card in hand_cards:
            temp_strs.append(utils.format_card(card))
        logging.info(self.__unique_output("Hand cards: %s" % ' '.join(temp_strs)))

        logging.info(self.__unique_output("Pot: %f" % pot))

        temp_strs = []
        for player in players.items():
            temp_strs.append("[%s]%f" % (player[0], player[1]))
        logging.info(self.__unique_output("Players: %s" % ' '.join(temp_strs)))

        logging.info(self.__unique_output("Poker: %f" % poker))

    def __unique_output(self, output_str):
        return "[%s] %s" % (self.code, output_str)
