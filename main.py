

from src.prime_generation import get_prime
import time

def main():
    # p = PrimeGenerator(1024)

    print("As chaves primas p e q são: ")
    print(get_prime())
    print("--- %s seconds ---" % (time.time() - start_time))

    print("\n e \n")
    print(get_prime())


    return 0


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s Total seconds ---" % (time.time() - start_time))
