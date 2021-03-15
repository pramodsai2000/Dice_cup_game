import  random

class Die:
    """
    This class is Responsible for generating integer values between 1 and 6 for a die.

    Attributes:
        _value (int):   Value on top of a die.
    """
    def __init__(self):
        """The constructor for Die Class."""
        self.roll()

    def get_value(self) -> int:
        """
        This method returns the integer value on top of a die.

        Returns:
            _value (int): Value on top of a die.        
        """
        return self._value

    def roll(self):
        """This method assigns a random integer value to the top of a die."""
        self._value = random.randint(1,6)

class DiceCup:    
    """
    This class handles five objects (dice) of class Die and has the ability to bank and release dice.  
    Dice which are not banked are rolled in this class.

    Attributes:
        noofdice (int) : Number of dice used for playing the game.
        _dice    (list): List that stores the instances of the class Die.
    """
    def __init__(self,noofdice: int):
        """
        The constructor for DiceCup class.

        Parameters:
            noofdice (int): Number of dice used for playing the game. 
        """
        self.noofdice = noofdice
        self._dice = []        
        #creating die objects and storing them in _dice list
        count = 0 
        while count != noofdice: 
            self._dice_row = []
            die = Die()             
            self._dice_row.append(die)
            self._dice_row.append(False)
            self._dice.append(self._dice_row)
            count = count + 1

    def __iter__(self):
        """Dunder Method"""
        self.die_count = 0
        return self
    def __next__(self):
        """Dunder Method"""
        if self.die_count != self.noofdice:           
            self.ret_value = self._dice[self.die_count][1]
            self.die_count += 1
            return self.ret_value
        else:
            raise StopIteration

    def value(self,index: int) -> int:
        """
        This method returns an integer value on the top of each die.

        Parameters:
            index (int): An integer which is used to access the objects in _dice list

        Returns:
            int : The value on the top of a die with the given index.  
        """
        return self._dice[index][0].get_value()

    def bank(self,index: int):
        """
        This method bank a die with the given index as a parameter.

        Parameters:
            index (int): An integer which is used to access the objects in _dice list.
        """
        self._dice[index][1] = True

    def is_banked(self,index: int) -> bool:
        """
        This method returns the boolean value regarding whether the given die is banked or not.

        Parameters:
            index (int): An integer which is used to access the objects in _dice list.
        
        Returns:
            boolean: Returns True if the die is banked and False if the die is not banked. 
        """
        return self._dice[index][1]

    def release(self,index: int):
        """
        This method unbanks the die with the given index as a parameter.

        Parameters:
            index (int): Number which is used to access the instance in _dice list.
        """
        self._dice[index][1] = False

    def release_all(self):
        """All the dice is unbanked in this method."""
        for count in range(self.noofdice):
            self.release(count)

    #rolling unbanked dice
    def roll(self):
        """Unbanked dice are rolled in this method"""
        for die_count in range(len(self._dice)):

            if(self._dice[die_count][1]==True):
                pass            
            else:
                self._dice[die_count][0].roll()      

class ShipOfFoolsGame:
    """
    This ShipOfFoolsGame Class is responsible for the game logic.
    This class has the ability to play three rounds of the game for each player. 
    _winning_score is also given in this class. 

    Attributes:
        _cup (Object): Object of the class DieCup.
        _winning_score (int): An integer which is used to terminate the game.    
    """
    def __init__(self):
        """This is the constructor for ShipOfFoolsGame class."""
        self._cup = DiceCup(5)
        #winning score is set to 21
        self._winning_score = 21

    def round(self) -> int:
        """
        This method is responsible for the execution of the game.
        It contains the game logic.

        Returns:
            int: Returns individual score of each player after 3 rounds of game.
        """
        has_ship = False
        has_captain = False
        has_crew = False
        bank_count = 0               
        #using iterators to perform 3 rounds of game.
        iterable_value = [1,2,3]
        iterable_object = iter(iterable_value)    
        while True:
            try:
                round_count = next(iterable_object)
                if round_count == 1:
                    for each in list(DiceCup(5)):
                        if each == False:
                            bank_count += 1
                        if bank_count == 5:
                            print("All dice are unbanked")
                self._cup.roll()
                # Ship is not banked. 
                if not has_ship:
                
                    for die_count in range(len(self._cup._dice)):
                        if self._cup.value(die_count) == 6:
                            self._cup.bank(die_count)
                            has_ship = True
                            break    
                # Ship is banked but captainis not banked.              
                if has_ship and not has_captain:

                    for die_count in range(len(self._cup._dice)):
                        if self._cup.value(die_count) == 5:
                            self._cup.bank(die_count)
                            has_captain = True
                            break
                # Ship and captain are banked but not the crew.
                if has_captain and not has_crew:

                    for die_count in range(len(self._cup._dice)):
                        if self._cup.value(die_count) == 4:
                            self._cup.bank(die_count)
                            has_crew = True
                            break
                #All ship, captain and crew are banked and maximum cargo is considered.
                if has_ship and has_captain and has_crew:
                    for die_count in range(len(self._cup._dice)):
                        if not self._cup.is_banked(die_count) and self._cup.value(die_count) > 3:
                            self._cup.bank(die_count)
                #list to store the rolled values
                rolled_values = []

                for die_count in range(len(self._cup._dice)):                    
                    rolled_values.append(self._cup.value(die_count))             
                print("\t",rolled_values)
                print('********Round',round_count,'Complete********')
                #returning the Score of player in a chance.
                total = 0 
                cargo = 0
                if has_ship and has_captain and has_crew:     

                    for count in range(len(self._cup._dice)):
                        total = total + self._cup.value(count)
                    cargo = total - 15
                #Checking if all dice are banked.
                bank_check = 0
                for die_count in range(len(self._cup._dice)):
                    if self._cup.is_banked(die_count):
                        bank_check = bank_check +1
                if bank_check == len(self._cup._dice):
                    break
            except StopIteration:
                break
        print('\t\t**********Player Chance complete**********')
        return cargo

class PlayRoom:
    """ This PlayRoom class handles players and whole game. 
    PlayRoom is a playing area where the players play game and thier scores are compared to the winning score.
    This class has an aggregation relationship with the ShipOfFoolsGame class.

    Attributes:
        _players (list): list of players playing the game.
        _game (object): Object of the class ShipOfFoolsGame.
    """
    def __init__(self):
        """This is the constructor for PlayRoom class"""
        #creating the list _players to store the game players.
        self._players = []

    #setting the game
    def set_game(self, game: object):
        """
        This set method sets the game by creating the object of ShipOfFoolsGame class.

        Parameters:
            _game (object): Object of the class ShipOfFoolsGame.
        """
        self._game = game
    #adding the player into the game
    def add_player(self,player: object):
        """
        This method add players in _players list.

        Parameters:
            player (object): Instance of the class Player.
        """
        self._players.append(player)      
    #resetting the score
    def reset_scores(self):
        """The score of all players is set to 0 in this method."""
        for players_count in range(len(self._players)):
            self._players[players_count].reset_score()

    def play_round(self):
        """Each player plays game rounds in this method"""
        for players_count in range(len(self._players)):
             self._players[players_count].play_round(self._game)
             self._game._cup.release_all()

    def game_finished(self) -> bool:
        """
        A boolean value is returned refering to whether the game is finished or not in this method.

        Returns:
            boolean: True if the player score > winning score, False if the player score < winning score.  
        """
        #if any player gets the score more than winning_score the game ends
        for player in self._players:
            if player._score >= self._game._winning_score:
                return True
        else:
            return False

    def print_scores(self):
        """Score of each player is printed in this method."""
        for players_count in range(len(self._players)):
           print('Score of',self._players[players_count]._name,':',self._players[players_count]._score)

    def print_winner(self):
        """Prints whether a winner is emerged or a tie occured"""
        max_score = 0
        #list for storing the players with same max_scores 
        draw_list = []
        
        for players_count in range(len(self._players)):    

            if self._players[players_count]._score > max_score:
                max_score = self._players[players_count]._score

        for players_count in range(len(self._players)):

            if self._players[players_count]._score == max_score:
                draw_list.append(self._players[players_count]._name)

        if len(draw_list) == 1:
            print('And the winner is',draw_list[0],'!!!')

        else:
            print('Game is draw for players',draw_list)

class Player:
    """  
    This player class is responsible for executing the game for individual player. 
    This Class corresponds to each player in the game. Each players data is stored in this class.

    Attributes: 
        _name (str): name of player
        _score (int): Score of the player
    """
    def __init__(self,namestring: str):
        """ The constructor for Player class.

        parameters:
             namestring (str): name of player.
        """            
        self._name = str()
        self._score = 0
        self.set_name(namestring)

    def set_name(self,namestring: str):
        """
        This method sets the name of the player.

        Parameters:
             namestring (str): name of player.
        """
        self._name = namestring

    def current_score(self):
        """Current score of a player is updated in this method."""
        self._score = self._score + self.round_score

    def reset_score(self):
        """The score of the player is set to 0 in this method."""
        self._score = 0

    def play_round(self,game: object): 
        """
        This method is responsible for the whole game to play i.e runs three round of game for each player 
        and updates scores until the winner is emerged.

        Parameters:
            game (object): Object of the Class ShipOfFoolsGame.
        """
        self.round_score = game.round()  
        self.current_score()

if __name__ == "__main__":
    """This is main method of the Program."""
    room = PlayRoom()
    room.set_game(ShipOfFoolsGame())
    room.add_player(Player('Ling'))
    room.add_player(Player('Chang'))
    room.add_player(Player('pramod'))
    room.reset_scores()
    while not room.game_finished():
        room.play_round()
        room.print_scores()
    room.print_winner()
    