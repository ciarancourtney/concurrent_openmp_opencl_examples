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






          



  
## References

R. P. Brent. The parallel evaluation of general arithmetic expressions. Journal of the Association
for Computing Machinery, 21(2):201–206, Apr. 1974.
