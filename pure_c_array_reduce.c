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

}