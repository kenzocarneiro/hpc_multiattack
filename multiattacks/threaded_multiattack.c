// multiattack.c
// Starts multiple instances checking if a password can be found in the dictionnary.
// usage : nb_of_processus dictionnary_file shasum_file

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <omp.h>
#include <time.h>
#include <sys/time.h>

#define MAX_LINE 1024

#define RESULTS_PATH "results/m3results.txt"
// #define VERBOSE // Disable this line to remove print outputs

double time_diff(struct timeval *begin, struct timeval *end){
    return (double)(end->tv_sec - begin->tv_sec) + (double)(end->tv_usec - begin->tv_usec) / 1000000;
}

char* grep(char* current_password_to_analyse, char * dict_file_name){
    char* line = NULL;
    line = malloc((MAX_LINE + 1)  * sizeof(char));
    bzero(line, MAX_LINE + 1);

    FILE *dict_file = fopen(dict_file_name, "r");
    if (dict_file == NULL)
    {
        perror("Error opening dictionnary file");
        exit(EXIT_FAILURE);
    }

    while(fgets(line, MAX_LINE, dict_file) != NULL)
    {
        if (strstr(line, current_password_to_analyse) != NULL) {
            #ifdef VERBOSE
            printf("Password found: %s\n", line);
            #endif
            fclose(dict_file);
            return line;
        }
    }

    free(line);
    fclose(dict_file);
    return NULL;
}


int main(int argc, char *argv[]) {
    struct timeval begin_prgm, end_prgm, begin_parallel, end_parallel;
    gettimeofday(&begin_prgm, NULL);

    int nb_threads = atoi(argv[1]);
    char *dict_file = argv[2];
    char *shasum_file = argv[3];

    omp_set_num_threads(nb_threads);

    #ifdef VERBOSE
    int thread_id;
    #endif
    int nb_passwords = 0;

    // opening file
    FILE * shadow = fopen(shasum_file, "r");
    if (shadow == NULL)
    {
        perror("Error opening dictionnary file");
        exit(EXIT_FAILURE);
    }

    gettimeofday(&begin_parallel, NULL);

    #ifdef VERBOSE
    #pragma omp parallel private(thread_id) shared(shadow, dict_file, nb_passwords)
    #else
    #pragma omp parallel shared(shadow, dict_file, nb_passwords)
    #endif
    {
        #ifdef VERBOSE
        thread_id = omp_get_thread_num();

        printf("Thread %d is starting\n", thread_id);
        #endif

        char password[MAX_LINE+1];
        bzero(password, MAX_LINE + 1);

        //iterate over the shadow file
        while(fgets(password, MAX_LINE, shadow) != NULL){
            //compare the current_password_to_analyse with the password
            char * result = grep(password, dict_file);

            if(result != NULL) {
                #ifdef VERBOSE
                printf("Thread %d found the password %s\n", thread_id, result);
                #endif
                nb_passwords++;
                free(result);
            }
        }
        #ifdef VERBOSE
        printf("Thread %d is exiting\n", thread_id);
        #endif
    }

    gettimeofday(&end_parallel, NULL);

    #ifdef VERBOSE
    printf("Number of passwords found : %d\n", nb_passwords);
    #endif

    // closing file
    fclose(shadow);

    gettimeofday(&end_prgm, NULL);

    #ifdef VERBOSE
    printf("Time spent in parallel :%f\nTime spent in total :\t%f\n", time_diff(&begin_parallel, &end_parallel), time_diff(&begin_prgm, &end_prgm));
    printf("Number of threads : %d\n", omp_get_max_threads());
    #endif

    FILE *results = fopen(RESULTS_PATH, "a");
    fprintf(results, "%d:%f:%f\n", omp_get_max_threads(), time_diff(&begin_parallel, &end_parallel), time_diff(&begin_prgm, &end_prgm));
    fclose(results);

    return 0;
}
