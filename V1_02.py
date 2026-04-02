"""
Daniel Baer
02.04.2026

mINF4/1, V1, "Maximale Abschnittssumme"

V1_02.py


This application implements the divide-and-conquer algorithm to find the maximum subarray sum in a given sequence of integers.
The algorithm finds the maximum subarray and outputs the maximum subarray sum along with its start and end.
"""


def finde_zwischen(Z,l,m,r):
    linksMax = -999999
    sum = 0
    for i in range(m,l-1,-1):
        sum += Z[i]
        if sum > linksMax:
            linksMax = sum
            links = i
    rechtsMax = -999999
    sum = 0
    for i in range(m+1,r+1):
        sum += Z[i]
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
    
    # execute algorithm for each sequence file
    for i in range(4):
        filename = f"AlgoDatSoSe26/data/seq{i}.txt"
        
        # read in sequence from file
        with open(filename, 'r') as f:
            Z = [int(line.strip()) for line in f]
            
        # execute algorithm
        max_sum, start, end = maxfolge3(Z, 0, len(Z)-1)
        
        # print out result
        print(f"seq{i}.txt: Max Sum = {max_sum}, from index {start} to {end}")



if __name__ == "__main__":
    main()
