from itertools import combinations
from multiprocessing import Pool

def generate_itemsets(items, k):
    itemsets = [combo for combo in combinations(items, k)]
    return itemsets

def calculate_support(all_itemset, transaction):
    support_counts = {}
    for itemset in all_itemset:
        for t in transaction:
            if set(itemset).issubset(set(t)):
                support_counts.setdefault(tuple(itemset), 0)
                support_counts[tuple(itemset)] += 1
    
    return support_counts

def extract_frequent_itemsets(support_count, minsup):
    frequent_itemsets = {}
    for items, count in support_count.items():
        if count >= minsup:
            frequent_itemsets[items] = count
        
    return frequent_itemsets

def partition_transactions(transaction, num_partitions):
    partitions = [[] for _ in range(num_partitions)]
    for i, t in enumerate(transaction):
        partitions[i % num_partitions].append(t)
    return partitions

def process_partition(args):
    
    transaction, minsup = args
    k = 1
    items = sorted(set.union(*transaction))
    frequent_itemsets = {}
    while True:
        all_itemsets = generate_itemsets(items, k)
        temp_support_count = calculate_support(all_itemsets, transaction)
        new_frequent_itemsets = extract_frequent_itemsets(temp_support_count, minsup)
        if len(new_frequent_itemsets) > 0:
            frequent_itemsets.update(new_frequent_itemsets)
            prev = []
            for key in new_frequent_itemsets:
                prev.extend(key)
            items = sorted(set(prev))
        else:
            break
        k += 1
    return frequent_itemsets

def main():
    # taking input of transaction
    transaction = [
       {'A', 'E'},
       {'B', 'D'},
       {'D', 'E'},
       {'B', 'C'},
       {'E'},
       {'B', 'C', 'D'}
       ]
    
    num_partitions = int(input("Enter the number of partitions: "))
    num_partitions = int(len(transaction)/num_partitions)
    minsup = int(input("Enter the minimum support threshold: "))
    
    partitions = partition_transactions(transaction, num_partitions)
        
    with Pool() as pool:
        results = pool.map(process_partition, [(p, minsup) for p in partitions])
    
    print(results)
    all_frequent_itemsets = {}
    for frequent_itemsets in results:
        all_frequent_itemsets.update(frequent_itemsets)
    
    print("Final Frequent Itemsets:")
    for key, value in all_frequent_itemsets.items():
        print(f"{key} -> {value}")

if __name__ == "__main__":
    main()