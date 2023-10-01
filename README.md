# MohuPy(developing...)

MohuPy is a fuzzy logic and fuzzy mathematics toolkit which includes q-rung orthopair 
fuzzy sets, q-rung orthopair interval-valued fuzzy sets.
This also includes advanced uses of q-rung orthopair 
fuzzy sets and q-rung orthopair interval-valued fuzzy sets.

## Installation

Download the latest version `MohuPy-xx.zip`. Put it into your project and unzip it.
```shell
cd MohuPy-xx
pip install .
```

## Requirements

1. numpy
2. scipy
3. matplotlib
4. pandas
5. networkx

## TODO

 - [x] Regedit
 - [ ] Hesitant fuzzy sets
 - [ ] Neural network
 - [ ] Mohunum function(Q-rung orthopair fuzzy function)
 - [ ] Derivatives of mohunum function and gradients of mohuset functions 
 - [ ] Symbol mohu function
 - [ ] Adapted to GPU

## Quick Start

### 1. Construct a q-rung orthopair fuzzy number
```python
import mohupy as mp
t = mp.mohunum(3, 0.7, 0.3)
print(f'Fuzzy number: {t}')
print(f'Fuzzy type:{t.mtype}')
print(f'Score: {t.score}')
```
```
Fuzzy number: [0.7,0.3]
Fuzzy type: qrofn
Score: 0.3160 
```
A Fermatean fuzzy number with `qrung=3` and a membership degree of `0.7` and a non-membership degree of `0.3`

### 2. Randomly generate a `qrung=3`, q-rung orthopair fuzzy matrix with a shape of 3*5
```python
import mohupy as mp
t = mp.random(3, 'qrofn', 3, 5)
print(t)
```
```
[[[0.3109,0.9884] [0.123,0.2081] [0.3323,0.6285] [0.7218,0.4971]
  [0.8825,0.274]]
 [[0.0793,0.581] [0.0625,0.7799] [0.7804,0.6011] [0.544,0.1499]
  [0.522,0.0119]]
 [[0.5353,0.3237] [0.4312,0.1532] [0.0241,0.9458] [0.6488,0.5679]
  [0.2155,0.0089]]]
```

### 3. Calculate the dot product and cartesian sum of two q-rung orthopair fuzzy vectors
```python
import mohupy as mp
t1 = mp.random(3, 'qrofn', 5)
t2 = mp.random(3, 'qrofn', 5)
print(mp.dot(t1, t2))
print(mp.cartadd(t1,t2))
```
```
[0.1559,0.0686]

[[[0.9255,0.0249] [0.9454,0.0439] [0.9338,0.0801] [0.9254,0.0894]
  [0.9893,0.0094]]
 [[0.1825,0.0757] [0.6355,0.1338] [0.4779,0.2442] [0.1655,0.2725]
  [0.9465,0.0286]]
 [[0.1278,0.153] [0.6331,0.2704] [0.4726,0.4933] [0.0813,0.5505]
  [0.9462,0.0577]]
 [[0.2473,0.2306] [0.6411,0.4075] [0.4894,0.7435] [0.2387,0.8297]
  [0.947,0.0869]]
 [[0.1472,0.1701] [0.6337,0.3007] [0.4741,0.5487] [0.118,0.6122]
  [0.9463,0.0642]]]
```

### 4. Matrix multiplication of two fuzzy matrices
```python
import mohupy as mp
t1 = mp.random(3, 'qrofn', 3,5)
t2 = mp.random(3, 'qrofn', 5,4)
print(t1@t2)
```
```
[[[0.5618,0.0231] [0.5808,0.0546] [0.5612,0.01] [0.3101,0.0042]]
 [[0.4468,0.0246] [0.6463,0.0377] [0.6438,0.0743] [0.3923,0.0316]]
 [[0.5362,0.0638] [0.6451,0.094] [0.6296,0.1642] [0.3437,0.0814]]]
```

### 5. Calculate the Shapley index with a set `[0.4,0.25,0.37,0.2]` (using lambda fuzzy measure)
```python
import mohupy as mp
t = [0.4,0.25,0.37,0.2]
print(mp.indices.shapley(t, mp.lambda_meas, t))
```
```
[0.33322906 0.2013346  0.30610416 0.15933218]
```

### 6. Randomly generate 15 qrofn and ivfn and draw their distribution map

```python
import mohupy as mp
t1 = mp.random(3, 'ivfn', 15)
t2 = mp.random(3, 'qrofn', 15)
t1.plot()
t2.plot()
```

Scatter plot of t1

![img1.png](assets%2Fimg1.png)

Scatter plot of t2

![img2.png](assets%2Fimg2.png)


## Update Log
Latest update instructions: 0.1.2-10.1.2023


Update log: [Log](update.md)

## Contact

email: yibocat@yeah.net

## Functional description

[Chinese](docs/description(Chinese).md)

[English](docs/description(English).md)

## License
[MIT](LICENSE)