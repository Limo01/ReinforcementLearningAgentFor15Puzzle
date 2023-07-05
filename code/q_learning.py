import random
import pickle
from fifteenGame import FifteenGame

def q_learning(gamma, epochs, q_table = {}, exploitationLevel = 0, tryNewPaths = True):
    environment = FifteenGame()
    solved = 0

    for _ in range(epochs):
        current_state = environment.getHash()
        possible_actions = environment.getPossibleActions()
        action = -1

        if tryNewPaths:
            for a in possible_actions:
                if (current_state, a) not in q_table:
                    action = a

        if action == -1:
            if environment.getRowsSolved() < exploitationLevel: # Exploitation for the first exploitationLevel columns
                for a in possible_actions:
                    if q_table.get((current_state, a), 0) >= q_table.get((current_state, action), 0):
                        action = a
            else: # Otherwise exploration
                action = random.choice(possible_actions)
        
        reward = environment.doAction(action)

        print(f"Current_state_hash: {current_state}, Reward: {reward}")
        
        new_state = environment.getHash()
        new_state_possible_actions = environment.getPossibleActions()
        best_new_state_action_reward = 0
        
        for a in new_state_possible_actions:
            best_new_state_action_reward = max(best_new_state_action_reward, q_table.get((new_state, a), 0))
        
        q_table[(current_state, action)] = reward + gamma * best_new_state_action_reward
        
        if environment.isGameFinished():
            environment.generate_random_board()
            solved += 1
    
    return q_table, solved

def countValuseDifferentFromZero(q_table):
    count = 0

    for i in q_table:
        if q_table[i] != 0:
            count += 1
    
    return count

def printNumberOfStatesPerRowsSolved(q_table):
    first_row_completed = set()
    second_row_completed = set()
    zero_rows_completed = set()

    for p in q_table.keys():
        if p[0][:15] == "1_2_3_4_5_6_7_8":
            second_row_completed.add(p[0])
        elif p[0][:7] == "1_2_3_4":
            first_row_completed.add(p[0])
        else:
            zero_rows_completed.add(p[0])

    print(f"Number of states with no rows completed: {len(zero_rows_completed)}")
    print(f"Number of states with first row completed: {len(first_row_completed)}")
    print(f"Number of states with second row completed: {len(second_row_completed)}")
    

with open('q_table_08_1_2_2_100_7.policy', 'rb') as f:
    q_table = pickle.load(f)

# Train the new policy

q_table, solved = q_learning(0.8, 40_000_000, q_table, exploitationLevel=1)

print(f"Max value on the map: {max(q_table.values())}")
print(f"Total number of states and actions in the map: {len(q_table)}")
print(f"Total number of action values different from zero: {countValuseDifferentFromZero(q_table)}")
print(f"Puzzle solved: {solved}")
printNumberOfStatesPerRowsSolved(q_table)

with open('q_table_08_1_2_2_100_8.policy', 'wb') as f:
    pickle.dump(q_table, f)