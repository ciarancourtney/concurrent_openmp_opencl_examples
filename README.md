# CA670 Concurrent Programming - Assignment 2

Name: Ciaran Courtney

Date: 15 April 2017

## Spec

In this assignment you are to develop an efficient implementation of the Parallel Sum Reduction operator that computes 
the sum of a large array of values in both OpenMP and OpenCL. A prime criterion in the assessment of your assignment 
will be the efficiency of both your implementations and the evidence you present to substantiate your claim that your 
implementations are efficient.

## Introduction

The aim of _Parallel Sum Reduction_ is to sum all elements of a given vector. For example, to serially reduce the vector w:

    w = [1, 2, 3, 4, 5]
    
      = [((((1 + 2) + 3) + 4) + 5)]
      
      = 15
      
requires 4 summing operations. Reordering the elements does not affect the result of the reduction, making it a commutative. 

    [((((5 + 4) + 3) + 2) + 1)]

Likewise, grouping the additions in an different manner would not affect the result, this means the reduction is also associative.

    [(5 + (4 + (3 + (2 + 1))))]
    
Taking these properties into account this operation is ripe for paralleling. In the first example there are 4 steps (n = 4) required
to obtain the sum. Grouping the first addition into three groups and reducing the sum at each step looks like this:

    (n=1)   (1+2) (3+4) (5) 
    (n=2)   (3+7) (5)
    (n=3)   (10+5)
            (15)

Here we have reduced the number of steps required to 3 (n=3). If we imagine an example where 1024 numbers are to be summed,
serially we know this would take 1023 operations. Assuming an unlimited number of cores are available, this operation would
take 10 steps, as we know the first step requires 512 operations, the 2nd 256 and so on until a result is obtained. 
So a parallel sum reduction has step complexity ceiling of log2(n) or in Big O notation, O(log n). Now, to put that into real world
terms were cores are finite, Brent's Theorem tries to obtain the maximum speedup that parallelism can obtain for a given core count.
If a parallel algorithm does a number of operations (m) in unit time (t), then on (p) processors the same algorithm can 
be done in time tp where:


    tp <= t + (m-t)/p          
          
So for the 1024 operation example, on a four core machine it would take 256.75sec in total compared to 1024sec, assuming
each operation takes 1sec.


## Toolchain

### Linux subsystem on Windows 10
- OS: Ubuntu 16.04 and Windows Subsystem for Linux (WSL) https://msdn.microsoft.com/en-us/commandline/wsl/about?f=255&MSPPError=-2147217396
- C Compiler: GCC 5.4.0 (OpenMP 4.0 support)

### Windows 10
- OS: Windows 10 x64
- C Compiler: Intel C/C++ compiler 17.0.2 (OpenMP 4.5 support)

## Method
  
### C Implementation (pure_c_array_reduce.c)

As both openMP and openCL support C, it was decided to create a base method in pure C to perform a sum reduction, and then
extend the code to work in openMP and openCL.

Usage:

    icl pure_c_array_reduce.c -o pure_c_array_reduce.c
    ./pure_c_array_reduce <array_size> <range> --verbose
    ./pure_c_array_reduce 1000000000 100 --verbose

* An array of random integers are created conforming to the stdin
  * int array_size - number of random elements to create in array
  * int range - the maximum integer to random generate i.e. between zero and range-1

* sscanf() is used to parse stdin arguments as integers
* malloc() is used to allocate memory in the stack for the variable sized array
* Random numbers are seeded based on time
* An array of random integers is generated using rand() in a for loop
* The reduction sum is calculated using a for loop into the variable sum, a long integer.
* clock() is used to calculate the CPU time that the reduction loop consumes
* After the reduction is down and total time is output to stdout, the allocated memory is cleared using free() and
the program returns 0
  
### OpenMP Implementation in C (openmp_array_reduce.c)
  
The advantage of OpenMP is take it is easy to employ parallelism to a serial piece of C/C++ code without changing code
dramatically. OpenMP offers several clauses that try to add parallelism to common serial code e.g. for loops.
One such clause is REDUCTION, which can be decorated on any for loops that perform a certain operation, i.e. summing.
 
C summing for loop:

    for (j = 0; j < array_length; j++) {
        sum = sum + array[j] ;
    }
    
OpenMP summing for loop:

    #pragma omp parallel for reduction(+ : sum)
    for (j = 0; j < array_length; j++) {
        sum = sum + array[j] ;
    }

The OpenMP REDUCTION clause knows that the sum variable is a shared variable which is modified in every iteration.
Without the REDUCTION clause, we would introduce a race condition, as concurrent threads try to update the shared variable 
at the same time. In the above code sample, the reduction parameters are:

* The operation (+)
* The reduction variable (sum)

OpenMP launches threads to compute each for loop concurrently. On the first iteration it knows that for array length 1024,
512 summing operations are required, so on a 4 core machine this will mean 512/4 operations to be performed serially per core.
Each thread has its own local copy of the sum variable so that it doesn't clash with any of the other concurrent threads.
After the last iteration, all local copies of the sum variable are combined into the shared variable. 

**Intel Compile Instructions**

    icl /MD /Qopenmp openmp_array_reduce.c -o openmp_array_reduce
    
This will output a windows exe binary named openmp_array_reduce.exe.

**C Vs OpenMP results**

A significant speedup was found with the most simple form of reduction pragma added to the for loop. At the top end
of 512,000,000 elements, a 2x speedup was found (0.2036sec Vs 0.1018sec).

![Alt text](results/c_vs_openmp.png?raw=true)


## References

R. P. Brent. The parallel evaluation of general arithmetic expressions. Journal of the Association
for Computing Machinery, 21(2):201–206, Apr. 1974.

http://jakascorner.com/blog/2016/06/omp-for-reduction.html 

Intel Compiler notes https://software.intel.com/en-us/intel-cplusplus-compiler-17.0-user-and-reference-guide

The compiler supports many OpenMP* features, including all of OpenMP* Version 4.0 and most of OpenMP* Version 4.5.

Get Intel Parallel Studio ZE 2017 free for academic use from here https://software.intel.com/en-us/intel-parallel-studio-xe

See here for notes on compiler CLI arguments https://software.intel.com/en-us/node/522690
