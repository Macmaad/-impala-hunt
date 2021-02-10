import random


class Knowledge:
    def __init__(self, position):
        """
        The head will be the initial position of the lion, then each children will be the action that the animals
        did for example {"impala": "drink_water", "lion": "move_west"}.
        """
        self.data = dict()
        self.position = position

    def search_knowledge(self, impala_move, lion_move, distance_between):
        """
        Check all the tree to check if something similar already happened. If something match, look for the fastest
        way to get a success result and follow that path.
        :return:
        """
        ...

    def save_knowledge(self, impala_move, lion_move, distance_between):
        """
        Save everything on a txt file that can be loaded before.
        :return:
        """
        ...

    def load_knowledge(self):
        """
        Load tree of knowledge to add new data or use it to hunt.
        :return:
        """
        ...


def need_to_escape(distance_between):
    """
    Handles logic to see if the impala needs to run from the lion.
    :param distance_between:
    :return: bool
    """
    return distance_between < 3


class Impala:

    def __init__(self):
        """
        init impala with the position.
        """
        self.impala_moves = ["look_right", "look_left", "look_up", "drink_water"]

    def move(self, distance_from_lion):
        """
        Random choice of movements.
        :return:
        """
        if not need_to_escape(distance_from_lion):
            impala_move = random.choice(self.impala_moves)
        else:
            impala_move = "escape"
        return impala_move


def set_initial_distance(initial_position):
    """
    :param initial_position: int parameter to set the distance between the lion and the impala at the beginning
    this value will change with the time.
    :return:
    """
    initial_distance = None
    if initial_position == 1:
        initial_distance = 15

    elif initial_position in (2, 8):
        initial_distance = 12

    elif initial_position in (3, 4, 5, 6, 7):
        initial_distance = 9

    return initial_distance


def look_for_knowledge(tree_head, position, distance_between):
    ...


class Lion:
    """
    Notes: Always track lion position.
    """

    def __init__(self, position):
        """
        Init lion on board.
        """
        self.position = position
        self.distance_to_impala = set_initial_distance(position)
        self.lion_moves = ["move", "hide", "attack"]

    def move(self, tree_node):
        """
        Using the tree that handles the knowledge choose a move. If no knowledge provided choose it random.
        Should validate the lake spaces.

        Define for each position the spaces where the lion can move. (Hardcode them)

        Update board.
        :return:
        """
        lion_move = random.choice(self.lion_moves)  # this is temporal until we can load the knowledge.

        if lion_move == "move":
            self.distance_to_impala = self.distance_to_impala - 1

        return lion_move


def main():
    """
    Core handler of the program. Should load knowledge from the beginning. Handle if the file exists or not.
    :return:
    """
    ...


def lion_was_seen(impala_move, lion_move, initial_position):
    seen = False
    if impala_move == "look_right" and lion_move != "hide" and initial_position in (2, 3, 4):
        seen = True

    elif impala_move == "look_up" and lion_move != "hide" and initial_position in (1, 2, 8):
        seen = True

    elif impala_move == "look_left" and lion_move != "hide" and initial_position in (6, 7, 8):
        seen = True

    return seen


def interactive_menu():
    """
    Allows some decisions:
    1. Step by step hunt
    2. Train. (take input from user)
    3. Download knowledge.
    4. Save knowledge
    5. Stop (save knowledge)
    :return: int with option.
    """
    ...


def escape_success(distance_between):
    if distance_between == 3:
        incursion_status = True
    else:
        incursion_status = False

    return incursion_status


def simulate_hunt(initial_position):
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
    incursion_status, lion_move, impala_move, finish = True, None, None, False
    knowledge = Knowledge(initial_position)
    impala = Impala()
    lion = Lion(initial_position)

    while True:
        distance_between = lion.distance_to_impala
        was_seen = lion_was_seen(impala_move, lion_move, distance_between)
        if was_seen:
            finish = True
            incursion_status = escape_success(distance_between)

        if not finish:
            impala_move = impala.move(distance_between)
            if impala_move == "scape":
                finish = True
                incursion_status = escape_success(distance_between)

        if not finish:
            lion_move = lion.move(tree_head)
            if lion_move == "attack":
                finish = True
                incursion_status = escape_success(distance_between)

        if finish:
            # Store incursion
            print(lion_move, impala_move, incursion_status)
            user_input = int(input("Continue 1=yes/2=no"))
            if user_input == 2:
                break
        print(lion_move, impala_move, incursion_status)


simulate_hunt(3)
