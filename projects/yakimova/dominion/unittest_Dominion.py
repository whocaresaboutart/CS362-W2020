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