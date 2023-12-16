// multiattack.c
// Starts multiple instances checking if a password can be found in the dictionnary.
// usage : nb_of_processus dictionnary_file shasum_file

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>

#define RESULTS_PATH "results/m2results.txt"
//#define VERBOSE // Disable this line to remove print outputs

double time_diff(struct timeval *begin, struct timeval *end){
    return (double)(end->tv_sec - begin->tv_sec) + (double)(end->tv_usec - begin->tv_usec) / 1000000;
}

int main(int argc, char *argv[])
{
	#ifdef VERBOSE
	clock_t start = clock();
	#endif
	struct timeval begin_prgm, end_prgm, begin_parallel, end_parallel;
    gettimeofday(&begin_prgm, NULL);

	int MAX_FILS = 5;
	if (argc < 2)
	{
		fprintf(stderr, "Usage: '%s' nb_of_processus dictionnary_file shasum_file\n", argv[0]);
		exit(EXIT_FAILURE);
	}
	char *p;
	MAX_FILS = strtol(argv[1], &p, 10);
	char *dict_file_name = argv[2];
	char *shasum_file_name = argv[3];

	// opening file
	FILE *shadow_file = fopen(shasum_file_name, "r");
	if (shadow_file == NULL)
		exit(EXIT_FAILURE);

	char current_password_to_analyse[2048];
	int current_checker_running = 0;

	gettimeofday(&begin_parallel, NULL);
	int n = 0;
	while (fgets(current_password_to_analyse, 1024, shadow_file) != NULL)
	{
		while (current_checker_running < MAX_FILS)
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
				printf("[INFO] Started  %dth son searching for password %s\n", current_checker_running, current_password_to_analyse);
				#endif
			}
			else
			{ // son code.
				char line[1024];
				FILE *dict_file = fopen(dict_file_name, "r");
				if (dict_file == NULL)
					exit(EXIT_FAILURE);

				while(fgets(line, 1024, dict_file) != NULL)
				{
					if (strstr(line, current_password_to_analyse) != NULL) {
						#ifdef VERBOSE
						printf("Password found: %s\n", line);
						#endif
						_exit(0);
					}
				}
				fclose(dict_file);
				_exit(0);
			}
		} // for end. So I should have more or less MAX_FILS sons, until one's returning ...
		pid_t any_child;
		wait(&any_child);
		#ifdef VERBOSE
		printf("One of my son has finished.\nI'll start another one if I need to...\n");
		#endif
		// one son has terminated
		current_checker_running--;
	} // end while

	fclose(shadow_file);
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
