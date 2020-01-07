import csv
import networkx as nx

g = nx.DiGraph()

# 4. Data Science/Engineering Tracks
# 4b. Pipeline Dependency

with open('task_ids.txt', 'r') as f:
    reader = csv.reader(f)
    task_ids = list(reader)[0]
    g.add_nodes_from(task_ids)

with open('relations.txt', 'r') as f:
    line = f.readline()
    while line:
        content = line.split('->')
        task1 = content[0].strip()
        task2 = content[1].strip()
        g.add_edge(task1, task2)
        line = f.readline()

# check to see if its a DAG
is_dag = nx.is_directed_acyclic_graph(g)
print (is_dag)

ts = list(nx.topological_sort(g))


def generate_task_order(ts, task_starting, task_goal):
    if isinstance(task_starting, list):
        idxs = [ts.index(task) for task in task_starting]
        idx = max(idxs)
    else:
        idx = ts.index(task_starting)
    return ts[idx:ts.index(task_goal) + 1]


print (generate_task_order(ts, '73', '36'))
print (generate_task_order(ts, ['73', '56'], '36'))

