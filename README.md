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
 - [x] Q-rung orthopair hesitant fuzzy sets
 - [x] Add more Archimedean norm operations and register (Einstein, Frank, Hamacher)
 - [ ] Neural network
 - [ ] Fuzzy function
 - [ ] Derivatives of fuzznum function and gradients of mohuset functions
 - [ ] Integrate the operations of fuzzy numbers and fuzzy sets into computational graph models

## Quick Start

### 1. Construct a q-rung orthopair fuzzy number

```python
import mohupy as mp

t = mp.fuzznum(3, 0.7, 0.3)
print(f'Fuzzy number: {t}')
print(f'Fuzzy type:{t.mtype}')
print(f'Score: {t.score}')
```
```
Fuzzy number: <0.7,0.3>
Fuzzy type: qrofn
Score: 0.3160 
```
A Fermatean fuzzy number with `qrung=3` and a membership degree of `0.7` and a non-membership degree of `0.3`

### 2. Randomly generate a `qrung=3`, q-rung orthopair fuzzy matrix with a shape of 3*5
```python
import mohupy as mp
t = mp.random.rand(3, 'qrofn', 3, 5)
print(t)
```
```
[[<0.9231,0.3439> <0.7568,0.0039> <0.4517,0.0026> <0.5421,0.4783>
  <0.277,0.5086>]
 [<0.9031,0.595> <0.4604,0.8352> <0.1529,0.3904> <0.1572,0.3834>
  <0.2359,0.4272>]
 [<0.476,0.7841> <0.17,0.6308> <0.3336,0.1038> <0.5024,0.1449>
  <0.6342,0.4409>]]
```

### 3. Calculate the dot product and cartesian sum of two q-rung orthopair fuzzy vectors
```python
import mohupy as mp
t1 = mp.random.rand(3, 'qrofn', 5)
t2 = mp.random.rand(3, 'qrofn', 5)
print(mp.dot(t1, t2))
print(mp.cartadd(t1,t2))
```
```
<0.9235,0.0175>

[[<0.4802,0.0492> <0.8261,0.3321> <0.9261,0.264> <0.5774,0.2483>
  <0.9767,0.1092>]
 [<0.7632,0.0107> <0.8994,0.0723> <0.9552,0.0574> <0.7914,0.054>
  <0.9856,0.0238>]
 [<0.9328,0.0143> <0.9682,0.0963> <0.9853,0.0765> <0.9394,0.072>
  <0.9952,0.0317>]
 [<0.8182,0.0166> <0.9198,0.1124> <0.9638,0.0893> <0.8384,0.084>
  <0.9883,0.037>]
 [<0.6558,0.0186> <0.8653,0.1256> <0.9412,0.0998> <0.7035,0.0939>
  <0.9813,0.0413>]]
```

### 4. Matrix multiplication of two fuzzy matrices
```python
import mohupy as mp
t1 = mp.random.rand(3, 'qrofn', 3,5)
t2 = mp.random.rand(3, 'qrofn', 5,4)
print(t1@t2)
```
```
[[<0.7138,0.1048> <0.535,0.16> <0.5321,0.3022> <0.5155,0.1704>]
 [<0.3536,0.0401> <0.4134,0.1281> <0.3376,0.0712> <0.5114,0.1001>]
 [<0.4219,0.0519> <0.5131,0.0532> <0.2228,0.033> <0.1698,0.0369>]]
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
t1 = mp.random.rand(3, 'ivfn', 15)
t2 = mp.random.rand(3, 'qrofn', 15)
mp.plot(t1)
mp.plot(t2)
```

Scatter plot of t1

![img2.png](assets%2Fimg2.png)

Scatter plot of t2

![img1.png](assets%2Fimg1.png)


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