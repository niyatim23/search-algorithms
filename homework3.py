# ('../resource/asnlib/public/input1.txt')

from collections import deque
import heapq

def read_input(path):
    input_data = open(path, 'r')
    algorithm = input_data.readline()
    grid_size = list(map(int, input_data.readline().split()))
    landing_site = list(map(int, input_data.readline().split()))
    max_elevation = int(input_data.readline().split()[0])
    number_of_target_sites = int(input_data.readline()[0])
    target_sites = []
    for i in range(0, number_of_target_sites):
        target_sites.append(list(map(int, input_data.readline().split())))
    grid = []
    for i in range(0, int(grid_size[1])):
        grid.append(list(map(int, input_data.readline().split())))
    return [algorithm.strip(), grid_size, landing_site, max_elevation, number_of_target_sites, target_sites, grid]


def bfs(grid_size, landing_site, max_elevation, t, grid):
    if (landing_site == t):
        return landing_site
    landing_site = tuple(landing_site[::-1])  #ls is now x, y and is a tuple
    print(landing_site)
    t = tuple(t[::-1])                       #t is x, y and is a tuple
    frontier = deque([landing_site])   #inserted into frontier as x, y and as a tuple
    parent_dict = {}
    for i in range(0, grid_size[1]):
        for j in range(0, grid_size[0]):
            parent_dict[tuple([i,j])] = 'X'   #parent_dict is storing values as x, y
    explored = set()
    travel_path = []
    while frontier:
        parent = frontier.popleft()
        explored.add(parent)
        children = []  #list of tuples in x,y
        x_rows = [x + parent[0] for x in [-1, -1, -1, 0, 0, 1, 1, 1]]
        y_columns = [y + parent[1] for y in [-1, 0, 1, -1, 1, -1, 0, 1]]
        for i in range(0, 8):
            if 0 <= x_rows[i] < grid_size[1] and 0 <= y_columns[i] < grid_size[0]:
                if abs(grid[x_rows[i]][y_columns[i]] - grid[parent[0]][parent[1]]) <= max_elevation:
                    children.append(tuple([x_rows[i], y_columns[i]]))
        for child in children:
            if child not in list(explored) and child not in list(frontier):
                parent_dict[child] = parent
                if child == t:
                    x = t
                    while(x != landing_site):
                        travel_path.append(x[::-1])
                        x = parent_dict.get(x)
                    travel_path.append(landing_site)
                    return travel_path[::-1]
                frontier.append(child)
    return "FAIL"


def ucs(grid_size, landing_site, max_elevation, t, grid):
    landing_site = tuple(landing_site[::-1])
    t = tuple(t[::-1])
    frontier = []
    heapq.heappush(frontier, (0, landing_site))
    explored = set()
    parent_dict = {}
    for i in range(0, grid_size[1]):
        for j in range(0, grid_size[0]):
            parent_dict[tuple([i, j])] = 'X'
    travel_path = []
    while frontier:
        parent = heapq.heappop(frontier)
        if(parent[1] == t):
            x = t
            while(x != landing_site):
                travel_path.append(x[::-1])
                x = parent_dict.get(x)
            travel_path.append(landing_site)
            return travel_path[::-1]
        explored.add(parent[1])
        children = []
        x_rows = [x + parent[1][0] for x in [-1, -1, -1, 0, 0, 1, 1, 1]]
        y_columns = [y + parent[1][1] for y in [-1, 0, 1, -1, 1, -1, 0, 1]]
        for i in range(0, 8):
            if 0 <= x_rows[i] < grid_size[1] and 0 <= y_columns[i] < grid_size[0]:
                if abs(grid[x_rows[i]][y_columns[i]] - grid[parent[1][0]][parent[1][1]]) <= max_elevation:
                    if x_rows[i] == parent[1][0] or y_columns[i] == parent[1][1]:
                        children.append(tuple([10 + parent[0], tuple([x_rows[i], y_columns[i]])]))
                    else:
                        children.append(tuple([14 + parent[0], tuple([x_rows[i], y_columns[i]])]))
        for child in children:
            if child[1] not in explored and child[1] not in [x[1] for x in frontier]:
                heapq.heappush(frontier, (child[0], child[1]))
                parent_dict[child[1]] = parent[1]
            else:
                for f in frontier:
                    if f[1] == child[1]:
                        if child[0] < f[0]:
                            frontier.remove(f)
                            frontier.append(tuple([child[0], child[1]]))
                            heapq.heapify(frontier)
                            break
    return "FAIL"




 # node[fn = gn + hn, gn, [x, y]]
def astar(grid_size, landing_site, max_elevation, t, grid):
    landing_site = tuple(landing_site[::-1])  
    t = tuple(t[::-1])                       
    frontier = []                            
    heapq.heappush(frontier, (0, 0, landing_site))
    explored = set()
    parent_dict = {}
    for i in range(0, grid_size[1]):
        for j in range(0, grid_size[0]):
            parent_dict[tuple([i, j])] = 'X'   
    travel_path = []
    while frontier:
        parent = heapq.heappop(frontier)
        if(parent[2] == t):
            x = t
            while(x != landing_site):
                travel_path.append(x[::-1])
                x = parent_dict.get(x)
            travel_path.append(landing_site[::-1])
            return travel_path[::-1]
        explored.add(parent[2])
        children = []  
        x_rows = [x + parent[2][0] for x in [-1, -1, -1, 0, 0, 1, 1, 1]]
        y_columns = [y + parent[2][1] for y in [-1, 0, 1, -1, 1, -1, 0, 1]]
        for i in range(0, 8):
            if 0 <= x_rows[i] < grid_size[1] and 0 <= y_columns[i] < grid_size[0]:
                if abs(grid[x_rows[i]][y_columns[i]] - grid[parent[2][0]][parent[2][1]]) <= max_elevation:
                    hn = round(math.sqrt(((x_rows[i] - t[0])*(x_rows[i] - t[0]) + (y_columns[i] - t[1])*(y_columns[i] - t[1]) + (grid[x_rows[i]][y_columns[i]] - grid[t[0]][t[1]])*(grid[x_rows[i]][y_columns[i]] - grid[t[0]][t[1]]))))
                    if x_rows[i] == parent[2][0] or y_columns[i] == parent[2][1]:
                        children.append(tuple([10 + parent[1] + abs(grid[x_rows[i]][y_columns[i]] - grid[parent[2][0]][parent[2][1]]) + hn, 10 + parent[1] + abs(grid[x_rows[i]][y_columns[i]] - grid[parent[2][0]][parent[2][1]]), tuple([x_rows[i], y_columns[i]])]))
                    else:
                        children.append(tuple([14 + parent[1] + abs(grid[x_rows[i]][y_columns[i]] - grid[parent[2][0]][parent[2][1]]) + hn, 14 + parent[1] + abs(grid[x_rows[i]][y_columns[i]] - grid[parent[2][0]][parent[2][1]]), tuple([x_rows[i], y_columns[i]])]))
        for child in children:
            if child[2] not in explored and child[2] not in [x[2] for x in frontier]:
                heapq.heappush(frontier, (child[0], child[1], child[2]))
                parent_dict[child[2]] = parent[2]
            else:
                if child[2] in [x[2] for x in frontier]:
                    for f in frontier:
                        if f[2] == child[2]:
                            if child[1] < f[1]:  
                                frontier.remove(f)
                                frontier.append(tuple([child[0], child[1], child[2]]))  
                                heapq.heapify(frontier)
                                break
    return "FAIL"



def rbfs(grid_size, node, max_elevation, goal, grid, parent_dict, f_limit):
    if(node[3] == goal):
        return node, 0
    successors = []
    x_rows = [x + node[3][0] for x in [-1, -1, -1, 0, 0, 1, 1, 1]]
    y_columns = [y + node[3][1] for y in [-1, 0, 1, -1, 1, -1, 0, 1]]
    for i in range(0, 8):
        if 0 <= x_rows[i] < grid_size[1] and 0 <= y_columns[i] < grid_size[0]:
            if abs(grid[x_rows[i]][y_columns[i]] - grid[node[3][0]][node[3][1]]) <= max_elevation:
                hn = round(math.sqrt(((x_rows[i] - goal[0])*(x_rows[i] - goal[0]) + (y_columns[i] - goal[1])*(y_columns[i] - goal[1]) + (grid[x_rows[i]][y_columns[i]] - grid[goal[0]][goal[1]])*(grid[x_rows[i]][y_columns[i]] - grid[goal[0]][goal[1]]))))
                if x_rows[i] == node[3][0] or y_columns[i] == node[3][1]:
                    gn = round(10 + abs(grid[x_rows[i]][y_columns[i]] - grid[node[3][0]][node[3][1]]) + node[1])
                else:
                    gn = round(14 + abs(grid[x_rows[i]][y_columns[i]] - grid[node[3][0]][node[3][1]]) + node[1])
                successors.append((list([gn + hn, gn, hn, list([x_rows[i], y_columns[i]])]))) 
    #print("Parent:", node, " Successors:", successors)
    if not successors:
        return None, math.inf
    for s in successors: 
        s[0] = max(s[1] + s[2], node[0])
    while True:
        successors.sort(key = lambda x : x[0])
        best = successors[0]
        if best[0] > f_limit:
            return None, best[0]
        if len(successors) > 1:
            alternative = successors[1][0]
        else:
            alternative = math.inf
        result, best[0] = a_star(grid_size, best, max_elevation, goal, grid, parent_dict, min(f_limit, alternative))
        if result is not None:
            parent_dict[tuple(best[3])] = tuple(node[3]) 
            return result, best[0]


if __name__ == "__main__":
    algorithm, grid_size, landing_site, max_elevation, number_of_target_sites, target_sites, grid = read_input('../Test Cases/testip.txt')
    if algorithm == "BFS":
        for t in target_sites:
            print(bfs(grid_size, landing_site, max_elevation, t, grid))
            print("END")
    elif algorithm == "UCS":
        for t in target_sites:
            print(ucs(grid_size, landing_site, max_elevation, t, grid))
            print("END")
    else:
        for t in target_sites:
            print(astar(grid_size, landing_site, max_elevation, t, grid))
        '''landing_site = list([0, 0, 0, list(landing_site[::-1])])
        for t in target_sites:
            parent_dict = {}
            for i in range(0, grid_size[1]):
                for j in range(0, grid_size[0]):
                    parent_dict[tuple([i, j])] = 'X'
            t = t[::-1]
            p, q = a_star(grid_size, landing_site, max_elevation, t, grid, parent_dict, math.inf)
            if(p is not None):
                x = tuple(t)
                travel_path = []
                while(x != tuple(landing_site[3])):
                    travel_path.append(x[::-1])
                    x = parent_dict.get(x)
                travel_path.append(tuple(landing_site[3]))
                print(travel_path[::-1])
            else:
                print("FAIL")
            print("END")'''
