"""
Daniel Baer
08.04.2026

mINF4/1, V01, "Maximale Abschnittssumme"

V01_02.py


This application implements the divide-and-conquer algorithm to find the maximum subarray sum in a given sequence of integers.
The algorithm finds the maximum subarray and outputs the maximum subarray sum along with its start and end.
"""


import math


def finde_zwischen(Z,l,m,r):
    
    global count_comp, count_add
    
    linksMax = -999999
    sum = 0
    
    # left side
    for i in range(m,l-1,-1):
        
        sum += Z[i]
        count_add += 1 # increment count of additions (and comparisons)
        
        if sum > linksMax:
            linksMax = sum
            links = i
        
    rechtsMax = -999999
    sum = 0
    
    # right side
    for i in range(m+1,r+1):
        
        sum += Z[i]
        count_add += 1 # increment count of additions (and comparisons)
        
        if sum > rechtsMax:
            rechtsMax = sum
            rZ = i
        
    return linksMax + rechtsMax, links, rZ


def maxfolge3(Z,l,r):
    if l == r:
        return Z[l],l,r
    else:
        m = (l+r)//2
        linksMax, linksL, linksR = maxfolge3(Z,l,m)
        rechtsMax, rechtsL, rechtsR = maxfolge3(Z,m+1,r)
        zwiMax, zwiL, zwiR = finde_zwischen(Z,l,m,r)
        
        if linksMax >= rechtsMax and linksMax >= zwiMax:
            return linksMax, linksL, linksR
        elif rechtsMax >= linksMax and rechtsMax >= zwiMax:
            return rechtsMax, rechtsL, rechtsR
        else:
            return zwiMax, zwiL, zwiR

    
def main() -> None:
    global count_add, count_comp
    
    # execute algorithm for each sequence file
    for i in range(4):

        count_add = 0
        
        filename = f"AlgoDatSoSe26/data/seq{i}.txt"
        
        # read in sequence from file
        with open(filename, 'r') as f:
            sequence = [int(line.strip()) for line in f]
            
        # execute algorithm
        max_sum, start, end = maxfolge3(sequence, 0, len(sequence)-1)
        
        # print out result
        print(f"seq{i} ({len(sequence)} elements): max sum = {max_sum}, from index {start} to {end} ({end-start+1} elements)")
        
        #print out counts of comparisons and additions
        complexity = (int)(len(sequence)*math.log2(len(sequence)))
        print(f"additions: {count_add}, n*ld(n): {complexity}, error: {count_add - complexity}\n")



if __name__ == "__main__":
    main()
