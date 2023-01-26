import src.primitives as primitives
from src.rsa import RSAKey

from Crypto.Util.asn1 import DerSequence
from Crypto.PublicKey import (_expand_subject_public_key_info)
from Crypto.Math.Numbers import Integer



def import_key(extern_key, passphrase=None):
    """Import an RSA key (public or private).
    """

    from Crypto.IO import PEM

    extern_key = primitives.tobytes(extern_key)
    if passphrase:
        passphrase = primitives.tobytes(passphrase)

   

    if extern_key.startswith(b'-----'):
        # This is probably a PEM encoded key.
        (der, marker, enc_flag) = PEM.decode(primitives.tostr(extern_key), passphrase)
        if enc_flag:
            passphrase = None
        return _import_keyDER(der, passphrase)


    raise ValueError("RSA key format is not supported")

oid = "1.2.840.113549.1.1.1"


# copied from Crypto but changed to my class
def construct(rsa_components):
    r"""Construct an RSA key from a tuple of valid RSA components.

    The modulus **n** must be the product of two primes.
    The public exponent **e** must be odd and larger than 1.
        ValueError: when the key being imported fails the most basic RSA validity checks.

    Returns: An RSA key object (:class:`RSAKey`).
    """

    class InputComps(object):
        pass

    input_comps = InputComps()
    for (comp, value) in zip(('n', 'e', 'd', 'p', 'q', 'u'), rsa_components):
        setattr(input_comps, comp, Integer(value))

    n = input_comps.n
    e = input_comps.e
    if not hasattr(input_comps, 'd'):
        key = RSAKey(modulus=n, e=e)
    else:
        d = input_comps.d
        if hasattr(input_comps, 'q'):
            p = input_comps.p
            q = input_comps.q
        else:
            # Compute factors p and q from the private exponent d.
            # We assume that n has no more than two factors.
            # See 8.2.2(i) in Handbook of Applied Cryptography.
            ktot = d * e - 1
            # The quantity d*e-1 is a multiple of phi(n), even,
            # and can be represented as t*2^s.
            t = ktot
            while t % 2 == 0:
                t //= 2
            # Cycle through all multiplicative inverses in Zn.
            # The algorithm is non-deterministic, but there is a 50% chance
            # any candidate a leads to successful factoring.
            # See "Digitalized Signatures and Public Key Functions as Intractable
            # as Factorization", M. Rabin, 1979
            spotted = False
            a = Integer(2)
            while not spotted and a < 100:
                k = Integer(t)
                # Cycle through all values a^{t*2^i}=a^k
                while k < ktot:
                    cand = pow(a, k, n)
                    # Check if a^k is a non-trivial root of unity (mod n)
                    if cand != 1 and cand != (n - 1) and pow(cand, 2, n) == 1:
                        # We have found a number such that (cand-1)(cand+1)=0 (mod n).
                        # Either of the terms divides n.
                        p = Integer(n).gcd(cand + 1)
                        spotted = True
                        break
                    k *= 2
                # This value was not any good... let's try another!
                a += 2
            if not spotted:
                raise ValueError("Unable to compute factors p and q from exponent d.")
            # Found !
            assert ((n % p) == 0)
            q = n // p

        if hasattr(input_comps, 'u'):
            u = input_comps.u
        else:
            u = p.inverse(q)

        # Build key object
        key = RSAKey(modulus=n, e=e, d=d, p=p, q=q, u=u)

    # Verify consistency of the key

    return key

def _import_keyDER(extern_key, passphrase):
    """Import an RSA key (public or private half), encoded in DER form."""

    decodings = (_import_pkcs1_private,
                 _import_pkcs1_public,
                 _import_subjectPublicKeyInfo)

    for decoding in decodings:
        try:
            return decoding(extern_key, passphrase)
        except ValueError:
            pass

    raise ValueError("RSA key format is not supported")

def _import_pkcs1_private(encoded, *kwargs):
    # RSAPrivateKey ::= SEQUENCE {
    #           version Version,
    #           modulus INTEGER, -- n
    #           publicExponent INTEGER, -- e
    #           privateExponent INTEGER, -- d
    #           prime1 INTEGER, -- p
    #           prime2 INTEGER, -- q
    #           exponent1 INTEGER, -- d mod (p-1)
    #           exponent2 INTEGER, -- d mod (q-1)
    #           coefficient INTEGER -- (inverse of q) mod p
    # }
    #
    # Version ::= INTEGER
    der = DerSequence().decode(encoded, nr_elements=9, only_ints_expected=True)
    if der[0] != 0:
        raise ValueError("No PKCS#1 encoding of an RSA private key")
    return construct(der[1:6] + [Integer(der[4]).inverse(der[5])])

def _import_pkcs1_public(encoded, *kwargs):
    # RSAPublicKey ::= SEQUENCE {
    #           modulus INTEGER, -- n
    #           publicExponent INTEGER -- e
    # }
    der = DerSequence().decode(encoded, nr_elements=2, only_ints_expected=True)
    return construct(der)

def _import_subjectPublicKeyInfo(encoded, *kwargs):

    algoid, encoded_key, params = _expand_subject_public_key_info(encoded)
    if algoid != oid or params is not None:
        raise ValueError("No RSA subjectPublicKeyInfo")
    return _import_pkcs1_public(encoded_key)