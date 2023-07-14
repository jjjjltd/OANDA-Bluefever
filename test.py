def get_all_pairs(our_curr):
    
    pairs=[]
    
    for i in range(len(our_curr)):
        if i== 0:
            j=1
        else:
            j=0

        while (j) < len(our_curr):
            if i != j:
                pairs.append(f"{our_curr[i]}_{our_curr[j]}")
            j = j + 1
    
    return pairs

our_curr = ["EUR", "USD", "GBP", "JPY", "CHF", "NZD", "CAD"]
all_pairs = get_all_pairs(our_curr)
print(len(all_pairs))