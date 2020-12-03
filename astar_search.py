import copy
from collections import deque
import random
import time
import heapq


class State(object):
    def __init__(self, randm, blank_location):
        self.matrix = randm
        self.blank = blank_location

    def __str__(self):
        return "%s %s %s\n%s %s %s\n%s %s %s" %(self.matrix[1][1], self.matrix[1][2],self.matrix[1][3],self.matrix[2][1],self.matrix[2][2],self.matrix[2][3],self.matrix[3][1],self.matrix[3][2],self.matrix[3][3])
    
    def is_goal(self):
        return self.matrix == [[-1,-1,-1,-1,-1], [-1,0,1,2,-1], [-1,3,4,5,-1], [-1,6,7,8,-1], [-1,-1,-1,-1,-1]]

    def different(self):
        goal = [0,1,2,3,4,5,6,7,8]
        compare = []
        for i in range(1,4):
            for j in range(1,4):
                compare.append(self.matrix[i][j])
        difference = set(goal).symmetric_difference(set(compare))
        return len(difference)

    def manhattan_dist(self):
        goal = [[-1,-1,-1,-1,-1], [-1,0,1,2,-1], [-1,3,4,5,-1], [-1,6,7,8,-1], [-1,-1,-1,-1,-1]]
        goal_dic = {} # add goal position
        ans = 0
        for i in range(1,4):
            for j in range(1,4):
                goal_dic[goal[i][j]] = [i,j]
        for i in range(1,4):
            for j in range(1,4):
                comp = self.matrix[i][j]
                goali, goalj = goal_dic[comp]
                ans += abs(goali-i) + abs(goalj-j)
        return ans

    def possible_move(self):
        i = int(self.blank[0])
        j = int(self.blank[1])
        next_matrix = copy.deepcopy(self.matrix)

        if int(self.matrix[i-1][j]) > 0:
            next_matrix[i-1][j] = self.matrix[i][j]
            next_matrix[i][j] = self.matrix[i-1][j] 
            new_state = State(next_matrix, [i-1, j])
            yield new_state
            
        if int(self.matrix[i+1][j]) > 0:
            next_matrix = copy.deepcopy(self.matrix)
            next_matrix[i+1][j] = self.matrix[i][j]
            next_matrix[i][j] = self.matrix[i+1][j]
            new_state = State(next_matrix, [i+1, j])
            yield new_state
            
        if int(self.matrix[i][j-1]) > 0:
            next_matrix = copy.deepcopy(self.matrix)
            next_matrix[i][j-1] = self.matrix[i][j]
            next_matrix[i][j] = self.matrix[i][j-1]
            new_state = State(next_matrix, [i, j-1])
            yield new_state
            
        if int(self.matrix[i][j+1]) > 0:
            next_matrix = copy.deepcopy(self.matrix)
            next_matrix[i][j+1] = self.matrix[i][j]
            next_matrix[i][j] = self.matrix[i][j+1]
            new_state = State(next_matrix, [i, j+1])
            yield new_state
        

class Node(object):
    def __init__(self, parent, state, cost):
        self.parent = parent
        self.state = state
        self.cost = cost
    
    def __str__(self):
        return self.state.__str__()
    
    def childrens(self):    
        for state in self.state.possible_move():
            if self.parent != None and self.parent.state == state:
                continue
            state_hn = state.different() + state.manhattan_dist()
            state_gn = self.cost + 1
            yield Node(parent=self, state=state, cost=state_gn + state_hn)
    
    def backchaining(self):
        sol = []
        node = self
        sol.append(node)
        while node.parent is not None:
            sol.append(node.parent)
            node = node.parent
        sol.reverse()
        return sol


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0
    
    def add(self, cost, node):
        heapq.heappush(self.elements, (cost,node))
    
    def pop(self):
        return heapq.heappop(self.elements)[1]


def is_solvable(matrix):
    inversed = 0
    for k in range(8):
        for l in range(k+1,9):
            if matrix[k] > matrix[l] and matrix[k] != 0 and matrix[l] != 0:
                inversed += 1
    return inversed % 2 == 0  # return true if inverse count is even


def make_randm():
    default = [0,1,2,3,4,5,6,7,8]
    while True:
        random.shuffle(default)
        if is_solvable(default):
            break
    randm_matrix = [[-1,-1,-1,-1,-1], [-1,0,1,2,-1], [-1,3,4,5,-1], [-1,6,7,8,-1], [-1,-1,-1,-1,-1]]
    k = 0
    for i in range(1,4):
        for j in range(1,4):
            randm_matrix[i][j] = default[k]
            if default[k] == 0:
                blank_i = i
                blank_j = j
            k += 1
    return randm_matrix, [blank_i, blank_j]

def astar_search(root):
    frontier = PriorityQueue()
    nodedic = {}

    i = 0
    frontier.add(0,i)
    nodedic[i] = root

    while not frontier.empty():
        curr_node = nodedic[frontier.pop()]
        if curr_node.state.is_goal():
            print("Total cost: ",curr_node.cost)
            return curr_node.backchaining()
        for node in curr_node.childrens():
            i += 1
            frontier.add(node.cost,i)
            nodedic[i] = node  

def main():
    m, a = make_randm()
    start_state = State(m,a)
    root = Node(None, start_state, 0)
    t0 = time.time()
    for state in astar_search(root):
        print(state)
        print("\n")
    t1 = time.time()
    print("Execution time: %s"%(t1-t0))

if __name__ == '__main__':
    main() 