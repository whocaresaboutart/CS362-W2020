from unittest import TestCase
import testUtility
import sys
from io import StringIO
import Dominion


class TestActionCard(TestCase):
    def dataSetUp(self):
        # Data setup
        self.player_names = ["*Annie", "Ben", "*Carla"]
        self.nV = testUtility.GetNumVictory(self.player_names)
        self.nC = testUtility.GetNumCurses(self.player_names)
        self.box = testUtility.GetBoxes(self.nV)
        self.supply_order = testUtility.GetSupplyOrder()
        #Setup supply with 5 cards
        self.supply = testUtility.GetSupply(self.box, self.nV, self.nC, len(self.player_names), 5)
        self.trash = []
        #set player
        self.player = Dominion.Player(self.player_names[1]) #Ben

    def test_init(self):
        #init data
        self.dataSetUp()
        cardName = "Smithy"
        cost = 4
        actions = 0
        cards = 3
        buys = 0
        coins = 0

        #initiate a Smithy action card object
        card = Dominion.Action_card(cardName,cost,actions,cards,buys,coins,)

        #verify that card class variables have the expected values
        self.assertEqual(cardName, card.name)
        self.assertEqual(cost, card.cost)
        self.assertEqual(actions, card.actions)
        self.assertEqual(cards, card.cards)
        self.assertEqual(buys, card.buys)
        self.assertEqual(coins, card.coins)
        self.assertEqual("action", card.category)

    def test_use(self):
        #init data
        self.dataSetUp()
        cardName = "Smithy"
        cost = 4
        actions = 0
        cards = 3
        buys = 0
        coins = 0

        #initiate a Smithy action card object
        card = Dominion.Action_card(cardName,cost,actions,cards,buys,coins,)

        #add card to hand
        self.player.hand.append(card)

        #Assert player has 6 cards in hand and has played no cards
        self.assertEqual(0, len(self.player.played))
        self.assertEqual(6, len(self.player.hand))

        #use the card
        card.use(self.player, self.trash)

        #Assert changes made
        self.assertEqual(1, len(self.player.played))
        self.assertEqual(5, len(self.player.hand))
        self.assertEqual("Smithy", self.player.played[0].name)


    def test_augment(self):
        # init data
        self.dataSetUp()
        cardName = "Smithy"
        cost = 4
        actions = 0
        cards = 3
        buys = 0
        coins = 0

        #do a trun to init some vars
        sys.stdin = StringIO('\n') #force hitting enter
        self.player.turn([], self.supply, self.trash)

        # initiate a Smithy action card object
        card = Dominion.Action_card(cardName, cost, actions, cards, buys, coins, )

        # add card to hand
        self.player.hand.append(card)

        # Assert player has 6 cards in hand and has played no cards
        self.assertEqual(0, len(self.player.played))
        self.assertEqual(6, len(self.player.hand))

        # use the card
        card.use(self.player, self.trash)
        card.augment(self.player)

        # Assert changes made
        self.assertEqual(1, len(self.player.played)) # played 1 card
        self.assertEqual(5 + cards, len(self.player.hand)) # drew 3 cards
        self.assertEqual(1 + actions, self.player.actions) # added 0 actions
        self.assertEqual(1 + buys, self.player.buys) # added 0 buys

class TestPlayer(TestCase):
    def dataSetUp(self):
        # Data setup
        self.player_names = ["*Annie", "Ben", "*Carla"]
        self.nV = testUtility.GetNumVictory(self.player_names)
        self.nC = testUtility.GetNumCurses(self.player_names)
        self.box = testUtility.GetBoxes(self.nV)
        self.supply_order = testUtility.GetSupplyOrder()
        #Setup supply with 5 cards
        self.supply = testUtility.GetSupply(self.box, self.nV, self.nC, len(self.player_names), 5)
        self.trash = []
        # set player
        self.player = Dominion.Player(self.player_names[1]) # Ben

    def test_actionBalance(self):
        # init data
        self.dataSetUp()

        # test before adding action cards
        self.assertEqual(0, self.player.action_balance()) # should be zero action cards

        # add 4 action cards
        self.player.deck += [Dominion.Smithy()] * 2 + [Dominion.Militia()] * 2

        # test new balance
        self.assertEqual(-20.0, self.player.action_balance()) # should now be -20.0

        # add 6 more action cards
        self.player.deck += [Dominion.Witch()] * 3 + [Dominion.Mine()] * 3

        # test new balance
        self.assertEqual(-35.0, self.player.action_balance()) # should now be -35.0

    def test_calcPoints(self):
        # init data
        self.dataSetUp()

        # test before adding action cards
        self.assertEqual(3, self.player.calcpoints()) # should be 3 from 3 estates

        # add 2 provinces (6 points each)
        self.player.deck += [Dominion.Province()] * 2

        # test calcPoints
        self.assertEqual(15, self.player.calcpoints())

        # add 2 Duchies (3 points each)
        self.player.deck += [Dominion.Duchy()] * 2

        # test calcPoints
        self.assertEqual(21, self.player.calcpoints())

        # add 6 gardens (2 points each)
        self.player.deck += [Dominion.Gardens()] * 6

        # test calcPoints
        self.assertEqual(33, self.player.calcpoints())

    def test_draw(self):
        # init data
        self.dataSetUp()

        # test before drawing cards
        self.assertEqual(5, len(self.player.hand))  # should be 5 original cards in hand
        self.assertEqual(5, len(self.player.deck))  # should be 5 original cards in deck
        self.assertEqual(0, len(self.player.discard))  # should be 0 original cards in discard pile

        # draw a card
        self.player.draw()

        # test
        self.assertEqual(6, len(self.player.hand))  # should be 6 cards in hand
        self.assertEqual(4, len(self.player.deck))
        self.assertEqual(0, len(self.player.discard))  # should be 0 original cards in discard pile

        # draw a card into the discard pile
        self.player.draw(self.player.discard)

        # test
        self.assertEqual(6, len(self.player.hand))  # should be 6 cards in hand
        self.assertEqual(3, len(self.player.deck))
        self.assertEqual(1, len(self.player.discard))  # should be 1 card in discard pile

    def test_cardSummary(self):
        # init data
        self.dataSetUp()

        # get summary after setup
        summary = self.player.cardsummary()

        # test
        self.assertEqual(3, summary['VICTORY POINTS'])  # Test for 3 victory points
        self.assertEqual(7, summary['Copper'])  # Test for 7 copper cards
        self.assertEqual(3, summary['Estate'])  # Test for 3 Estate cards

        # add some cards to the deck
        self.player.deck += [Dominion.Smithy()] * 2
        self.player.deck += [Dominion.Duchy()] * 5
        self.player.deck += [Dominion.Bureaucrat()] * 9

        # get new summary
        summary = self.player.cardsummary()

        # test for the added card plus the old ones
        self.assertEqual(7, summary['Copper'])  # Test for 7 copper cards
        self.assertEqual(3, summary['Estate'])  # Test for 3 Estate cards
        self.assertEqual(2, summary['Smithy'])
        self.assertEqual(5, summary['Duchy'])
        self.assertEqual(9, summary['Bureaucrat'])