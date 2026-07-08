import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells: 
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge: list[Sentence] = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        def infer():
            # Shallow copy knowledge base so it can be modified while iterating
            kb = self.knowledge.copy()
            new_safes = set()
            new_mines = set()

            # Get known mines and safes from sentences
            for sentence in kb:
                new_safes.update(sentence.known_safes())
                new_mines.update(sentence.known_mines())    

            # If no new mines or safes, end with inferring
            if len(new_safes) == 0 and len(new_mines) == 0:
                return (new_safes, new_mines)

            for sentence in kb:
                # Update sentences with new known mines and safes
                for ns in new_safes:
                    sentence.mark_safe(ns)
                for nm in new_mines:
                    sentence.mark_mine(nm)

                for sentence_two in kb:
                    if sentence == sentence_two:
                        continue
                    # If sentence_two is subset of sentence
                    if sentence.cells.intersection(sentence_two.cells):
                        new_cells = sentence.cells - sentence_two.cells
                        new_count = sentence.count - sentence_two.count
                        new_sentence = Sentence(new_cells, new_count)
                        if new_sentence not in self.knowledge:
                            self.knowledge.append(new_sentence)
                
            s, m = infer()
            s.update(new_safes)
            m.update(new_mines)
            return (s, m)

        # Add cell to played and safe
        self.moves_made.add(cell)
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

        # Get neighboring cells
        row, col = cell
        neighbor_cells = set()
        for i in range(row-1, row+2):
            if i < 0 or i >= self.height:
                continue
            for j in range(col-1, col+2):
                if j < 0 or j >= self.width:
                    continue
                neighbor_cell = (i, j)
                if neighbor_cell == cell:
                    continue
                neighbor_cells.add(neighbor_cell)

        # Remove safes
        neighbor_cells -= self.safes

        # Remove mines and lower the count
        known_mines_in_neighbors = neighbor_cells.intersection(self.mines)
        neighbor_cells -= known_mines_in_neighbors
        new_count = count - len(known_mines_in_neighbors)

        # Add new sentence if not already present
        new_sentence = Sentence(neighbor_cells, new_count)
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)

        # Infer KB for new sentences, known mines and safes
        new_safes, new_mines = infer()
        self.safes.update(new_safes)
        self.mines.update(new_mines)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes - self.moves_made
        if safe_moves:
            return safe_moves.pop()
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:
            if len(self.moves_made) + len(self.mines) >= self.height * self.width:
                return None
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            cell = (i, j)
            if cell not in self.moves_made and cell not in self.mines:
                return cell
