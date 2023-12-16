import subprocess
import sys
from constants import SHADOW_GENERATOR_COMMAND

def generate_shadow(nb_users):
    subprocess.run(SHADOW_GENERATOR_COMMAND + [nb_users], check=True)

if __name__ == "__main__":
    generate_shadow(sys.argv[1])