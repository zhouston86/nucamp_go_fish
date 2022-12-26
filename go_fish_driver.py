# TODO: Refactoring.

# nice to have - replace player 0 messages with "Your"
# nice to have - try to use some lambda functions
# nice to have - make more OOP structured (next revision)


import random
import go_fish_modules
import time


# set for testing during dev
testing = False
turn_rate = 0.2

# set for demo of code, where you can see all players hands, but user is still playing'
demo = False

# initiate game by selecting number of cards in hand and number of players
print("§~~~~ Welcome to Go Fish! ~~~~§")

if testing:
    number_of_players = go_fish_modules.get_number_of_players(3)
    size_of_hands = go_fish_modules.get_hand_size(6)
else:
    number_of_players = go_fish_modules.get_number_of_players()
    size_of_hands = go_fish_modules.get_hand_size()

# create "pond" deck
coats = ("C", "S", "H", "D")
card_numbers = ("2", "3", "4", "5", "6", "7", "8",
                "9", "10", "J", "Q", "K", "A")

pond = go_fish_modules.create_deck(card_numbers, coats)

# initialize hand. 2D list, where index 0 is user player, index 1 is comp 1, index 2 is comp 2, etc...
hands = [[0 for i in range(0, size_of_hands)]
         for j in range(0, number_of_players)]

# deal hands
for i in range(0, number_of_players):
    for j in range(0, size_of_hands):
        hands[i][j] = pond.pop()

# player's memory decks to remember previous guesses. Use sets because duplicates dont matter.
memories = [set() for i in range(0, number_of_players)]

# initalize some things
matched_cards = []
cards_in_hand = []
game_end = False
current_player = 0
selected_player = 1

# TODO nice to have - fix sort to be integer based instead of string
go_fish_modules.sort_hands(hands)


while game_end == False:

    # for testing/demo
    if testing or demo and current_player == 0:
        print("players current hands")
        for each in range(0, len(hands)):
            print(hands[each])

    if current_player == 0 and not testing:
        ### USER TURN ###

        print("\n§~~~~ Your Turn! ~~~~§")
        print("Your current hand:")
        print(hands[current_player])

        matched_cards.clear()
        cards_in_hand.clear()

        # get a list of numbers in hand to validate user input
        for each in hands[current_player]:
            cards_in_hand.append(each[0])

        # ask user for selected card and player
        selected_card = go_fish_modules.get_card_from_user(
            card_numbers, cards_in_hand)

        selected_player = go_fish_modules.get_selected_player_from_user(
            number_of_players)

        # save the guessed card in the other players memory
        memories[current_player].add(selected_card)

        matched_cards = go_fish_modules.check_for_matches(
            hands, selected_player, selected_card)

        if not matched_cards:
            if len(pond) != 0:
                print("No Match! Go fish!")
                fished_card = pond.pop()
                print("You fished a {0}".format(fished_card))
                hands[current_player].append(fished_card)
            else:
                print("No Match! No more cards in the pond!")
        else:
            print("Player {0} gave Player {1}".format(
                selected_player, current_player), ":", len(matched_cards), "X", selected_card, "'s")
            for match in matched_cards:
                hands[current_player].append(match)
                hands[selected_player].remove(match)

        if testing:
            print("For testing...")
            print("Player {0}'s new hand".format(current_player))
            print(hands[current_player])
            print("Player {0}'s new hand for testing".format(selected_player))
            print(hands[selected_player])

        if testing:
            print("Memory deck for testing...")
            print(memories)

    ### COMPUTER TURN ###
    if current_player != 0 or testing:

        selected_card = None
        matched_cards.clear()
        print("\n§~~~~ Computer Player {0}'s Turn! ~~~~§".format(
            current_player))

        if testing:
            print("Players hands for testing...")
            for each in range(0, len(hands)):
                print(hands[each])

        # TODO: Refactor
        # see if comp player has a card in memory that matches one in their hand, and use as selected card and player. if not, choose random card from hand and player with largest hand.

        for each in hands[current_player]:
            for player in memories:
                for number in player:
                    if number in each and memories.index(player) != current_player:
                        if testing:
                            print("Found current player card {0} in memory for player {1}.".format(
                                number, memories.index(player)))
                        selected_card = number
                        selected_player = memories.index(player)
                    elif selected_card == None:
                        if testing:
                            print("no player cards found in memory.")
                        selected_card = random.choice(
                            hands[current_player])[0]
                        selected_player = go_fish_modules.get_largest_hand_player(
                            hands, current_player)

        # ask for card
        print("Player {0} asks Player {1} for {2}'s".format(
            current_player, selected_player, selected_card))

        # save the guessed card in the other players memory
        memories[current_player].add(selected_card)
        if selected_card in memories[selected_player]:
            memories[selected_player].remove(selected_card)

        matched_cards = go_fish_modules.check_for_matches(
            hands, selected_player, selected_card)

        if not matched_cards:
            if len(pond) != 0:
                print("No Match! Go fish!")
                hands[current_player].append(pond.pop())
            else:
                print("No Match! No more cards in the pond!")
        else:
            print("Player {0} gave Player {1}".format(
                selected_player, current_player), ":", len(matched_cards), "X", selected_card, "'s")
            for match in matched_cards:
                hands[current_player].append(match)
                hands[selected_player].remove(match)

    ### ALL PLAYER TURN END FUNCTIONS ###

    go_fish_modules.sort_hands(hands)

    # Check for four of kind in player hand
    four_of_kind_card = None
    four_of_kind_card = go_fish_modules.four_of_a_kind_check(
        hands, current_player)

    if four_of_kind_card != None:
        go_fish_modules.remove_four_of_kind(
            hands, current_player, four_of_kind_card)
        if testing:
            print(hands[current_player])

    if go_fish_modules.check_win_condition(hands, current_player):
        game_end = True

    # If player has a match, gets to go again
    if four_of_kind_card == None:
        current_player += 1
        if current_player >= number_of_players:
            current_player = 0
    else:
        print("Player {0} sets down 4 of a kind and gets to go again!".format(
            current_player))

    if testing:
        time.sleep(turn_rate)
    else:
        go_fish_modules.wait_for_player()
