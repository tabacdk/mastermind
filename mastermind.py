
"""\
Mastermind, the game

This is an implementation of the classic board game in Python. The focus of
the implementation is on strong typing, testing, and validation. The user
interface is rudimentary, but it has not been the focus of the
implementation.
"""

import typing as t
import enum
import collections
import random

DEBUG : bool = True

class Pin(enum.Enum):
    """The pins are used as the code and the guesses.
    """
    BLACK = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    WHITE = 5

class Mark(enum.Enum):
    """The marks are used for feedback in comparing the code and the guess.
    """
    BLANK = 0
    WHITE = 1
    BLACK = 2

Combination = t.Tuple[Pin, Pin, Pin, Pin]
Combination.__doc__ = """\
The Combination is a tuple four Pins.

It is used for the code as well as for the guess.
"""

Marking = collections.namedtuple('Marking', ['blacks', 'whites', 'blanks'])
Marking.__doc__ = """\
The Marking is the number of black, white, and blank Marks.

The Marking is the feedback for the guess compared to the code.
"""

Row = t.Tuple[Combination, Marking]
Row.__doc__ = """\
The Row is a pair of a particular guess Combination and the adhering Marking.

The Game keeps track of the guesses and markings through the gameplay.
"""

def calc_marking(code: Combination, guess: Combination) -> Marking:
    """Calculates the Marking of a guess against a code

    code: The code of the game
    guess: The actual guess

    Returns: The Marking
    """
    blacks = 0
    whites = 0
    code_remains = []
    guess_remains = []
    for code_element, guess_element in zip(code, guess):
        if code_element == guess_element:
            blacks += 1
        else:
            code_remains.append(code_element)
            guess_remains.append(guess_element)
    for guess_element in guess_remains:
        if guess_element in code_remains:
            whites += 1
            code_remains.remove(guess_element)
    blanks = 4 - blacks - whites
    return Marking(blacks, whites, blanks)

def get_code() -> Combination:
    """Creates a random code Combination

    Returns: a random Combination
    """
    code : Combination = (
        random.choice(list(Pin)), random.choice(list(Pin)),
        random.choice(list(Pin)), random.choice(list(Pin))
    )
    return code

def str2combination(input_string : str) -> Combination:
    """Converts a string of four digits into a Combination

    input_string: The input string

    Returns: The combination

    Raises: ValueError
    """
    input_list = list(input_string)
    if len(input_list) != 4:
        raise ValueError("Bad number of pins")
    combi : Combination = (
        Pin(int(input_list[0])),
        Pin(int(input_list[1])),
        Pin(int(input_list[2])),
        Pin(int(input_list[3]))
    )
    return combi

class Game:
    """A game simutation.

    Simulates a game og Mastermind with the instance as the code setter and
    the user/caller as the code guesser.
    """
    def __init__(self, turns: int = 12, code : t.Optional[Combination] = None):
        self.code : Combination
        if code is None:
            self.code = get_code()
        else:
            self.code = code
        self.rows : t.List[Row] = []
        self.turns : int = turns
        self.finished : bool = False
        self.won : bool = False

    def print_board(self) -> str:
        """Returns a string representation of the actual board.
        """
        out : str = ''
        if DEBUG:
            out += f'The code is {self.code}\n'
        for row in self.rows:
            for guess in row[0]:
                out += f'| {guess:10} '
            out += f'| {str(row[1]):25} |\n'
        out += f'You have {self.turns} guess(es) remaining'
        return out

    def submit_guess(self, guess: Combination):
        """Allows the user/caller to submit a guess.

        The guess is evaluated against the code and markings are set.
        It is furthermore evaluated if the game is over and if the game is
        won by the user/caller.
        """
        marking : Marking = calc_marking(self.code, guess)
        row : Row = (guess, marking)
        self.rows.append(row)
        self.turns -= 1
        if marking.blacks == 4:
            self.finished = True
            self.won = True
        elif self.turns == 0:
            self.finished = True
            self.won = False

    def is_finished(self):
        """Predicate for whether the game is over.
        """
        return self.finished

    def is_won(self):
        """Predicate for whether the game is won by the user/caller.
        """
        return self.won

def main():
    """The main function.
    """
    while True:
        game : Game = Game()
        while True:
            print(game.print_board())
            print("Black=0, Red=1, Green=2, Blue=3, Yellow=4, White=5")
            guess_text = input('Enter your guess as xxxx : ')
            try:
                guess : Combination = str2combination(guess_text)
            except ValueError:
                print("Your input was ill-formed, please try again ...")
                continue
            game.submit_guess(guess)
            if game.is_finished():
                if game.is_won():
                    print("Congratulations, you won!")
                else:
                    print("Too bad, you lost ...")
                break
        answer: str = input("Play again (y/n) ? ")
        if answer == 'n':
            print("Bye ...")
            break

if __name__ == "__main__":
    main()
