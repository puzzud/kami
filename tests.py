import unittest
from main import *


# Tests ######################################################################
class TestKami(unittest.TestCase):
	#-------------------------------------------------------------
	# Test to make sure a player cannot play empress card face
	# down when there is no offensive card played.
	#-------------------------------------------------------------
	def test_cannot_play_empress_face_down_round_first_turn(self):
		player_index_0: int = 0

		player_hand: list[CardId] = [
			CardId.SOLDIER,
			CardId.SOLDIER,
			CardId.SOLDIER,
			CardId.SOLDIER,
			CardId.SOLDIER,
			CardId.SOLDIER,
			CardId.SOLDIER,
			CardId.EMPRESS
		]

		played_cards: list[CardId] = [
			[],
			[],
			[],
			[]
		]
		
		offensive_player_index: int = -1 # No player with an offensive card played.
		
		to_play_cards: list[CardId] = [] # This player has not selected any cards to play, including defensive line.

		self.assertFalse(can_player_play_card_id(player_index_0, CardId.EMPRESS, player_hand, played_cards, offensive_player_index, to_play_cards))


	#-------------------------------------------------------------
	# Normally an empress card cannot be played against a soldier
	# or a spearman, but if the player is themself played the last
	# offensive card, they can.
	# TODO: This logic needs verification / clarification.
	#-------------------------------------------------------------
	def test_can_play_double_empress_as_last_two_cards_when_offensive(self):
		player_index_0: int = 0

		player_hand: list[CardId] = [
			CardId.EMPRESS,
			CardId.EMPRESS
		]

		played_cards: list[CardId] = [
			[CardId.MADMAN, CardId.MADMAN, CardId.TOWER, CardId.TOWER, CardId.SPEARMAN, CardId.SPEARMAN], # player_index_1 plays
			[],
			[],
			[]
		]
		
		offensive_player_index: int = player_index_0
		
		to_play_cards: list[CardId] = [] # This player has not selected any cards to play, including defensive line.

		self.assertTrue(can_player_play_card_id(player_index_0, CardId.EMPRESS, player_hand, played_cards, offensive_player_index, to_play_cards))

		to_play_cards.append(CardId.EMPRESS)

		self.assertTrue(can_player_play_card_id(player_index_0, CardId.EMPRESS, player_hand, played_cards, offensive_player_index, to_play_cards))


##############################################################################
if __name__ == '__main__':
	unittest.main()
