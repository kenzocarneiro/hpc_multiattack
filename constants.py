# Constants for the generators
DICT_GENERATOR_PATH = "data/my_sha_dict_generator"
DICT_GENERATOR_COMMAND = [DICT_GENERATOR_PATH, "data/dict.txt" ,"data/new_dict.txt"]
SHADOW_GENERATOR_PATH = "data/my_sha_shadow_generator"
SHADOW_GENERATOR_COMMAND = [SHADOW_GENERATOR_PATH, "data/dict.txt", "data/shadow.txt"]

# Constants for the multiattack algorithms
NUM_RUNS = 20
MAX_THREADS = 20
MULTIATTACK_ARGUMENTS = ["data/new_dict.txt", "data/shadow.txt"]
MULTIATTACK_ALGORITHMS = {
    'v1': './multiattacks/multiattackv1',
    'v2': './multiattacks/multiattackv2',
    'threaded': './multiattacks/threaded_multiattack',
}

# Constants for the results
RESULTS_PATHS = {
    'v1': "results/m1results.txt",
    'v2': "results/m2results.txt",
    'threaded': "results/m3results.txt"
}
TIME_LOGS_FILE_PATH = "results/time_logs.txt"
