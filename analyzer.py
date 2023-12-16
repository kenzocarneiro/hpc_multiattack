from constants import MAX_THREADS, RESULTS_PATHS, MULTIATTACK_ALGORITHMS
import matplotlib.pyplot as plt

def get_times(results_path):
    #take all the times for the total and parallel runs and put them in a list, then display them with matplotlib
    total_times = [[] for i in range(MAX_THREADS)]
    par_times = [[] for i in range(MAX_THREADS)]

    #read times from file
    with open(results_path, "r") as f:
        for line in f:
            #the lines are formatted like this: "number of threads:parallel time:total time"
            nb_threads, par_time, total_time = line.split(":")
            nb_threads, par_time, total_time = int(nb_threads), float(par_time), float(total_time)
            assert nb_threads <= MAX_THREADS, "The number of threads in the file is bigger than MAX_THREADS"
            total_times[nb_threads-1].append(total_time)
            par_times[nb_threads-1].append(par_time)

    return total_times, par_times

def get_mean_times(total_times, par_times):
    # # Check that the analyzer was run until the end: the number of threads should be MAX_THREADS
    # assert len(total_times) == MAX_THREADS, "The number of threads is not "+str(MAX_THREADS)
    # assert len(total_times) == len(par_times), "The number of total and parallel times is not the same"

    #make the average of the times for each number of threads
    for i in range(MAX_THREADS):
        assert len(total_times[i]) == len(par_times[i]), "The number of total and parallel times is not the same for "+str(i+1)+" threads"
        assert len(total_times[i]) > 0, "No times for "+str(i+1)+" threads"
        total_times[i] = sum(total_times[i])/len(total_times[i])
        par_times[i] = sum(par_times[i])/len(par_times[i])
    return total_times, par_times

def reversed_amdahl_law(f, p):
    return 1/(f + (1-f)/p)

def amdahl_law(p, s):
    return 1/((1-p) + p/s)

def get_amdahl_speedup(total_times, par_times):
    #plot the ahmdal's law
    speedup = []
    for i in range(MAX_THREADS):
        # f = temps total de la partie qui ne sera pas parallélisée / temps total du programme
        # f = (temps total du programme - temps total de la partie qui sera parallélisée) / temps total du programme
        f = (total_times[i] - par_times[i])/total_times[i]
        p = i+1
        speedup.append(reversed_amdahl_law(f, p))

    return speedup

def analyze(algorithms):
    total_algo_times = {}
    for algorithm in algorithms:
        total_times, par_times = get_times(RESULTS_PATHS[algorithm])
        total_mean_times, par_mean_times = get_mean_times(total_times, par_times)
        total_algo_times[algorithm] = total_mean_times

        seq_times = [total_mean_times[i] - par_mean_times[i] for i in range(MAX_THREADS)]

        #plot the times (the number of threads is the position in the list + 1)
        plt.plot(range(1, MAX_THREADS+1), total_mean_times, label="Total", color="red", marker="o")
        plt.plot(par_mean_times, label="Parallel", color="blue", marker="x")
        plt.plot(seq_times, label="Sequential", color="green", marker="^")
        plt.xlabel("Number of threads")
        plt.ylabel("Time (s)")
        plt.legend()
        plt.title(f"Times for multiattack {algorithm}")
        plt.savefig(f"figures/times_{algorithm}.png")
        plt.clf()

        # plot only the sequential times
        plt.plot(range(1, MAX_THREADS+1), seq_times, label="Sequential", color="green", marker="^")
        plt.xlabel("Number of threads")
        plt.ylabel("Time (s)")
        plt.legend()
        plt.title(f"Times for multiattack {algorithm}")
        plt.savefig(f"figures/seq_{algorithm}.png")
        plt.clf()

        speedup = get_amdahl_speedup(total_mean_times, par_mean_times)

        plt.plot(speedup, label="Speedup")
        plt.xlabel("Number of threads")
        plt.xscale('log', base=2)
        plt.ylabel("Speedup")
        plt.legend()
        plt.title(f"Ahmdal's law for multiattack {algorithm}")
        plt.savefig(f"figures/speedup_{algorithm}.png")
        plt.clf()

    if len(algorithms) > 1:
        plt.plot(range(1, MAX_THREADS+1), total_algo_times['v1'], label="v1 (fork)", color="red", marker="o")
        plt.plot(range(1, MAX_THREADS+1), total_algo_times['v2'], label="v2 (optimized fork)", color="blue", marker="x")
        plt.plot(range(1, MAX_THREADS+1), total_algo_times['threaded'], label="v3 (OpenMP)", color="green", marker="^")
        plt.xlabel("Number of threads")
        plt.ylabel("Time (s)")
        plt.legend()
        plt.title("Comparison of total times for all algorithms")
        plt.savefig(f"figures/times_all.png")
        plt.clf()


if __name__ == "__main__":
    analyze(MULTIATTACK_ALGORITHMS.keys())
