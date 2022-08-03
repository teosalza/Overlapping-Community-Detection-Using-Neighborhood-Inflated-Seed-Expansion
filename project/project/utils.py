#loading data for Graph generation
def load_data(filename):
    input_lines = []
    raw_lines = open(filename, 'r').read().splitlines()
    num_nodes = 0
    nodes = {}
    for line in raw_lines:
        line_content = line.split()
        from_id = int(line_content[0])
        to_id = int(line_content[1])
        if from_id not in nodes:
            nodes[from_id] = num_nodes
            num_nodes += 1
        if to_id not in nodes:
            nodes[to_id] = num_nodes
            num_nodes += 1
        input_lines.append([nodes[from_id], nodes[to_id]])
    return input_lines, num_nodes