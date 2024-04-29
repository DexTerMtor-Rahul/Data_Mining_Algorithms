from itertools import combinations

def generate_itemsets(items, k):
    return [set(combo) for combo in combinations(items, k)]

def hash_function(itemset):
    order_sum = 0
    for item in itemset:
        for i, char in enumerate(sorted(item)):
            order = ord(char)
            order_sum += order * (10 ** i)
            i += 1
    return order_sum % 7

def calculate_support(all_itemset, transaction):
    hash_table = [[] for _ in range(7)]
    for itemset in all_itemset:
        hash_index = hash_function(itemset)
        count = sum(set(itemset).issubset(set(t)) for t in transaction)
        hash_table[hash_index].append((itemset, count))
    return hash_table

def extract_frequent_itemsets(hash_table, minsup):
    frequent_itemsets = []
    for bucket in hash_table:
        for itemset, count in bucket:
            if count >= minsup:
                frequent_itemsets.append((itemset, count))
    return frequent_itemsets

def main():
    # taking input of transaction
    transaction = [
        {'A', 'B', 'E'},
        {'B', 'D'},
        {'B', 'C'},
        {'A', 'B', 'D'},
        {'A', 'C'},
        {'B', 'C'},
        {'A', 'C'},
        {'A', 'B', 'C', 'E'},
        {'A', 'B', 'C'}
    ]

    k = 1
    minsup = int(input("Enter the minimum support threshold: "))
    items = sorted(set.union(*transaction))

    while True:
        all_itemsets = generate_itemsets(items, k)
        hash_table = calculate_support(all_itemsets, transaction)
        frequent_itemsets = extract_frequent_itemsets(hash_table, minsup)

        if len(frequent_itemsets) > 0:
            print(f"\nHash Table for {k}-itemsets:")
            for i in range(len(hash_table)):
                print(f"{i} -> {hash_table[i]}")
            
            print(f"Frequent Itemsets with Support >= {minsup}: ")
            for itemset, count in frequent_itemsets:
                print(f"{itemset} -> {count}")

            items = sorted(set.union(*[itemset for itemset, _ in frequent_itemsets]))
            
            print("Next items for frequent dataitemsets: ")
            print(items)
        else:
            break

        k += 1

if __name__ == "__main__":
    main()
