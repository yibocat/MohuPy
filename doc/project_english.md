## Implemented Functions
1. Q-rung intuitionistic fuzzy numbers: definition, operation and special functions;
2. Q-rung interval-valued intuitionistic fuzzy numbers: definition, operation 
and special functions;
3. Q-rung dual hesitant fuzzy elements: definition, operation and special functions;
4. Fuzzy Sets: Definitions, operations and special Features;
5. Membership function generator;
6. Fuzzy integrals: only discrete Choquet integrals (numeric or single valued);
7. Configuration Tool: Fuzzy element dictionary configuration;
8. Aggregation operator: general weighted average operator and general weighted 
geometric operator for three fuzzy elements;

## Planning Function
1. Indeterminacy of the three fuzzy elements;
2. The similarity formula and correlation formula (generalized 
distance and Hausdorff distance) of the three fuzzy elements;
3. More functions of fuzzy sets (set sorting, set distance, similarity, correlation, 
comparison, intersection and union)
4. Custom fuzzy element program: need to write configuration tool code to construct 
a custom configuration dictionary program;
5. Change the underlying operation code of the fuzzy logic operation to be written 
in C or C++ language. Preliminary consideration of Cython;
6. Fuzzy Integral Related Content (Discrete Fuzzy Measures)
   1. Derivatives of Set Functions
   2. Shapley Value;
   3. Banzhaf Value;
   4. Entropy;
   5. Cardinality Index;
   6. Representation of fuzzy measures;
   7. Sugeno Integral;
   8. Use fuzzy numbers to represent numerical values in fuzzy integrals;

## Detailed description of the completed functions
1. Q-rung intuitionistic fuzzy numbers
   1. Score function, judgment empty, complement,Indeterminacy, algebraic power, 
algebraic multiple, Einstein power, Einstein multiple;
   2. Intersection operation, union operation, algebraic multiplication, 
algebraic addition, Einstein multiplication, Einstein addition;
   3. random generation, character conversion, positive ideal, negative ideal, 
0 value;
2. Q-rung interval-valued intuitionistic fuzzy numbers
   1. Score function, judgment empty, complement,Indeterminacy, algebraic power, 
algebraic multiple, Einstein power, Einstein multiple;
   2. Intersection operation, union operation, algebraic multiplication, 
algebraic addition, Einstein multiplication, Einstein addition;
   3. random generation, character conversion, positive ideal, negative ideal, 
0 value;
3. Q-rung dual hesitant fuzzy elements
   1. Score function, judgment empty, complement,Indeterminacy, algebraic power, 
algebraic multiple, Einstein power, Einstein multiple;
   2. Intersection operation, union operation, algebraic multiplication, 
algebraic addition, Einstein multiplication, Einstein addition;
   3. random generation, character conversion, positive ideal, negative ideal, 
0 value;
4. Fuzzy element mathematical operation
   1. Dual hesitant fuzzy element normalization (continuous normalization of 
parameter values)
   2. Q-rung dual hesitant fuzzy element generalized distance formula: 
This formula needs to be further improved into a distance formula corresponding 
to all fuzzy elements;
5. Membership function generator 
   (including 8 basic membership functions and custom functions)
   1. Q-rung intuitionistic fuzzy membership function generator;
   2. Q-rung interval-valued intuitionistic fuzzy membership function generator;
   3. Q-rung dual hesitant fuzzy membership function generator;
6. Fuzzy sets (high-dimensional fuzzy sets, based on Numpy)
   1. Fuzzy set class;
   2. Set dictionary, collection, set shape, number of set elements, list of set 
elements, empty judgment, matrix, set score
   3. Append, delete by value, delete by index, set element custom function, random 
fuzzy set, random fuzzy set of any dimension;
   4. Set remodeling, set expansion, positive ideal set, negative ideal set, 
zero value set, set clear;
   5. Maximum value, minimum value, maximum value of custom function, minimum 
value of custom function, set sum;
   6. Save fuzzy set (including fuzzy information), read fuzzy set (including 
fuzzy information), save fuzzy matrix, read fuzzy matrix;
7. Fuzzy Set Math Operations
   1. Dot product, set element addition, set element multiplication, set element 
union, set element intersection;
   2. Set element custom collection functions, Cartesian sum, Cartesian product;
8. Fuzzy Set Tool
   1. Fuzzy set functions `fuzzys` (similar to `numpy.array`);
   2. Transformation set function `asfuzzyset` (similar to `numpy.asarray`);
   3. Strict equality judgment, (weak equality) similar judgment;
9. Fuzzy Integral
   1. lambda-fuzzy measure;
   2. lambda anonymous function;
   3. Discrete Choquet integral;
10. Fuzzy Element Configuration Dictionary
    1. Configure dictionary;
    2. Configure dictionary save function, configure dictionary load function;
    3. Manually configure dictionary updates;
11. Aggregation operator
    1. General weighted average aggregation operators (Q-rung intuitionistic 
fuzzy, interval-valued fuzzy and dual hesitant fuzzy);
    2. General weighted geometric aggregation operators (Q-rung intuitionistic 
fuzzy, interval-valued fuzzy and dual hesitant fuzzy)
12. Toolkit (collections using `numpy.ndarray`)
    1. Dataset plot analysis method;
    2. Data set normal distribution ks test;
    3. The data set is randomly divided into two sets;