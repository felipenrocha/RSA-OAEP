
def egcd(a, b):
    """Extenden euclidean algorithm"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
def gcd(a, b):
    """Greatest Common divisor"""
    while a != 0:
      a, b = b % a, a
    return b

def is_coprime(x, y):
        """Return if x is coprime with y"""
        return gcd(x, y) == 1
def find_mod_inverse(a, m):
    """Return mod inverse multiplicative"""
    # obs.: im using pow(a,b,c) instead.
    g, x, y = egcd(a, m)
    if g != 1:
        return -1
    else:
        return x % m