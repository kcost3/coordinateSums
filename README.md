# coordinateSums

For  a  natural  number *n*, we  can  consider vectors of length *d* with entries in the integers modulo n. They form the set (**Z**/n**Z**)<sup>d</sup>. Inside that set, let *G(n,d)* denote the set of vectors such that 0 does not occur as a sum of some of the coordinates. For example, G(n, 2) consists of the vectors (x, y) in (**Z**/n**Z**)<sup>2</sup> such that x, y, and x + y are nonzero modulo n. What can be said about this set and its cardinality? 

To gain intution for this problem, we provide a brute force recursive algorithm for computing the vectors of G(n, d) for given values of n, d. From here, the cardinality of G(n, d) can be computed, and we provice exact solutions to |G(n, d)| for specific values of n, d. This code was used for a project in the MIT math class 18.821 - Project Laboratory in Mathematics. 
