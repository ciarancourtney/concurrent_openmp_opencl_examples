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

- OS: Windows 10 x64 with Visual Studio 2015 Community Edition

**OpenMP**
- C Compiler: Intel C/C++ compiler 17.0.2 (OpenMP 4.5 support)

**OpenCL**
- C Compiler: Intel C/C++ compiler 17.0.2 (OpenCL 2.1 support)
- OpenCL Driver: Intel® SDK for OpenCL™ Applications for Windows 6.3.0.1904 (2016-11-02)


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


### OpenCL Implementation in python (opencl_array_reduce.py)

**OpenCL** environment install steps

After much frustration trying to get VS2015 and Intel OpenCL SDK to play nice, and trying and failing  GCC for windows, it was 
decided to instead use pyopencl to run the kernel code.

**pyopencl** 

There are still many barriers to cross when building pyopencl [on windows](https://wiki.tiker.net/PyOpenCL/Installation/Windows#Installing_PyOpenCL_on_Windows)
Downloading and installing a prebuilt binary for windows from [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopencl) bypassed these issues and saved a lot of time.

Basic requirements
* Python 3.6
* pyopencl
* numpy (for creating c-like arrays)

pyopencl automatically detects the Intel SDK, or it can be specified using the PYOPENCL_CTX environment variable.

Based on the pyopencl [array multiplication benchmark](https://github.com/pyopencl/pyopencl/blob/master/examples/benchmark.py)
a similar piece of code was derived to instead calculate sum reduction using OpenCL

OpenCL Terms:

Device: CPU or GPU that can be used with the OpenCL API

Context: A set of one or more devices.

Platform: Contains information about the machine and the implementation version of OpenCL

Program: Contains the source code of the functions to be executed in OpenCL.

CommandQueue: Command queue to run. A command can be, for example: Read or write a buffer, execute a function

**Memory Allocation**

An array of random integers is defined using numpy with dtype int32. This allocation with numpy allows us to create an
array at the host. We must now declare the same array at the __global memory of OpenCL. To do this you have to create buffers in the context.


**kernel code** 


    __kernel void reduce(__global int *a, __global int *r, __local int *b) {
        uint global_id = get_global_id(0);
        uint group_id = get_group_id(0);
        uint local_id = get_local_id(0);
        uint local_size = get_local_size(0);
    
        b[local_id] = a[global_id];
        barrier(CLK_LOCAL_MEM_FENCE);
    
        for(uint s = local_size/2; s > 0; s >>= 1) {
        if(local_id < s) {
          b[local_id] += b[local_id+s];
        }
        barrier(CLK_LOCAL_MEM_FENCE);
        }
        if(local_id == 0) r[group_id] = b[local_id];
    }

The __kernel keyword is there to say that this is a main function of the program. It is a function that we can call from our program in python.
The __global keyword is there to say that this is a parameter stored in the global memory, the memory of the context. 
The function __get_global_id(0)__ returns the global index.

During kernel runtime, all integers are copied into shared memory (VRAM), which is much less than the system memory (RAM).
The first N/2 numbers on the left side are taken and added to the other N/2 numbers on the right side. Then half of those
and added to the next half until only one number, the result, remains.

CLK_LOCAL_MEM_FENCE barriers will either flush any variables stored in local memory or queue a memory fence to ensure
correct ordering of memory operations to local memory.

**Runtime**

The implementation of pyopencl allows us again to simplify the use of opencl. It is no longer necessary to create a Kernel
object to use it, nor to pass the arguments one by one. To reduce the Array we simply call the function sum (A, B, C) on the set of elements, we simply write

    cl_kernel.reduce(queue, (N,), (thread_count,), array_buf, placeholder_buf, local_buf)

Reduce must be called once more to obtain the final sum into result_sum_buf:

    evt = cl_kernel.reduce(queue, (thread_count,), (thread_count,), placeholder_buf, result_sum_buf, local_buf)

Then the result is stored in result_sum_buf, must be transferred from the context to the host:

    cl.enqueue_copy(queue, result_sum, result_sum_buf)

The result can then be compared with a call to numpy.sum to confirm correctness.

    print(result_sum, np.sum(array))  # uncomment this line to check

**C Vs OpenMP Vs OpenCL results**

![Alt text](results/c_vs_openmp_vs_opencl.png?raw=true)

Unfortunately due to GPU memory constraints and the fact that N must be a multiple of the worker size, I wasn't able to
reduce an array length larger than 67,108,864, but results show that at size 33,554,432, OpenCL is doing the reduction
10x faster then near equivalent array size in serial C or multithreaded C with OpenMP. Also the time taken is linear with
array size.

## Conclusion

Creating a fair comparison between OpenCL and the other methods is difficult, as the array size must be a specific multiple
of the worker count, and also host GPU memory constraints. But the speedup found when doing Parallel Sum Reduction is 
very significant.

At the moment the greatest difficulty with OpenCL is resolving the nuanced issues between different GPU hardware, associated
drivers and SDKs, Windows compiler issues, and also OpenCL versions. PyOpenCL can ease the burden of auto-detecting
installed SDKs on windows and wrapping & executing CL code.


## References

Private Github repo available at https://github.com/ciarancourtney/concurrent_openmp_opencl_examples
This repo will be public from April 25th to Summer 2017 to aid marking, it will be made private again to avoid future 
plagiarism for future CA670 assignments. Please do not hesitate to ask if there are any issues with this, or problems reproducing benchmarks.

R. P. Brent. The parallel evaluation of general arithmetic expressions. Journal of the Association
for Computing Machinery, 21(2):201–206, Apr. 1974.

http://jakascorner.com/blog/2016/06/omp-for-reduction.html 

Intel Compiler notes https://software.intel.com/en-us/intel-cplusplus-compiler-17.0-user-and-reference-guide

The compiler supports many OpenMP* features, including all of OpenMP* Version 4.0 and most of OpenMP* Version 4.5.

Get Intel Parallel Studio ZE 2017 free for academic use from here https://software.intel.com/en-us/intel-parallel-studio-xe

See here for notes on compiler CLI arguments https://software.intel.com/en-us/node/522690

PyOpenCL documentation https://documen.tician.de/pyopencl/
