from collections import deque
from collections import defaultdict
from itertools import combinations
class Node:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.path = [] 
        if parent:
            self.path = parent.path + [item]

class FPTree:
    def __init__(self):
        self.root = Node(None, 1, None)


    def add_transaction(self, transaction):
        current_node = self.root

        for item in transaction:
            if item not in current_node.children:
                current_node.children[item] = Node(item, 1, current_node)
            else:
                current_node.children[item].count += 1

            current_node = current_node.children[item]


    def print_tree_level_order(self):
        if self.root is None:
            return

        queue = deque([self.root])
        level = 0

        while queue:
            level_size = len(queue)

            for _ in range(level_size):
                node = queue.popleft()

                if node.item is not None:
                    print(f"{node.item} ({node.count})", end=" ")

                for child in node.children.values():
                    queue.append(child)

            level += 1
            print()

    def get_node_paths(self):
        node_paths = {}

        def traverse(node):
            if node.item is not None:
                node_paths[node] = node.path

            for child in node.children.values():
                traverse(child)

        traverse(self.root)
        return node_paths
           
def construct_conditional_pattern_base(node_path):
    
    conditional_pattern_base = defaultdict(list)
    for node, path in node_path.items():
        temp = (path[:-1], node.count)
        conditional_pattern_base[node.item].append(temp)
    
    return conditional_pattern_base

def construct_fp_tree(ordered_frequent_set):
    fp_tree = FPTree()
    for transaction in ordered_frequent_set:
        fp_tree.add_transaction(transaction)
    return fp_tree


def get_ordered_frequent_set(frequent_pattern_set, transaction):
    ordered_frequent_set = []
    for t in transaction:
        temp = []
        for item in frequent_pattern_set:
            if set(item).issubset(set(t)):
                temp.extend(item)
        ordered_frequent_set.append(temp)
        
    return ordered_frequent_set
            

def get_frequent_pattern_set(transaction, items, minsup):
    itemset = {}
    for item in items:
        for t in transaction:
            if set(item).issubset(set(t)):
                itemset.setdefault(tuple(item),0)
                itemset[tuple(item)] += 1;
    
    frequent_pattern_set = {}
    for item, freq in itemset.items():
        if freq >= minsup:
            frequent_pattern_set[item] = freq
    
    frequent_pattern_set = dict(sorted(frequent_pattern_set.items(), key=lambda items: items[1] , reverse=True))
    return frequent_pattern_set

def extract_frequent_itemsets(conditional_pattern_base):
    conditional_frequent_pattern = {}
    for key, cpb in conditional_pattern_base.items():
        temp = set(cpb[0][0])
        freq = cpb[0][1]
        for item in cpb[1:]:
            temp.intersection_update(set(item[0]))
            freq += item[1]
        if(len(temp)==0):
            continue
        
        cfp = (temp,freq)
        conditional_frequent_pattern[key] = cfp
    
    
    itemsets = []
    for key, value in conditional_frequent_pattern.items():
        temp = list(key)
        temp.extend(value[0])
        itemsets.append(temp)
    
    frequent_itemsets = []
    for items in itemsets:
        for i in range(2,len(items)+1):
            frequent_itemsets.extend([combo for combo in combinations(items, i)])
    
    return frequent_itemsets
            

def main():
    transaction = [['E','K','M','N','O','Y'],
                   ['D','E','K','N','O','Y'], 
                   ['A','E','K','M'],  
                   ['C','K','M','U','Y'],
                   ['C','E','I','K','O','O']]
    
    items = sorted(set.union(*map(set,transaction)))
    minsup = 3
    
    print("Frequent Pattern Set: ")
    frequent_pattern_set = get_frequent_pattern_set(transaction, items, minsup)
    for key, value in frequent_pattern_set.items():
        print(f" {key}        {value}")
    
    print("Ordered Frequent Set:")
    ordered_frequent_set = get_ordered_frequent_set(frequent_pattern_set, transaction)
    for key in ordered_frequent_set:
        print(f"{key}")
    
    fp_tree = construct_fp_tree(ordered_frequent_set)
    print("FP-Tree:")
    fp_tree.print_tree_level_order()
    
    node_paths = fp_tree.get_node_paths()

    conditional_pattern_base = construct_conditional_pattern_base(node_paths)
    print("Items    Condtional Pattern Base")
    for key, value in conditional_pattern_base.items():
        print(f" {key}        {value}")
        
    print("Frequent Itemsets are:")
    frequent_itemsets = extract_frequent_itemsets(conditional_pattern_base)
    for items in frequent_itemsets:
        print(items)
        
        
if __name__ == '__main__':
    main()

