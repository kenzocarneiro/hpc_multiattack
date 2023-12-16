import subprocess
from constants import DICT_GENERATOR_COMMAND

def generate_dict():
    subprocess.run(DICT_GENERATOR_COMMAND, check=True)

if __name__ == "__main__":
    generate_dict()