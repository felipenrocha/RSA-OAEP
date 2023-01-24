

from src.key_gen import KeyGen
import time

def main():
    key_gen = KeyGen()

    return 0


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s Total seconds ---" % (time.time() - start_time))
