## MohuPy

1. Q-rung orthopair fuzzy numbers and Q-rung orthopair interval-valued fuzzy numbers
   1. Definition
   2. Addition, subtraction, multiplication, division, power and comparison operations (operator overloading)
   3. intersection operation
   4. Legality judgment, null judgment, conversion, Q-order plane diagram of fuzzy numbers
   5. Random function, fuzzy number character conversion
   6. Generalized Q-rung orthopair fuzzy distance
   7. Einstein plus, Einstein multiplied, Einstein times, Einstein power
2. Q-rung orthopair fuzzy sets and Q-rung orthopair interval-valued fuzzy sets
   1. Q-rung orthopair fuzzy sets and Q-rung orthopair interval-valued fuzzy sets with interval 
      values based on the Numpy (CuPy) framework
   2. Membership matrix, non-membership matrix, score matrix, transposed matrix
   3. Q-rung orthopair fuzzy higher-order addition, subtraction, multiplication, 
      division and power operations
   4. High-order random, add elements, delete elements, remove elements, clear, sum
   5. Maximum value, minimum value, maximum value of f function, minimum value of f function
   6. Save .npz file, load .npz file, save .csv file, load .csv file
   7. Fuzzy number distribution diagram of Q-order order for Q-rung orthopair fuzzy sets and 
      Q-rung orthopair interval-valued fuzzy sets
   8. Custom function fuzzy set operation, randomly extract fuzzy numbers
   9. Q-rung orthopair fuzzy vector dot product, inner product, outer product, custom function 
      operation, Cartesian sum, Cartesian product
   10. Q-rung orthopair fuzzy high-order dot product, inner product, custom function operation, 
       Cartesian sum, Cartesian product
   11. Construct high-order Q-rung orthopair all-zero fuzzy sets, positive ideal high-order fuzzy sets, 
       negative ideal high-order fuzzy sets, and arbitrary fuzzy number high-order fuzzy sets
3. Function
   1. 8 commonly used functions: sigmf function, triangle function, Z-shaped function, trapezoidal function, 
      S-shaped function, Gaussian function, double Gaussian function, generalized Bell function
   2. Membership and non-membership function generators
4. Fuzzy measure
   1. Dirac measure (Boolean fuzzy measure)
   2. additive fuzzy measure
   3. Symmetric fuzzy measure
   4. lambda fuzzy measure
   5. Mobius representation
   6. Zeta representation
   7. vector representation
   8. Dictionary representation
   9. Fuzzy measure Hasse diagram
5. Fuzzy measure index
   1. Derivatives of set functions
   2. Shapley value
   3. Banzhaf value
   4. Shannon entropy
6. Fuzzy measure integral
   1. Choquet integral
   2. Sugeno integral
   3. Shilkret integral
7. Utils
   1. Data set normal distribution ks test
   2. The data set is randomly divided into two sets
   3. Archimedean T norm and Archimedean T co-norm

## Features to be developed：
1. Q-rung orthopair fuzzy similarity measure for fuzzy numbers, fuzzy entropy measure
2. Generalized fuzzy set distance, similarity measure
3. [ ] Adapted to GPU, using CuPy
4. [ ] Add a fuzzy framework based on PyTorch or TensorFlow, adapted for deep learning development
5. [ ] Numpy and CuPy have flaws in tensor calculations. Consider adapting PyTorch and TensorFlow.
6. [ ] Q-rung orthopair fuzzy neural network based on MohuPy
7. [ ] Adding the calculation of Q-rung orthopair hesitant fuzzy sets
