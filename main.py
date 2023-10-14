from enum import Enum
import random
import time
import sys


# Deck ##############################################################################
class CardId(Enum):
	NONE = -1
	SOLDIER = 0
	HORSEMAN = 1
	SPEARMAN = 2
	DRAGON_SILVER = 3
	DRAGON_GOLD = 4
	MADMAN = 5
	TOWER = 6
	EMPRESS = 7


cards: dict[CardId, dict] = {
	CardId.SOLDIER:       {"name": "Soldier",       "score": 1},
	CardId.HORSEMAN:      {"name": "Horseman",      "score": 2},
	CardId.SPEARMAN:      {"name": "Spearman",      "score": 2},
	CardId.DRAGON_SILVER: {"name": "Silver Dragon", "score": 3},
	CardId.DRAGON_GOLD:   {"name": "Gold Dragon",   "score": 3},
	CardId.MADMAN:        {"name": "Madman",        "score": 4},
	CardId.TOWER:         {"name": "Tower",         "score": 4},
	CardId.EMPRESS:       {"name": "Empress",       "score": 5},
}


standard_deck_card_counts: dict[CardId, int] = {
	CardId.SOLDIER:       10,
	CardId.HORSEMAN:      4,
	CardId.SPEARMAN:      4,
	CardId.DRAGON_SILVER: 4,
	CardId.DRAGON_GOLD:   4,
	CardId.MADMAN:        2,
	CardId.TOWER:         2,
	CardId.EMPRESS:       2,
}


def get_card_name(card_id: CardId) -> str:
	return cards[card_id]["name"]


def get_card_score(card_id: CardId) -> int:
	return cards[card_id]["score"]


def build_deck(card_counts: dict[CardId, int]) -> list[CardId]:
	deck = []

	for card_id in card_counts.keys():
		card_count = card_counts[card_id]
		deck.extend([card_id] * card_count)
	
	return deck


def shuffle_deck(deck: list[CardId]):
	#print("Shuffling deck")
	random.shuffle(deck)
	#print(deck)


# Score ##############################################################################
def reset_team_scores(team_scores: list[int]):
	for team_index in range(len(team_scores)):
		team_scores[team_index] = 0


def adjust_team_score(team_index: int, score_adjustment: int, team_scores: list[int]):
	team_scores[team_index] += score_adjustment


def get_team_score(team_index: int, team_scores: list[int]) -> int:
	if team_index < 0:
		print("get_team_score: Attempted to get score of invalid team index: " + str(team_index), file=sys.stderr)
		return -1

	return team_scores[team_index]


def print_team_scores(team_scores: list[int]):
	team_scores_string_list: list[str] = []
	
	for team_index in range(len(team_scores)):
		team_score = team_scores[team_index]
		team_score_string = "Team %d: %d" % (team_index, team_score)
		team_scores_string_list.append(team_score_string)
	
	team_scores_string = ", ".join(team_scores_string_list)

	print("Scores: %s" % (team_scores_string))


# Win Condition  ##############################################################################
def get_winning_team_index(team_scores: list[int]) -> int:
	winning_team_index = -1
	winning_team_score = 0
	
	for team_index in range(len(team_scores)):
		team_score = team_scores[team_index]
		if team_score < 0:
			continue

		if team_score > winning_team_score:
			winning_team_score = team_score
			winning_team_index = team_index
	
	return winning_team_index


def is_game_over(team_scores: list[int]) -> bool:
	winning_team_index = get_winning_team_index(team_scores)
	if winning_team_index < 0:
		return False
	
	winning_team_score = get_team_score(winning_team_index, team_scores)
	return winning_team_score >= 15 # TODO: Replace with member or constant variable.


# Player ##############################################################################
def get_player_team_index(player_index: int, player_team_indices: list[int]) -> int:
	return player_team_indices[player_index]


def get_player_hand(player_index: int, hands: list[list, CardId]) -> list:
	return hands[player_index]


def print_player_hand(player_index: int, player_team_index: int, player_hand: list[CardId]):
	#print(hand)

	card_name_list: list[str] = []

	for card_id in player_hand:
		card_name_list.append(get_card_name(card_id))
	
	player_hand_string = "[%s]" % (", ".join(card_name_list))
	print("Turn Player %d (Team %d) turn: %s" % (player_index, player_team_index, player_hand_string))



def get_player_played_cards(player_index: int, played_cards: list[list, CardId]) -> list:
	return played_cards[player_index]


def get_player_offensive_card_id(player_index: int, played_cards: list[list, CardId]) -> CardId:
	if player_index < 0 or player_index >= len(played_cards):
		return CardId.NONE

	player_played_cards = get_player_played_cards(player_index, played_cards)

	number_of_player_played_cards = len(player_played_cards)
	if number_of_player_played_cards < 1:
		return CardId.NONE

	# Technically correct to trap on the condition where a player has played
	# a defensive card but not an offensive card;
	# so there is a requirement to ensure an even number of played cards.
	if (number_of_player_played_cards % 2) == 1:
		return CardId.NONE

	return player_played_cards[number_of_player_played_cards - 1]


def get_player_trick_score(player_index: int, played_cards: list[list, CardId]) -> int:
	player_played_cards = get_player_played_cards(player_index, played_cards)
	if len(player_played_cards) < 8: # TODO: Replace with member or constant variable.
		return 0

	offensive_card_id = get_player_offensive_card_id(player_index, played_cards)
	if offensive_card_id == CardId.NONE:
		return 0

	return get_card_score(offensive_card_id)


# Returns list of cards a player wants to play.
# An empty list indicates a pass.
# The 2nd card in the list is assumed to be the offensive card.
# The 1st card is either a face down card or a defensive card.
def get_player_turn_to_play_cards(player_index: int, player_hand: list[CardId], played_cards: list[list, CardId], offensive_player_index: int, player_team_indices: list[int]) -> list[CardId]:
	card_ids: list[CardId] = []
	
	player_hand_copy = player_hand.copy()

	if player_index == offensive_player_index or offensive_player_index < 0:
		# Request a card face down
		# TODO: Use AI
		face_down_card_id = random.choice(player_hand_copy)
		player_hand_copy.remove(face_down_card_id)
		card_ids.append(face_down_card_id)
	else:
		# TODO: Should determine if the offensive card was played by a teammate,
		# which strongly influences whether player should play a defensive card.

		# TODO: Use AI

		# Attempt to request to play a defensive card face up
		offensive_card_id = get_player_offensive_card_id(offensive_player_index, played_cards)
		if offensive_card_id in player_hand_copy:
			player_hand_copy.remove(offensive_card_id)
			card_ids.append(offensive_card_id)
	
	# If possible, request an offensive card face up
	if len(card_ids) > 0:
		# TODO: Use AI
		offensive_card_id = random.choice(player_hand_copy)
		player_hand_copy.remove(offensive_card_id)
		card_ids.append(offensive_card_id)

	return card_ids


# NOTE: Unused
def can_player_play_card_id(player_index: int, card_id: CardId, player_hand: list, played_cards: list, offensive_player_index: int) -> bool:
	if card_id == CardId.NONE:
		return False
	
	if not (card_id in player_hand):
		return False
	
	offensive_card_id = get_player_offensive_card_id(offensive_player_index, played_cards)
	if card_id == offensive_card_id:
		return True

	match card_id:
		case CardId.Empress:
			if offensive_card_id in [CardId.SOLDIER, CardId.SPEARMAN]:
				return False
			elif not has_empress_been_played(played_cards) and offensive_card_id != CardId.NONE:
				return False
			else:
				return False
		case _:
			return offensive_player_index == player_index


# Game Progression ##############################################################################
def play_game():
	# Set up game
	random.seed(int(time.time()))

	number_of_teams: int = 2
	number_players_per_team: int = 2
	number_of_players = number_of_teams * number_players_per_team
	player_team_indices: list[int] = [0, 1, 0, 1] # TODO: Automate this.

	card_counts = standard_deck_card_counts

	# Start game
	team_scores: list[int] = [0] * number_of_teams
	reset_team_scores(team_scores)
	player_index: int = -1
	round_number: int = 0

	print_team_scores(team_scores)

	while not is_game_over(team_scores):
		# Start round
		round_number += 1
		print("Round %d" % (round_number))
		deck = build_deck(card_counts)
		shuffle_deck(deck)
		# TODO: Determine how game rules resolve which player starts round.
		player_index = get_next_turn_player_index(player_index, number_of_players)
		offensive_player_index: int = -1

		hands = deal_hands(deck, number_of_players)
		#print(deck)

		played_cards = [[] for _ in range(number_of_players)]

		while True:
			# Start player turn
			player_hand = get_player_hand(player_index, hands)
			print_player_hand(player_index, get_player_team_index(player_index, player_team_indices), player_hand)

			to_play_cards = get_player_turn_to_play_cards(player_index, player_hand, played_cards, offensive_player_index, player_team_indices)
			if len(to_play_cards) > 0:
				# TODO: Perform validation on to play cards.
				for card_id in to_play_cards:
					card_name = get_card_name(card_id)
					print("Player %d played %s" % (player_index, card_name))
					player_hand.remove(card_id)

				player_played_cards = get_player_played_cards(player_index, played_cards)
				player_played_cards.extend(to_play_cards)

				offensive_player_index = player_index

				trick_score = get_player_trick_score(player_index, played_cards)
				if trick_score > 0:
					team_index = get_player_team_index(player_index, player_team_indices)
					adjust_team_score(team_index, trick_score, team_scores)
					print("Player %d finishes trick and Team %d scores %d points" % (player_index, team_index, trick_score))
					break
			else:
				print("Player %d passes" % (player_index))
				player_index = get_next_turn_player_index(player_index, number_of_players)
		
		print_team_scores(team_scores)

	winning_team_index = get_winning_team_index(team_scores)
	print("Game over, Winning Team: %d" % (winning_team_index))


def deal_hands(deck: list[CardId], number_of_players: int) -> list[list[CardId]]:
	#print("Dealing hands")
	
	number_of_cards_per_player = int(len(deck) / number_of_players)

	hands: list[int] = [[] for _ in range(number_of_players)]

	for _ in range(number_of_cards_per_player):
		for player_index in range(number_of_players):
			card_id = random.choice(deck)
			hands[player_index].append(card_id)
			deck.remove(card_id)
	
	return hands


def get_next_turn_player_index(player_index: int, number_of_players: int) -> int:
	player_index += 1
	
	while player_index < 0:
		player_index += 1

	return player_index % number_of_players


def has_empress_been_played(played_cards: list[list[CardId]]) -> bool:
	for player_index in range(len(played_cards)):
		player_played_cards = get_player_played_cards(player_index, played_cards)
		if CardId.EMPRESS in player_played_cards:
			return True

	return False


##############################################################################
play_game()
