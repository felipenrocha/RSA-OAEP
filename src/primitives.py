#  https://www.inf.pucrs.br/~calazans/graduate/TPVLSI_I/RSA-oaep_spec.pdf

def i2osp(x: int, l: int):
    """
     Integer-to-Octet-String
    Input: 
        1. x -  nonnegative integer to be converted
        2. l  - intended length of the resulting octet string

    Output: 
        1. X - corresponding octet string of length l

    Errors: integer too large
    """

    # 2.  Write the integer x in its unique l-digit representation base 256:
    # 3. Let the octet Xi have the integer value xl−1 for 1 ≤ i ≤ l.
    #  Output the octet string X = X1X2 . . . Xl

    return x.to_bytes(l, byteorder='big')
   


def os2ip(X):
    """
    Input: 
        1. X -  octet string to be converted
    Output: 
        1. x  - corresponding nonnegative integer
    """
    # 1. Let X1X2 . . . Xn be the octets of X from first to last,
    #   and let Xi have the integer value xl−i for 1 ≤ i ≤ l.
    # 2. Let x = x_{l−1}256^(l−1) + x+{l−2}256^(l−2) + . . . + x1256 + x0.
    # 3. output x
    return int.from_bytes(X, byteorder='big')

def xor(x: bytes, y: bytes) -> bytes:
    '''Byte-by-byte XOR of two byte arrays'''
    return bytes(a ^ b for a, b in zip(x, y))