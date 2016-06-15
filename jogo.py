from truco import Card, Deck, Hand, CardCheck, Player, Pair, Game, Match, Round, MatchState, NormalMatch, TrucoMatch, SixMatch, NineMatch, TwelveMatch

def play_player(player, match, show_raise_option=None):

    end_match = False

    if(show_raise_option is None):
        show_raise_option = match.state.__class__ is not TwelveMatch
    
    if(show_raise_option and len(player.hand.cards) is not 0) :
        text_state = "0 - Pedir " + str(match.state.next().get_state_name() + "\n")
    else:
        text_state = "\n"

    print "\nVez de " + player.player_name + "\n"

    indexes = []
    for index, card in enumerate(player.hand.cards):
        indexes.append(index + 1)
        print str(index + 1) + " - " + str(card)
    
    print text_state
    card = raw_input()

    if(show_raise_option and int(card) == 0):
        accept = match.raise_match(player)
        if(accept is True):
            play_player(player, match, False)
        else:
            end_match = True
    elif(int(card) in indexes):
        player.throw_card(match=match, card_position=int(card))
    else:
        print "Entrada invalida"
        play_player(player, match)

    return end_match


if __name__ == '__main__':
    
    print "\t\nAIKE TRUCO\n"

    player_name = raw_input("Insira o nome do Jogador 1 da Dupla 1\n")
    player1 = Player(player_name)
    
    player_name = raw_input("Insira o nome do Jogador 2 da Dupla 1\n")
    player2 = Player(player_name)

    player_name = raw_input("Insira o nome do Jogador 1 da Dupla 2\n")
    player3 = Player(player_name)

    player_name = raw_input("Insira o nome do Jogador 2 da Dupla 2\n")
    player4 = Player(player_name)
    
    pair1 = {'player1': player1, 'player2': player2}
    pair_one = Pair(Pair.PAIR_ONE_ID, pair1)
    pair2 = {'player1': player3, 'player2': player4}
    pair_two = Pair(Pair.PAIR_TWO_ID, pair2)

    print "\n \t\t O jogo comecou! \n"

    game = Game([pair_one, pair_two])

    game.start()

    continue_game = True
    while continue_game:
        match =  game.current_match
        
        end_match = play_player(player1, match)
        if(end_match):
            continue
        else:
            end_match = play_player(player3, match)
            if(end_match):
                continue
            else:
                end_match = play_player(player2, match)
                if(end_match):
                    continue
                else:
                    play_player(player4, match)

        end_game = game.score[Pair.PAIR_ONE_ID] >= 12 or game.score[Pair.PAIR_TWO_ID] >= 12
        if(end_game):
            continue_game = False

    print "\t\t Fim do jogo!"
    game.print_score()
