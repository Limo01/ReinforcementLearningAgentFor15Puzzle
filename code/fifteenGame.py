import random

class FifteenGame:
    def __init__(self):
        self.empty_cell = 99
        self.empty_cell_index = 15
        
        self.board = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, self.empty_cell]
        self.rows_solved = 4
        self.generate_random_board()
    
    def generate_random_board(self):
        for _ in range(1000):
            row_empty_cell = self.empty_cell_index // 4
            col_empty_cell = self.empty_cell_index - row_empty_cell * 4

            possible_actions = []

            if row_empty_cell - 1 >= 0:
                possible_actions.append((row_empty_cell - 1) * 4 + col_empty_cell)
            
            if row_empty_cell + 1 < 4:
                possible_actions.append((row_empty_cell + 1) * 4 + col_empty_cell)
            
            if col_empty_cell - 1 >= 0:
                possible_actions.append(row_empty_cell * 4 + col_empty_cell - 1)

            if col_empty_cell + 1 < 4:
                possible_actions.append(row_empty_cell * 4 + col_empty_cell + 1)

            action = random.choice(possible_actions)
            
            self.board[self.empty_cell_index] = self.board[action]
            self.board[action] = self.empty_cell
            self.empty_cell_index = action
        self.rows_solved = self.getRowsSolved()

    
    def print_board(self):
        print("---------------------")

        for i in range(4):
            print("| ", end="")

            for j in range(4):          
                if self.board[i * 4 + j] < 10:
                    print(f" {self.board[i * 4 + j]} | ", end="")
                else:
                    print(f"{self.board[i * 4 + j]} | ", end="")
            print("")

        print("---------------------")
    
    def getPossibleActions(self):
        if self.rows_solved == 4:
            return []

        row_empty_cell = self.empty_cell_index // 4
        col_empty_cell = self.empty_cell_index - row_empty_cell * 4

        possible_actions = []

        if (self.rows_solved <= 2 and row_empty_cell - 1 >= self.rows_solved) or (self.rows_solved == 3 and row_empty_cell - 1 >= 2):
            possible_actions.append((row_empty_cell - 1) * 4 + col_empty_cell)
        
        if row_empty_cell + 1 < 4:
            possible_actions.append((row_empty_cell + 1) * 4 + col_empty_cell)
        
        if col_empty_cell - 1 >= 0:
            possible_actions.append(row_empty_cell * 4 + col_empty_cell - 1)

        if col_empty_cell + 1 < 4:
            possible_actions.append(row_empty_cell * 4 + col_empty_cell + 1)

        return possible_actions
    
    def doAction(self, action):
        if action not in self.getPossibleActions():
            raise Exception(f"Move {action} not allowed!")
        
        self.board[self.empty_cell_index] = self.board[action]
        self.board[action] = self.empty_cell

        self.empty_cell_index = action

        self.rows_solved = self.getRowsSolved()

        return self.__getReward()
    
    def getHash(self):
        hash = ""
        bound = len(self.board)

        if self.rows_solved < 2:
            bound = (self.rows_solved + 1) * 4

        for i in self.board:
            if i <= bound or i == self.empty_cell:
                hash += str(i) + "_"
            else:
                hash += str(0) + "_"
        
        return hash

    def __getReward(self):
        if self.rows_solved == 3:
            return 2
        elif self.rows_solved == 4:
            return 100
        
        return self.rows_solved

    def getRowsSolved(self):
        count = 0

        for i in range(len(self.board) - 1):
            if self.board[i] != i + 1:
                break
            count += 1
        
        if count == len(self.board) - 1:
            count += 1
        
        return count // 4
    
    def isGameFinished(self):
        return self.board == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, self.empty_cell]