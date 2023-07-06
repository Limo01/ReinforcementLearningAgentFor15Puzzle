import random
import pickle
import time
from fifteenGame import FifteenGame

def solveGame(q_table):
    environment = FifteenGame()
    moves = 0

    while not environment.isGameFinished():
        # environment.print_board()

        current_state = environment.getHash()
        possible_actions = environment.getPossibleActions()
        
        # IDEA: Take all the maximum and do randomly one of the max actions
        best_actions = [-1]

        for a in possible_actions:
            if q_table.get((current_state, a), 0) > q_table.get((current_state, best_actions[0]), 0):
                best_actions = [a]
            elif q_table.get((current_state, a), 0) == q_table.get((current_state, best_actions[0]), 0):
                best_actions.append(a)
            # print(q_table.get((current_state, a), 0))

        action = random.choice(best_actions)

        environment.doAction(action)
        moves += 1
        # time.sleep(2)

        if moves > 120:
            return None
    
    return moves

    # print("FINAL BOARD")
    # environment.print_board()
    # print(f"Number of moves: {moves}")


with open("q_table_08_1_2_2_100_8.policy", "rb") as f:
    q_table = pickle.load(f)

moves = []

for _ in range(100):
    res = solveGame(q_table)

    if res != None:
        moves.append(res)

print(f"Moves: {moves}")
print(f"Lenght Moves: {len(moves)}")
print(f"Average moves number: {sum(moves) / len(moves)}")