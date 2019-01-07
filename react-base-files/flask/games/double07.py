#!/usr/bin/python3
'''
Double07 game class
'''
from queue import Queue, PriorityQueue
from __game import Game

class Double07(Game):
    '''
    Class Attributes:
        the queue methods are used to sequence game moves by priority, not timing.
    '''
    __attack_queue = Queue()
    __target_queue = Queue()
    __other_queue = Queue()

    def __init__(self, players, timer=15, **kwargs):
        '''
        Sets up the games default parameters.
        '''
        def init_state(players):
            '''
            Setups the game state for each player with default parameters.
            '''
            for player in players:
                self.state[player] = {'hp' : 3, 'ap': 1, 'defend': 'none'}

        super().__init__(players, **kwargs)
        if self.socketio:
            self.socketio.on_event('endOfRound', self.action)
        init_state(self.players)
        self.__timer = timer

    def action(self, data):
        '''
        Inherited from Game. Handles controller input.
        In Double07, passes off input to a series of queues for later processing.
        '''
        print(data)
        if data['action'] == "attack":
            self.__attack_queue.put((data['player'], data['target']))
            self.__target_queue.put((data['player'], data['target']))
        else:
            self.__other_queue.put((data['player'], data['action']))


    def end_round(self):
        '''
        Inherited from Game. Handles game at the end of a round.
        Processes the queues one at a time to prioritize actions.
        First two queues setup defenses and reloads (not exclusively).
        Last queue handles attacks.
        '''
        while not self.__other_queue.empty():
            player, action = self.__other_queue.get()
            getattr(self, '_'+self.__name__+'__' + action)(player)
        while not self.__target_queue.empty():
            self.__target(*self.__target_queue.get())
        while not self.__attack_queue.empty():
            self.__attack(*self.__attack_queue.get())
        self.rank_players()
        self.display()
        if self.display_game:
            self.display_game.update(self.deepcopy)


    def display(self):
        '''
        Displays the game state to the console.
        '''
        print(self.state)
        if not self.active:
            self.print_standings()

    def run_game(self):
        '''
        Function that runs the gameloop from the server.
        '''
        while self.active:
            self.socketio.emit('state', self.state, broadcast=True)
            timer = self.timer
            while self.timer > 0:
                self.socketio.sleep(1)
                print(self.timer)
                self.timer -= 1
            self.socketio.emit('timerExpired', broadcast=True)
            self.timer = timer
            print("Waiting for inputs")
            self.socketio.sleep(1)
            print("Times up")
            self.end_round()
        print("Game Over")
        self.socketio.emit('gameOver', broadcast=True)

    @property
    def timer(self):
        '''
        Local timer object
        '''
        return self.__timer

    @timer.setter
    def timer(self, value):
        self.__timer = value

    @timer.deleter
    def timer(self):
        del self.__timer

    def __defend(self, player):
        '''
        Handles logic for the defend action.
        '''
        self.state[player]['defend'] = "all"
        self.state[player]['ap'] -= 1

    def __reload(self, player):
        '''
        Handles logic for the reload action.
        '''
        self.state[player]['defend'] = "none"
        self.state[player]['ap'] += 1

    def __target(self, player, target):
        '''
        Handles defend logic for attack action.
        Sets defense to attacker to prevent double attacks.
        '''
        self.state[player]['defend'] = target

    def __attack(self, player, target):
        '''
        Handles logic attack action.
        Handles different cases of success/failure.
        '''
        if self.state[target]['defend'] == "all":
            self.state[target]['ap'] += 1
            self.state[player]['ap'] -= 1
        elif self.state[target]['defend'] == player:
            self.state[player]['ap'] -= 1
        else:
            self.state[target]['hp'] -= 1

    def rank_players(self):
        '''
        Ranks players based on order of death.
        Simultaneous deaths are tie-broken by the player with greater AP.
            If that is tied, it is broken arbitrarily
            (pretty sure reverse alphabetical order kicks in)
        '''
        dead = PriorityQueue()
        def check_dead():
            '''
            A local function to __rank_players().
            Adds players to ranking queue if they are dead.
            '''
            for player, stats in self.state.items():
                if stats['hp'] != 'dead' and stats['hp'] <= 0:
                    dead.put((stats['ap'], player))
                    self.state[player]['hp'] = 'dead'
            while not dead.empty():
                self.add_ranks(dead.get()[1])

        def check_alive():
            '''
            A local function to __rank_players().
            Returns a list of living players.
            '''
            for player, stats in self.state.items():
                if stats['hp'] != 'dead':
                    yield player

        check_dead()
        alive = list(check_alive())
        if len(alive) < 2:
            for player in alive:
                self.add_ranks(player)
            self.end_game()

if __name__ == '__main__':
    GAME = Double07(['A', 'B', 'C'])
    GAME.display()
    GAME.action({'player': "C", 'action': 'defend'})
    GAME.action({'player': "B", 'action': 'reload'})
    GAME.action({'player': "A", 'action': 'attack', 'target': 'B'})
    GAME.end_round()    #test hit
    GAME.action({'player': "A", 'action': 'attack', 'target': 'B'})
    GAME.action({'player': "B", 'action': 'defend'})
    GAME.action({'player': "C", 'action': 'reload'})
    GAME.end_round()    # test defend
    GAME.action({'player': "A", 'action': 'reload'})
    GAME.action({'player': "B", 'action': 'attack', 'target': 'C'})
    GAME.action({'player': "C", 'action': 'attack', 'target': 'B'})
    GAME.end_round() # test simultaneous fire
    GAME.action({'player': "C", 'action': 'reload'})
    GAME.action({'player': "B", 'action': 'attack', 'target': 'C'})
    GAME.action({'player': "A", 'action': 'attack', 'target': 'B'})
    GAME.end_round()    # test hit
    GAME.action({'player': "C", 'action': 'attack', 'target': 'A'})
    GAME.action({'player': "B", 'action': 'attack', 'target': 'C'})
    GAME.action({'player': "A", 'action': 'attack', 'target': 'B'})
    GAME.end_round()    # test 3 way hit and death
    GAME.action({'player': "A", 'action': 'attack', 'target':'C'})
    GAME.action({'player': "C", 'action': 'reload'})
    GAME.end_round()   # should trigger end game

    GAME = Double07(['A', 'B', 'C'])
    GAME.action({'player': "A", 'action': 'reload'})
    GAME.action({'player': "C", 'action': 'defend'})
    GAME.action({'player': "B", 'action': 'reload'})
    GAME.end_round()
    GAME.action({'player': "A", 'action': 'defend'})
    GAME.action({'player': "C", 'action': 'reload'})
    GAME.action({'player': "B", 'action': 'reload'})
    GAME.end_round()
    GAME.action({'player': "C", 'action': 'attack', 'target': 'A'})
    GAME.action({'player': "B", 'action': 'attack', 'target': 'C'})
    GAME.action({'player': "A", 'action': 'attack', 'target': 'B'})
    GAME.end_round()
    GAME.action({'player': "C", 'action': 'attack', 'target': 'A'})
    GAME.action({'player': "B", 'action': 'attack', 'target': 'C'})
    GAME.action({'player': "A", 'action': 'attack', 'target': 'B'})
    GAME.end_round()
    GAME.action({'player': "C", 'action': 'attack', 'target': 'A'})
    GAME.action({'player': "B", 'action': 'attack', 'target': 'C'})
    GAME.action({'player': "A", 'action': 'attack', 'target': 'B'})
    GAME.end_round()   #triple kill

    GAME = Double07(map(chr, range(ord('a'), ord('z')+1)))
    GAME.display()
