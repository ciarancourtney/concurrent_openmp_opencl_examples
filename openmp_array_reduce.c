#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>


int main(int argc, char *argv[]) {

    if (argc < 3) {
        fprintf(stderr, "usage: %s <array_length> <range> <--verbose>\n", argv[0]);
        exit(1);
    }

    // parse string args as integers
    int array_length;
    sscanf (argv[1],"%d",&array_length);

    int max_int;
    sscanf (argv[2],"%d",&max_int);

    // create variable length array pointer and allocate enough memory for that number of ints (4 bytes each)
    int *array;
    array = malloc(array_length * sizeof(*array));
    if (array == NULL) {
        printf("Error allocating memory!\n");
        exit(1);
    }

    // intialize Pseudo-Random Number Generator based on current time
    srand(time(NULL));

    // Create array of length array_length consisting of random ints in range 0 to (max_int-1)
    int i;
    for(i = 0; i < array_length; i++){
        array[i]=(rand()%max_int);
    }

    // Sum all integers in array and print result to stdout
    long int sum = 0;
    int j;

    clock_t begin = clock();

    #pragma omp parallel for reduction(+:sum)
        for (j = 0; j < array_length; j++) {
            sum = sum + array[j] ;
        }

    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;

    if(argc > 3) {
        printf("Total Sum: %ld\n", sum);
        printf("Time Taken: %f\n", time_spent);
    } else {
        printf("%f\n", time_spent);
    }
    free(array);
}
