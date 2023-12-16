// multiattack.c
// Starts multiple instances checking if a password can be found in the dictionnary.
// usage : nb_of_processus dictionnary_file shasum_file

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <sys/time.h>

#define RESULTS_PATH "results/m1results.txt"
//#define VERBOSE // Disable this line to remove print outputs

// Default maximum number of simultaneous process
int MAX_FILS = 5;

double time_diff(struct timeval *begin, struct timeval *end){
    return (double)(end->tv_sec - begin->tv_sec) + (double)(end->tv_usec - begin->tv_usec) / 1000000;
}

// wraup for readline
char *readline(FILE *f)
{
	char *line = NULL;

	size_t len = 0;
	ssize_t read;
	if ((read = getline(&line, &len, f)) != -1)
	{
		line[read - 2] = '\0';

		return line;
	}
	return NULL;
}

int main(int argc, char *argv[])
{
	#ifdef VERBOSE
	clock_t start = clock();
	#endif
	struct timeval begin_prgm, end_prgm, begin_parallel, end_parallel;
    gettimeofday(&begin_prgm, NULL);

	if (argc < 2)
	{
		fprintf(stderr, "Usage: '%s' nb_of_processus dictionnary_file shasum_file num_of_process\n", argv[0]);
		exit(EXIT_FAILURE);
	}
	char *p;
	MAX_FILS = strtol(argv[1], &p, 10);
	char *dict_file = argv[2];
	char *shasum_file = argv[3];

	// opening file
	FILE *ds = fopen(shasum_file, "r");
	if (ds == NULL)
		exit(EXIT_FAILURE);
	char *current_password_to_analyse = readline(ds);
	int current_checker_running = 0;

	gettimeofday(&begin_parallel, NULL);
	int n = 0;
	while (current_password_to_analyse != NULL)
	{
		for (; current_checker_running < MAX_FILS;)
		{ // forking until reaching MAX_FILS sons
			if ((n = fork()) < 0)
			{
				perror("fork error");
				exit(1);
			}
			if (n != 0)
			{ // Father code, so I'm couting one more son

				current_checker_running++;
				#ifdef VERBOSE
				printf("\n[INFO] Started  %dth son searching for password %s\n", current_checker_running, current_password_to_analyse);
				#endif
				current_password_to_analyse = readline(ds);
			}
			else
			{ // son code.
				execl("/bin/grep", "grep", current_password_to_analyse, dict_file, NULL);
				// There's no return from execl, remember it ?
			}

		} // for end. So I should have more or less MAX_FILS sons, until one's returning ...
		pid_t any_child;
		wait(&any_child);
		#ifdef VERBOSE
		printf("One of my son has finished\n. I'll start another one if I need to...");
		#endif
		// one son has terminated
		current_checker_running--;
	} // end while

	pid_t any_child;
	while ((wait(&any_child)) > 0); // this way, the father waits for all the child processes

	gettimeofday(&end_parallel, NULL);
	gettimeofday(&end_prgm, NULL);

    FILE *results = fopen(RESULTS_PATH, "a");
    fprintf(results, "%d:%f:%f\n", MAX_FILS, time_diff(&begin_parallel, &end_parallel), time_diff(&begin_prgm, &end_prgm));
    fclose(results);

	#ifdef VERBOSE
	clock_t end = clock();
	double elapsed_time = (double)(end - start) / CLOCKS_PER_SEC;
	printf("[INFO] Elapsed time : %lf\n", elapsed_time);
	#endif
	return 0;
}
