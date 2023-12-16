from constants import NUM_RUNS, MAX_THREADS, RESULTS_PATHS, MULTIATTACK_ALGORITHMS, MULTIATTACK_ARGUMENTS
import subprocess

def deep(algorithms):
    # remove the previous results
    for result in RESULTS_PATHS.values():
        with open(result, "w") as f:
            f.write("")

    for algorithm in algorithms:
        # run the program with 1 to MAX_THREADS threads
        for i in range(0, MAX_THREADS):
            # run the program NUM_RUNS times for each number of threads
            for j in range(NUM_RUNS):
                # launch this command and wait for it to finish : ./new_parallel_test new_dict.txt shadow.txt
                executed_command = [algorithm + ".out", str(i+1)] + MULTIATTACK_ARGUMENTS
                subprocess.run(executed_command, check=True)
                print("Finished run "+str(j+1)+" with "+str(i+1)+" threads")


if __name__ == "__main__":
    deep(MULTIATTACK_ALGORITHMS.values())
