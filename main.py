

from src.prime_generation import PrimeGenerator

def main():
    p = PrimeGenerator(1024)
    q = PrimeGenerator(1024)
    print("As chaves primas p e q são: ")
    print(q.get_prime())
    print("\n e \n")
    print(p.get_prime())
    return 0


if __name__ == '__main__':
    main()