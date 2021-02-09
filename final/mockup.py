LION_MOVES_FROM_POSITION = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}}


class Tree:
    def __init__(self, data):
        """
        The head will be the initial position of the lion, then each children will be the action that the animals
        did for example {"impala": "drink_water", "lion": "move_west"}.
        """
        self.children = []
        self.data = data

    def search_knowledge(self, initial_position, impala_move, lion_move):
        """
        Check all the tree to check if something similar already happened.
        :return:
        """

    def save_knowledge(self):
        """
        Save everything on a txt file that can be loaded before.
        :return:
        """

    def load_knowledge(self):
        """
        Load tree of knowledge to add new data or use it to hunt.
        :return:
        """
        ...


class Board:

    def __init__(self):
        """
        Init board with 8 positions, take in account lake and set Imapla in place.
        """
        ...

    def __str__(self):
        """
        Print board.
        """
        ...

    def update_board(self):
        """
        Update board if someone moves, remove old representation of the element.
        """
        ...

    def distance_between(self):
        """
        Check distance between lion and impala. Check everything around and take the smaller distance.
        """
        ...


class Impala:

    def __init__(self, board):
        """
        init impala with the position.
        :param board: board object.
        """
        ...

    def move(self):
        """
        Random choice of movements.
        :return:
        """
        ...

    def scape(self):
        """
        Scape to the right or left if depends on the lion position. If the lion is on the center the scape should be a
        random decision.

        Some maths should make this easy. Depending how far is the lion that we should "simulate" the scape or just
        decide.
        :return:
        """
        ...


class Lion:
    """
    Notes: Always track lion position.
    """

    def __init__(self, board, position):
        """
        Init lion on board.
        """
        ...

    def move(self):
        """
        Using the tree that handles the knowledge choose a move. If no knowledge provided choose it random.
        Should validate the lake spaces.

        Define for each position the spaces where the lion can move. (Hardcode them)

        Update board.
        :return:
        """
        ...

    def attack(self):
        """
        Depends on the position if the lions attack and reaches the impala. Should be something easy using maths.
        :return:
        """
        ...


def main():
    """
    Core handler of the program. Should load knowledge from the beginning. Handle if the file exists or not.
    :return:
    """
    ...


def interactive_menu():
    """
    Allows some decisions:
    1. Step by step hunt
    2. Train. (take input from user)
    3. Download knowledge.
    4. Save knowledge
    5. Stop (save knowledge)
    :return:
    """
    ...


def simulate_hunt():
    """
    Check if is an automatic hunt or a step by step hunt.
    start lion, impala and board.
    start tree
    while True: -> for the time the user asked or each fail or success ask to continue or no.
        check if impala runs:
            run and return success or fail (store result, store result for Lion).
        else:
            move impala
        look for lion knowledge
        if knowledge:
            use knowledge to move lion
            check if lion attacks:
                run and return success or fail (store result, store result for Lion).
            else:
                move lion
        else:
            random move lion.
        store child node with new moves.
        move tree head.
    """
    ...
