
import random

# print whose turn, how many cards each player has, and prompt user for card, return that card


def check_win(player_hand):
    # might move this to driver since it just checks if the hand size is 0
    pass


def sort_hands(hands):
    for each in hands:
        each.sort()
    return hands


def wait_for_player():
    while True:
        input("Press enter to continue...")
        break


def get_number_of_players(manual=None):
    if manual:
        return manual
    while True:
        number_of_players = int(
            input("How many computer players would you like (1-3): "))
        if number_of_players in range(1, 4):
            number_of_players += 1  # because input is for computer players
            break
        print("That is not a valid selection")
    return number_of_players


def get_hand_size(manual=None):
    if manual:
        return manual
    while True:
        size_of_hands = int(
            input("What hand size would you like each player to start with (5-7): "))
        if size_of_hands in range(5, 8):
            break
        print("That is not a valid selection")
    return size_of_hands


def get_card_from_user(card_numbers, cards_in_hand):
    while True:
        selected_card = input(
            "Which card number would you like to guess (2 to A)?: ")
        selected_card = selected_card.upper()
        if (selected_card in card_numbers) and (selected_card in cards_in_hand):
            return selected_card
        print("Input must be a valid card and in your hand.")


def get_selected_player_from_user(number_of_players):
    while True:
        selected_player = int(input(
            "Which player would you like to fish from (1 to {0})?:  ".format(number_of_players - 1)))
        if selected_player in range(1, number_of_players):
            return selected_player
        print("That is an invalid player number")


def create_deck(card_numbers, coats):
    pond = []
    for card_number in card_numbers:
        for coat in coats:
            pond.append((card_number, coat))
    random.shuffle(pond)
    return pond


def get_largest_hand_player(hands, current_player):
    largest_hand_player = 0
    largest_hand = 0
    for each in hands:
        if len(each) >= largest_hand and hands.index(each) != current_player:
            largest_hand_player = hands.index(each)
            largest_hand = len(each)
    return largest_hand_player


def four_of_a_kind_check(hands, current_player):
    previous_card = None
    matcher = None
    sort_hands(hands)
    for each in hands[current_player]:
        # print(each[0])
        if each[0] == previous_card:
            matcher += 1
            previous_card = each[0]
        else:
            matcher = 0
            previous_card = each[0]

        if matcher == 3:
            print("Player {0} has 4 X {1}'s!".format(
                current_player, each[0]))
            return each[0]


def remove_four_of_kind(hands, current_player, four_of_kind_card):
    j = len(hands[current_player])
    i = 0
    # could not use list remove method because it would remove and shift to the next, skipping card checks
    while i != j and (len(hands[current_player]) != 0):
        if hands[current_player][i][0] == four_of_kind_card:
            hands[current_player].remove(hands[current_player][i])
            j -= 1
        else:
            i += 1
    return hands


def check_win_condition(hands, current_player):
    if len(hands[current_player]) == 0:
        print("Player {0} has no cards left and wins the game!".format(
            current_player))
        wait_for_player()
        return True
    return False


def check_for_matches(hands, selected_player, selected_card):
    matched_cards = []
    for each in hands[selected_player]:
        if (selected_card in each):
            matched_cards.append(each)
    return matched_cards
