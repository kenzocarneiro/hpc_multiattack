import sys
import subprocess
from constants import *
from deep_launch import deep
from quick_launch import quick
from analyzer import analyze
from generate_dict import generate_dict
from generate_shadow import generate_shadow

def print_shadow_help():
    print("----- Help for the shadow file -----")
    print("Usage: python3 main.py shadow <nb_users>")
    print("nb_users: the number of users in the shadow file (must be > 0)")


def print_deep_help():
    print("----- Help for the deep algorithm -----")
    print("Usage: python3 main.py deep <all/v1/v2/threaded>")
    print("all: run all the algorithms")
    print("v1: run the first algorithm")
    print("v2: run the second algorithm")
    print("threaded: run the threaded algorithm")

def print_analyze_help():
    print("----- Help for the analyze algorithm -----")
    print("Usage: python3 main.py analyze <all/v1/v2/threaded>")
    print("all: analyze all the algorithms")
    print("v1: analyze the first algorithm")
    print("v2: analyze the second algorithm")
    print("threaded: analyze the threaded algorithm")

def print_help():
    print("----- Help -----")
    print("Usage: python3 main.py <gcc/dict/shadow/quick/deep/analyze>")
    print("--- Compile ---")
    print("gcc: compile the programs")
    print("--- Data Generators ---")
    print("dict: generate a new dictionary")
    print("shadow: generate a new shadow file.")
    print("--- Launch & Analyze ---")
    print("quick: launch each program with 8 threads and calculate the global time of each.")
    print(f"deep: launch each program with 1 to {MAX_THREADS} threads on {NUM_RUNS} runs and calculate the parallel and total times for each.")
    print("analyze: analyze the results of the deep run and plot the times and the speedup.")

def main():
    if len(sys.argv) < 2 or (len(sys.argv) > 2 and sys.argv[1] not in ("shadow", "deep", "analyze")):
        print_help()
        return

    match sys.argv[1]:
        case "gcc":
            print("--- generators ---")
            subprocess.run(f"gcc {DICT_GENERATOR_PATH}.c -o {DICT_GENERATOR_PATH}.out -lssl -lcrypto".split(), check=True)
            print("Compiled my_sha_dict_generator")
            subprocess.run(f"gcc {SHADOW_GENERATOR_PATH}.c -o {SHADOW_GENERATOR_PATH}.out -lssl -lcrypto".split(), check=True)
            print("Compiled my_sha_shadow_generator")
            print("\n--- multiattack ---")
            subprocess.run(f"gcc {MULTIATTACK_ALGORITHMS['v1']}.c -o {MULTIATTACK_ALGORITHMS['v1']}.out  -Wall".split(), check=True)
            print("Compiled multiattackv1")
            subprocess.run(f"gcc {MULTIATTACK_ALGORITHMS['v2']}.c -o {MULTIATTACK_ALGORITHMS['v2']}.out -Wall".split(), check=True)
            print("Compiled multiattackv2")
            subprocess.run(f"gcc {MULTIATTACK_ALGORITHMS['threaded']}.c -o {MULTIATTACK_ALGORITHMS['threaded']}.out -fopenmp -Wall".split(), check=True)
            print("Compiled threaded_multiattack")
            print("\nFinished compiling.")
        case "dict":
            generate_dict()
            print("Generated new_dict.txt")
        case "shadow":
            if len(sys.argv) != 3 or int(sys.argv[2]) < 1:
                print_shadow_help()
                return

            generate_shadow(sys.argv[2])
            print("Generated shadow.txt with "+sys.argv[2]+" users")
        case "quick":
            quick()
        case "deep":
            if len(sys.argv) != 3 or sys.argv[2] not in ["all", "v1", "v2", "threaded"]:
                print_deep_help()
                return
            if sys.argv[2] == "all":
                deep(MULTIATTACK_ALGORITHMS.values())
            else:
                deep([MULTIATTACK_ALGORITHMS[sys.argv[2]]])
        case "analyze":
            if len(sys.argv) != 3 or sys.argv[2] not in ["all", "v1", "v2", "threaded"]:
                print_analyze_help()
                return
            if sys.argv[2] == "all":
                analyze(MULTIATTACK_ALGORITHMS.keys())
            else:
                analyze([sys.argv[2]])
        case _:
            print_help()

if __name__ == "__main__":
    main()
