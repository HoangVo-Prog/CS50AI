import sys

from crossword import *


class CrosswordCreator:

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.crossword.variables:
            for word in self.crossword.words:
                if len(word) != variable.length:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        revised = False
        x_delete = []

        for x_word in self.domains[x]:
            count = 0
            for y_word in self.domains[y]:
                if (overlap := self.crossword.overlaps[(x, y)]) is not None:

                    if x_word != y_word and x_word[overlap[0]] == y_word[overlap[1]]:
                        count += 1
                else:
                    if x_word != y_word:
                        count += 1

            if count == 0:
                revised = True
                x_delete.append(x_word)

        for x_word in x_delete:
            self.domains[x].remove(x_word)
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = [(x, y) for x in self.domains.keys() for y in self.domains.keys() if x != y]
        while arcs != list():
            x, y = arcs.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(x):
                    arcs.append((neighbor, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        if assignment == dict():
            return False
        for key in self.crossword.variables:
            if key not in assignment.keys():
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # distinct, length
        if assignment == dict():
            return False
        for key, value in assignment.items():
            if key.length != len(value) or value is None or value == "":
                return False

        # no conflict neighbor
        for key, value in self.crossword.overlaps.items():
            if value:
                x, y = key
                if x in assignment.keys() and y in assignment.keys():
                    if (string_x := assignment[x]) and (string_y := assignment[y]):
                        if string_x[value[0]] != string_y[value[1]]:
                            return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        if assignment == dict():
            possible_value = self.domains[var]
            tracking_dict = dict()
            for value in possible_value:
                count = 0
                for variable, overlap in self.crossword.overlaps.items():
                    if var in variable:
                        if value in self.domains[variable[1]]:
                            count += 1
                tracking_dict[value] = count
            sorted_dict = dict(sorted(tracking_dict.items(), key=lambda item: item[1]))
            return list(sorted_dict.keys())

        else:
            tracking_dict = dict()
            another_vars = [variable for variable in assignment.keys()
                            if variable != var
                            and assignment[variable] is None]
            for value in self.domains[var]:
                count = 0
                for variable in another_vars:
                    if value in self.domains[variable]:
                        self.domains[variable].remove(value)
                    if variable in self.crossword.neighbors(var):
                        for variable_value in self.domains[variable]:
                            overlap = self.crossword.overlaps(var, variable)
                            if value[overlap[0]] != variable_value[overlap[1]]:
                                self.domains[variable].remove(variable_value)
                    if len(self.domains[variable]) == 1:
                        count += 1
                tracking_dict[value] = count
            sorted_dict = dict(sorted(tracking_dict.items(), key=lambda item: item[1]))
            return list(sorted_dict.keys())

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        if assignment == dict():
            tracking_dict_by_length = {
                key: len(value) for key, value in self.domains.items()
                if key in self.crossword.variables
            }
            sorted_by_value = dict(sorted(tracking_dict_by_length.items(), key=lambda item: item[1]))
            return list(sorted_by_value.keys())[0]

        else:
            tracking_dict_by_length = {
                variable: len(value)
                for variable, value in self.domains.items()
                if variable in self.crossword.variables
                and variable not in assignment
            }
            sorted_by_value = dict(sorted(tracking_dict_by_length.items(), key=lambda item: item[1]))
            checking_max = [key for key, value in sorted_by_value.items() if max(sorted_by_value.values()) == value]
            if len(checking_max) == 1:
                return checking_max[0]

            tracking_list_by_overlap = checking_max
            tracking_dict_by_overlap = {}
            for variable in tracking_list_by_overlap:
                count = 0
                for value, key in self.crossword.overlaps.items():
                    if variable in value and key is not None:
                        count += 1
                tracking_dict_by_overlap[variable] = count
            sorted_by_overlap = dict(sorted(tracking_dict_by_overlap.items(),
                                            key=lambda item: item[1]), reversed=True)
            return list(sorted_by_overlap.keys())[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            self.domains[var].remove(value)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
