from itertools import combinations, permutations

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

def generate_association_rules(frequent_itemsets, min_confidence, n):

    rules = []
    for itemset, support in frequent_itemsets.items():
        if len(itemset) == n:
            for i in range(2, len(itemset)):
                left_items = [x for x in permutations(itemset, i)]
                right_items = [x for x in permutations(itemset, len(itemset)-i)]
            
                for left in left_items:
                    for right in right_items:
                        if not set(right).issubset(set(left)):
                            confidence = frequent_itemsets[tuple(sorted(itemset))] / frequent_itemsets[tuple(sorted(left))]
                            if confidence >= min_confidence:
                                rule = (left, right, confidence)
                                rules.append(rule)
                left_items, right_items = right_items, left_items  
    
                for left in left_items:
                    for right in right_items:
                        if not set(left).issubset(set(right)):
                            confidence = frequent_itemsets[tuple(sorted(itemset))] / frequent_itemsets[tuple(sorted(left))]
                            if confidence >= min_confidence:
                                rule = (left, right, confidence)
                                rules.append(rule)
                
    return rules

def main():
    # taking input of transaction
    transaction = [
        {'A', 'B'},
        {'B', 'D'},
        {'B', 'C'},
        {'A', 'B', 'D'},
        {'A', 'C'},
        {'B', 'C'},
        {'A', 'C'},
        {'A', 'B', 'C', 'E'},
        {'A', 'B', 'C'}
        ]
   
    
    support_count = {}

    k = 1
    minsup = int(input("Enter the minimum support threshold: "))
    min_confidence_percentage = float(input("Enter the minimum confidence threshold (percentage): "))
    min_confidence = min_confidence_percentage / 100
    items = sorted(set.union(*transaction))
    n = 0
    while True:
        all_itemsets = generate_itemsets(items, k)
        temp_support_count = calculate_support(all_itemsets, transaction)
        frequent_itemsets = extract_frequent_itemsets(temp_support_count, minsup)
        
        if len(frequent_itemsets) > 0:
            print(f"Frequent Itemsets with Support >= {minsup}: ")
            prev = []
            for key, value in frequent_itemsets.items():
                print(f"{key} -> {value}")
                prev.extend(key)
            items = sorted(set(prev))
            support_count.update(frequent_itemsets)
            n = max(n, len(list(frequent_itemsets.keys())[-1]))
            print(n)
        else:
            break
       
        k += 1
        
    association_rules = generate_association_rules(support_count, min_confidence, n)

    print("Association Rules:")
    for left, right, confidence in association_rules:
        print(f"{tuple(left)} => {tuple(right)} (Confidence: {confidence:.2f})")
    

if __name__ == "__main__":
    main()