
import random

# generate large prime:

# https://www.geeksforgeeks.org/how-to-generate-large-prime-numbers-for-rsa-algorithm/

class PrimeGenerator:
    def __init__(self,bits=1024):
        # size of key in bits
        self.bits = bits
        while True:
            prime_candidate = self.__get_low_level_prime()
            if self.__miller_rabin_test(prime_candidate):
                self.prime = prime_candidate
                break
        

    # public methods:
    def get_prime(self):
        return self.prime

    # private methods:
    def __get_low_level_prime(self):
        """
            The prime candidate is divided by the pre-generated primes to check for divisibility.
        Division with first primes to check for divisibility. If the Prime candidate is divisible 
        by any of the generated primes prior, the test fails and we take a new prime.
            This is repeated as long as a value which is coprime to all the primes in our generated
        primes list is found.
        """
        # get all primes up to 100
        list_of_primes = self.__get_small_primes(100)

        while True:
             # Obtain a random number
            prime_candidate = self.__random_number() 
            for divisor in list_of_primes: 
                if divisor != 0 and prime_candidate % divisor == 0 and divisor**2 <= prime_candidate:
                    break
                # If no divisor found, return value
                else:
                    return prime_candidate
 
    def __get_small_primes(self, number=1000):
        """Get small primes using Sieve of Eratosthenes algorithm. 
        Return a list with primes smaller than or equal to number. It is also given that n is a small number.
        """
        # list of primes up to number
        list_of_primes = list()        

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

        return list_of_primes


#   https://www.youtube.com/watch?v=-BWTS_1Nxao:
    def isMillerRabinPassed(self, mrc):
        '''Run 20 iterations of Rabin Miller Primality test'''
        maxDivisionsByTwo = 0
        ec = mrc-1
        while ec % 2 == 0:
            ec >>= 1
            maxDivisionsByTwo += 1
        assert(2**maxDivisionsByTwo * ec == mrc-1)
    
        def trialComposite(round_tester):
            if pow(round_tester, ec, mrc) == 1:
                return False
            for i in range(maxDivisionsByTwo):
                if pow(round_tester, 2**i * ec, mrc) == mrc-1:
                    return False
            return True
    
        # Set number of trials here
        numberOfRabinTrials = 20
        for i in range(numberOfRabinTrials):
            round_tester = random.randrange(2, mrc)
            if trialComposite(round_tester):
                return False
        return True
    def __miller_rabin_test(self, n, k=20):
        for i in range(k):
            a = random.randrange(2, n - 1)
            if not self.__single_test(n, a):
                return False
        return True
    def __single_test(self, n, a):
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
    def __random_number(self):
        return(random.randrange(2**(self.bits-1)+1, 2**self.bits-1))

