import pickle

with open("q_table_08_1_2_2_100_8.policy", "rb") as f:
    q_table = pickle.load(f)

out = open("rl_policy.js", "w")

out.write("function getPolicy() {\n")
out.write("\tlet policy = new Map();\n")

for k, v in q_table.items():
    out.write(f"\tpolicy.set(JSON.stringify(['{k[0]}', {k[1]}]), {v});\n")

out.write("return policy;\n")
out.write("};")
out.close()