
import random
BITS = 512

 
       

def get_prime():
    """Generate random prime of BITS size"""
    while True:
        prime_candidate = __get_low_level_prime(list_of_primes)
        if __miller_rabin_test(prime_candidate):
            return prime_candidate




def get_small_primes(number):
    """Get small primes using Sieve of Eratosthenes algorithm. 
        Return a list with primes smaller than or equal to number. It is also given that n is a small number.
    """
        # list of primes up to number
    list_of_primes = []       

    # Create a boolean array "prime[0..n]" and initialize  all entries it as true:

    prime = [True for i in range(number+1)]
        # first prime
    p = 2


        # algorithm:
    while p * p <= number:
        if prime[p] == True:
        # Update all multiples of p
            for i in range(p * p, number+1, p):
                prime[i] = False
        p+=1
        # return list of primes
    for i in range(number):
        if prime[i] == True:
            list_of_primes.append(i)        

    return list_of_primes[2:]


list_of_primes = get_small_primes(1000)


def __get_low_level_prime(list_of_primes):
    """
            The prime candidate is divided by the pre-generated primes to check for divisibility.
        Division with first primes to check for divisibility. If the Prime candidate is divisible 
        by any of the generated primes prior, the test fails and we take a new prime.
            This is repeated as long as a value which is coprime to all the primes in our generated
        primes list is found.
    """
        # get all primes up to 100


    while True:
             # Obtain a random number
        prime_candidate = __random_number() 
        for divisor in list_of_primes: 
            if prime_candidate % divisor == 0 and divisor  ** 2 <= prime_candidate:
                break
                # If no divisor found, return value
            else:
                return prime_candidate


def __miller_rabin_test(n, k=10):
    for i in range(k):
        a = random.randrange(2, n - 1)
        if not __single_test(n, a):
            return False
    return True
def __single_test(n, a):
    exp = n - 1
    while not exp & 1:
        exp >>= 1
            
    if pow(a, exp, n) == 1:
        return True
            
    while exp < n - 1:
        if pow(a, exp, n) == n - 1:
            return True
                
        exp <<= 1
            
    return False
    

 



    # return number of bit size n private function:
def __random_number():
    return(random.randrange(2**(BITS-1)+1, 2**BITS-1))

