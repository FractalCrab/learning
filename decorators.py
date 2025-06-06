from math import sqrt 

def is_prime(n):
    """
    Deterministic test based on the given pseudocode:
    n − 1 = 2^s · d  where d is odd.
    For all a in [2, min(n − 2, ⌊2 (ln n)^2⌋)]:
        compute x = a^d mod n
        repeat s times:
            y = x^2 mod n
            if y == 1 and x != 1 and x != n − 1:
                return False
            x = y
        if y != 1:
            return False
    return True
    """
    if n <= 3:
        return n == 2 or n == 3

    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    max_a = min(n - 2, int(2 * (math.log(n) ** 2)))

    for a in range(2, max_a + 1):
        x = pow(a, d, n) 

        for _ in range(s):
            y = pow(x, 2, n)  
            
            if y == 1 and x != 1 and x != n - 1:
                return False
            x = y
        
        if y != 1:
            return False

    return True



if __name__ == '__main__':
    n = int(input("Enter a number: "))
    print(is_prime(n))
    
