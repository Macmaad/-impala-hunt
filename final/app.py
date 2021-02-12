import random
import json
import os


def translate_knowledge(data):
    """
    :param data: Complete dictionary with all the data of the lion knowledge
    :return: Creates file that can be easy read for a human.
    """
    path = "./human_friendly_knowledge.txt"
    if os.path.exists(path):
        os.remove(path)
    with open(path, "w") as knowledge_file:
        for initial_distances in data.keys():
            knowledge_file.write(f"Initial position of lion: {initial_distances}\n")
            for distance_from_impala in data[initial_distances].keys():
                knowledge_file.write(
                    f"\tDistance from impala: {distance_from_impala}\n"
                )
                for do_or_not in data[initial_distances][distance_from_impala].keys():
                    for impala_moves in data[initial_distances][distance_from_impala][
                        do_or_not
                    ].keys():
                        lion_moves = data[initial_distances][distance_from_impala][
                            do_or_not
                        ][impala_moves]
                        if do_or_not == "false":
                            knowledge_file.write(
                                f"\t\tIf impala {impala_moves}. Don't do {lion_moves}\n"
                            )
                        else:
                            knowledge_file.write(
                                f"\t\tIf impala {impala_moves}. Do {lion_moves}\n"
                            )


class Knowledge:
    def __init__(self, position=0):
        """
        This class store all the methods that will be used to learn, load knowledge, delete knowledge, search and parse
        the initial position is the position of the lion.
        Knowledge path is relative to the final folder.
        """
        self.position = str(position)
        self.data = dict()
        self.knowledge_path = "./raw_knowledge.txt"

    def search_knowledge(self, impala_move, distance_between):
        """
        Looks for failures under the knowledge data structure. If the lion knows that he should not do someting it will
        just use move that can be done.
        :return: valid moves.
        """
        distance_between = str(distance_between)
        lion_moves, do_not_use = ["move", "hide", "attack"], []
        if self.data.get(self.position):
            inner_data = self.data[self.position]
            if inner_data.get(distance_between):
                inner_data = inner_data[distance_between]
                if inner_data.get("false"):
                    inner_data = inner_data["false"]
                    if inner_data.get(impala_move):
                        do_not_use = inner_data[impala_move]
        return list(set(lion_moves) - set(do_not_use))

    def update_knowledge(
        self, impala_move, lion_move, distance_between, incursion_status
    ):
        """
        During the hunting incursions the lion starts learning. This method stores all that knowledge.
        :return: raw_knowledge.txt file
        """
        distance_between = str(distance_between)
        incursion_status = str(incursion_status).lower()
        if self.data.get(self.position):
            inner_object = self.data[self.position]
            if inner_object.get(distance_between):
                inner_object = inner_object[distance_between]
                if inner_object.get(incursion_status):
                    inner_object = inner_object[incursion_status]
                    if inner_object.get(impala_move):
                        inner_object = self.data[self.position][distance_between][
                            incursion_status
                        ]
                        if lion_move not in inner_object[impala_move]:
                            self.data[self.position][distance_between][
                                incursion_status
                            ][impala_move].append(lion_move)
                    else:
                        self.data[self.position][distance_between][
                            incursion_status
                        ].update({impala_move: [lion_move]})

                else:
                    self.data[self.position][distance_between].update(
                        {incursion_status: {impala_move: [lion_move]}}
                    )

            else:
                self.data[self.position].update(
                    {distance_between: {incursion_status: {impala_move: [lion_move]}}}
                )

        else:
            self.data.update(
                {
                    self.position: {
                        distance_between: {incursion_status: {impala_move: [lion_move]}}
                    }
                }
            )

    def load_knowledge(self):
        """
        Loads knowledge from file.
        :return:
        """
        try:
            with open(self.knowledge_path, "r") as json_file:
                if os.stat(self.knowledge_path).st_size != 0:
                    file_data = json_file.read()
                    self.data = json.loads(file_data)
                else:
                    self.data = dict()
        except FileNotFoundError:
            self.data = dict()

    def save_knowledge(self):
        """
        Save knowledge in file.
        :return:
        """
        with open(self.knowledge_path, "w") as json_file:
            information = json.dumps(self.data)
            json_file.write(information)

    def flush_knowledge(self):
        """
        Deletes knowledge file.
        :return:
        """
        if os.path.exists(self.knowledge_path):
            os.remove(self.knowledge_path)

    def parse_knowledge(self):
        """
        To understand all the knowledge that the lion has this method creates a file that will be easy for a human to
        read.
        :return:
        """
        translate_knowledge(self.data)


def need_to_escape(distance_between):
    """
    Handles logic to see if the impala needs to run from the lion.
    :param distance_between:
    :return: bool
    """
    escape = False
    if distance_between:
        escape = distance_between < 3
    return escape


class Impala:
    def __init__(self):
        """
        init impala with the position.
        """
        self.impala_moves = ["look_right", "look_left", "look_up", "drink_water"]

    def move(self, distance_from_lion):
        """
        Random choice of movements. Checks if the lion is to close.
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
        Init lion.
        """
        self.position = position
        self.distance_to_impala = set_initial_distance(position)

    def move(self, lion_moves):
        """
        The Knowledge class returns a list of valid movements. Choose a random movement and if the lion moves this
        changes the distance between the lion and the impala.

        Update board.
        :return:
        """
        lion_move = random.choice(
            lion_moves
        )  # this is temporal until we can load the knowledge.

        if lion_move == "move" and self.distance_to_impala > 0:
            self.distance_to_impala = self.distance_to_impala - 1

        return lion_move


def lion_was_seen(impala_move, lion_move, initial_position):
    """
    Using the positions on the field. If the lion is not hided and is on an specific position the impala will see
    the lion and run.
    :param impala_move: str with impala move
    :param lion_move: str with lion move
    :param initial_position: Initial position of the lion.
    :return:
    """
    seen = False
    if (
        impala_move == "look_right"
        and lion_move != "hide"
        and initial_position in (2, 3, 4)
    ):
        seen = True

    elif (
        impala_move == "look_up"
        and lion_move != "hide"
        and initial_position in (1, 2, 8)
    ):
        seen = True

    elif (
        impala_move == "look_left"
        and lion_move != "hide"
        and initial_position in (6, 7, 8)
    ):
        seen = True

    return seen


def escape_success(distance_between):
    """
    If the lions is closer than 3 spaces or if he is at more than 3 spaces from the impala the attack will fail.
    This function handle the logic for that.
    :param distance_between:
    :return:
    """
    if distance_between == 3:
        incursion_status = True
    else:
        incursion_status = False

    return incursion_status


def simulate_hunt(
    initial_positions, manual_hunting=False, number_of_training_incursions=0
):
    """
    Check if is an automatic hunt or a step by step hunt.
    start lion, impala and board.
    load knowledge.
    while True: -> for the time the user asked or each fail or success ask to continue or no.
        move impala
        check if impala runs:
            run and return success or fail
            store result
            break.
        move lion:
            look for lion knowledge
            use knowledge to move lion

            if attack:
                check for success or failure.
                store result

            if move:
                check if impala sees the lion.
                store result

        check if lion was seen:
            store result


    """

    incursions = 0
    while True:
        incursions += 1

        initial_position = random.choice(initial_positions)
        knowledge = Knowledge(initial_position)
        knowledge.load_knowledge()
        hunt_status, finish = True, False

        impala = Impala()
        lion = Lion(initial_position)

        while True:
            lion_move, impala_move = None, None
            distance_between = lion.distance_to_impala
            if not finish:
                impala_move = impala.move(distance_between)
                if impala_move == "escape":
                    finish = True
                    hunt_status = escape_success(distance_between)
                    knowledge.update_knowledge(
                        impala_move, lion_move, distance_between, hunt_status
                    )

            if not finish:
                lion_moves = knowledge.search_knowledge(impala_move, distance_between)
                lion_move = lion.move(lion_moves)
                if lion_move == "attack":
                    finish = True
                    hunt_status = escape_success(distance_between)
                    knowledge.update_knowledge(
                        impala_move, lion_move, distance_between, hunt_status
                    )

                if lion_move == "move":
                    if distance_between > 0:
                        impala_alter_move = impala.move(distance_between - 1)
                        if impala_alter_move == "escape":
                            finish = True
                            hunt_status = escape_success(distance_between - 1)
                            knowledge.update_knowledge(
                                impala_move, lion_move, distance_between, hunt_status
                            )

            was_seen = lion_was_seen(impala_move, lion_move, initial_position)
            if was_seen and not finish:
                finish = True
                hunt_status = escape_success(distance_between)
                knowledge.update_knowledge(
                    impala_move, lion_move, distance_between, hunt_status
                )

            if finish:
                incursion_status = "Finished"
            else:
                incursion_status = "Continue"

            print(
                f"Impala action: {impala_move}. Lion action: {lion_move}. Incursion status: {incursion_status}"
            )

            if finish:
                knowledge.save_knowledge()
                if hunt_status:
                    print("The lion hunted the impala...")
                else:
                    print("The lion failed...")
                break

        if manual_hunting:
            user_input = input("Keep learning? 1 = yes, 2 = no: ")
            if user_input.isdigit() and int(user_input) == 2:
                break

        elif incursions == number_of_training_incursions and not manual_hunting:
            break


def handle_user_selection(user_selection):
    """
    Get data needed for options 1 and 2.
    :param user_selection:
    :return:
    """
    data = []

    if user_selection == 1:
        initial_position = input("Initial position: ")
        if initial_position.isdigit() and int(initial_position) in (
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
        ):
            data = [int(initial_position)]
        else:
            print("Please choose a correct option...")

    elif user_selection == 2:
        initial_positions = []
        while True:
            initial_position = input("Initial position: ")
            if (
                initial_position.isdigit()
                and int(initial_position) in (1, 2, 3, 4, 5, 6, 7, 8)
                and initial_position not in initial_positions
            ):
                initial_positions.append(int(initial_position))
            else:
                print("Not valid position... Try again")

            more_positions = input("Add more positions to train? 1 = yes, 2 = no: ")
            if more_positions.isdigit() and int(more_positions) == 2:
                data = [initial_positions]
                break
        while True:
            number_of_incursions = input(
                "How many times should the lion train? (ej: 10): "
            )
            if number_of_incursions.isdigit():
                number_of_incursions = int(number_of_incursions)
                data.append(number_of_incursions)
                break
            else:
                print("Please provide a valid number...")

    return data


def interactive_menu():
    """
    Allows some decisions:
    1. Step by step hunt
    2. Train. (take input from user)
    3. Download knowledge.
    4. Flush knowledge
    5. Stop (save knowledge)
    :return: int with option.
    """
    while True:
        print("\t Teaching a Lion to hunt...")
        print(
            "------------------------------------------------------------------------------------------"
        )
        print("Choose a number: ")
        print("1. Step by step hunt")
        print("2. Train")
        print("3. Get knowledge")
        print("4. Flush knowledge")
        print("5. Exit")

        user_input = input("Option: ")
        if user_input.isdigit() and int(user_input) in (1, 2, 3, 4, 5):
            user_input = int(user_input)
            break
        else:
            print("Please choose a correct option...")

    return user_input


def main():
    """
    Core handler of the program. Handles the selection of the user.
    :return:
    """
    while True:
        user_selection = interactive_menu()
        if user_selection == 1:
            initial_position = handle_user_selection(user_selection)
            simulate_hunt(initial_position, True)

        elif user_selection == 2:
            initial_positions, total_of_trainings = handle_user_selection(
                user_selection
            )
            if initial_positions:
                simulate_hunt(
                    initial_positions, number_of_training_incursions=total_of_trainings
                )
            else:
                print("Missing initial positions...")

        elif user_selection == 3:
            knowledge = Knowledge()
            knowledge.load_knowledge()
            knowledge.parse_knowledge()

        elif user_selection == 4:
            knowledge = Knowledge()
            knowledge.flush_knowledge()

        elif user_selection == 5:
            break


if __name__ == "__main__":
    main()
