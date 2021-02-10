import random


class Knowledge:
    def __init__(self, position):
        """
        The head will be the initial position of the lion, then each children will be the action that the animals
        did for example {"impala": "drink_water", "lion": "move_west"}.
        """
        self.data = dict()
        self.position = position

    def search_knowledge(self, impala_move, distance_between):
        """
        Check all the tree to check if something similar already happened. If something match, look for the fastest
        way to get a success result and follow that path.
        :return: valid moves.
        """
        lion_moves, do_not_use = ["move", "hide", "attack"], []
        if self.data.get(self.position):
            inner_data = self.data[self.position]
            if inner_data.get(distance_between):
                inner_data = inner_data[distance_between]
                if inner_data.get(False):
                    inner_data = inner_data[False]
                    if inner_data.get(impala_move):
                        do_not_use = inner_data[impala_move]
        return list(set(lion_moves) - set(do_not_use))

    def update_knowledge(self, impala_move, lion_move, distance_between, incursion_status):
        """
        Save everything on a txt file that can be loaded before.
        :return:
        """
        if self.data.get(self.position):
            inner_object = self.data[self.position]
            if inner_object.get(distance_between):
                inner_object = inner_object[distance_between]
                if inner_object.get(incursion_status) is not None:
                    inner_object = inner_object[incursion_status]
                    if inner_object.get(impala_move):
                        inner_object = self.data[self.position][distance_between][incursion_status]
                        if lion_move not in inner_object[impala_move]:
                            self.data[self.position][distance_between][incursion_status][impala_move].append(lion_move)
                    else:
                        self.data[self.position][distance_between][incursion_status].update({impala_move: [lion_move]})

                else:
                    self.data[self.position][distance_between].update({incursion_status: {impala_move: [lion_move]}})

            else:
                self.data[self.position].update({distance_between: {incursion_status: {impala_move: [lion_move]}}})

        else:
            self.data.update({self.position: {distance_between: {incursion_status: {impala_move: [lion_move]}}}})

    def load_knowledge(self):
        """
        Load tree of knowledge to add new data or use it to hunt.
        :return:
        """
        ...

    def save_knowldge(self):
        """

        :return:
        """


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

    def move(self, lion_moves):
        """
        Using the tree that handles the knowledge choose a move. If no knowledge provided choose it random.
        Should validate the lake spaces.

        Define for each position the spaces where the lion can move. (Hardcode them)

        Update board.
        :return:
        """
        lion_move = random.choice(lion_moves)  # this is temporal until we can load the knowledge.

        if lion_move == "move":
            self.distance_to_impala = self.distance_to_impala - 1

        return lion_move


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
    knowledge = Knowledge(initial_position)
    incursions, wins = 0, 0
    while True:
        incursions += 1
        hunt_status, lion_move, impala_move, finish = True, None, None, False
        impala = Impala()
        lion = Lion(initial_position)

        while True:
            distance_between = lion.distance_to_impala
            was_seen = lion_was_seen(impala_move, lion_move, initial_position)
            if was_seen:
                finish = True
                hunt_status = escape_success(distance_between)
                knowledge.update_knowledge(impala_move, lion_move, distance_between, hunt_status)

            if not finish:
                impala_move = impala.move(distance_between)
                if impala_move == "escape":
                    finish = True
                    hunt_status = escape_success(distance_between)
                    knowledge.update_knowledge(impala_move, lion_move, distance_between, hunt_status)

            if not finish:
                lion_moves = knowledge.search_knowledge(impala_move, distance_between)
                lion_move = lion.move(lion_moves)
                if lion_move == "attack":
                    finish = True
                    hunt_status = escape_success(distance_between)
                    knowledge.update_knowledge(impala_move, lion_move, distance_between, hunt_status)

            if finish:
                if hunt_status:
                    wins += 1
                break
            print(lion_move, impala_move, hunt_status)

        user_input = 1  # int(input("Continue 1=yes/2=no"))
        if user_input == 2:
            break


def main():
    """
    Core handler of the program. Should load knowledge from the beginning. Handle if the file exists or not.
    :return:
    """
    ...


simulate_hunt(3)
