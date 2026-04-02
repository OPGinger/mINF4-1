"""
Daniel Baer
02.04.2026

mINF4/1

V1_01.py

Application for testing the dependency of the number of additions inf summe_quadrate(n) on n 
"""


def summe_quadrate(n) -> int:
    s = 0
    c = 0
    
    for i in range(1, n+1):
        for j in range(1, i+1):
            c += 1                                  # increment count
            s = s+j                                 # addidtion
            
    print("count    = ", c)                         # output count of additions
    return s

def main() -> None:
    
    for i in range(1, 10):
        print("n        = ", i)                     # output n
        print("n!       = ", (int)(i*(i+1)/2))      # output n!
        print("f(n)     = ", summe_quadrate(i))     # output f(n)
        print()
    


if __name__ == "__main__":
    main()

