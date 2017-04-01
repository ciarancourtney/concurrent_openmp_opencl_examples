#include <stdio.h>
#include <stdlib.h>
#include <string.h>  // for memset (create variable length arrays)
#include <time.h>    // for time


int main(int argc, char *argv[]) {

    if (argc < 3) {
        fprintf(stderr, "usage: %s <array_length> <range>\n", argv[0]);
        exit(1);
    }

    // parse string args as integers
    int array_length;
    sscanf (argv[1],"%d",&array_length);

    int max_int;
    sscanf (argv[2],"%d",&max_int);

    // create variable length array
    int array[array_length];

    // allocate memory for array
    memset(array, 0, sizeof array);

    // intialize Pseudo-Random Number Generator based on current time
    srand(time(NULL));

    // Create array of length array_length consisting of random ints in range 0 to (max_int-1)
    int i;
    for(i = 0; i < array_length; i++){
        array[i]=(rand()%max_int);
    }

    // print to console for user
    for(i = 0; i < array_length; i++){
        printf("%d\n", array[i]);
    }

    // Sum all integers in array and print result to stdout
    int sum = 0;
    int j;
    clock_t begin = clock();
    for (j = 0; j < array_length; j++) {
        sum = sum + array[j] ;
    }
    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("%d\n", sum);
    printf("Time Taken: %f\n", time_spent);

}
