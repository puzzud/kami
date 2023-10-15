import unittest
from main import *


# Tests ######################################################################
class TestKami(unittest.TestCase):
	def test_cannot_play_empress_face_down_round_first_turn(self):
		player_index_0: int = 0

		player_hand: list[CardId] = [CardId.EMPRESS]
		played_cards: list[CardId] = [[], [], [], []]
		offensive_player_index: int = -1 # No player with an offensive card played.
		to_play_cards: list[CardId] = [] # This player has not selected any cards to play, including defensive line.

		self.assertFalse(can_player_play_card_id(player_index_0, CardId.EMPRESS, player_hand, played_cards, offensive_player_index, to_play_cards))
	

	def test_can_play_double_empress(self):
		player_index_0: int = 0
		player_index_3: int = 3

		player_hand: list[CardId] = [CardId.EMPRESS, CardId.EMPRESS]
		played_cards: list[CardId] = [
			[],
			[],
			[],
			[CardId.TOWER, CardId.TOWER] # player_index_3 started with 2 towers.
		]
		offensive_player_index: int = player_index_3
		to_play_cards: list[CardId] = [] # This player has not selected any cards to play, including defensive line.

		self.assertTrue(can_player_play_card_id(player_index_0, CardId.EMPRESS, player_hand, played_cards, offensive_player_index, to_play_cards))

		player_hand.remove(CardId.EMPRESS)
		to_play_cards.append(CardId.EMPRESS)

		self.assertTrue(can_player_play_card_id(player_index_0, CardId.EMPRESS, player_hand, played_cards, offensive_player_index, to_play_cards))


##############################################################################
if __name__ == '__main__':
	unittest.main()
