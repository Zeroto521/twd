# twd

twd means Model of **t**hree-**w**ay **d**ecision

The script implements this model.

> Firstly the space structure of set pair information granule can be divided into positive granule, negative granule, different granule, which were similar and slightly different with three regions of generalized three-way decision. The three kinds of information granules in set pair information granule space were built based on certain positive degree, negative degree and different degree. Secondly, according to the given threshold, set pair information granule is divided into mutually disjointing positive region, negative region and different region.

## Prerequisites

-   `numpy`

> More details for [requirements](requirements.txt) file.

## Installation

```bash
>>> git clone https://github.com/Zeroto521/twd.git
>>> cd twd
>>> python setup.py install
```

## Examples

```python
>>> from twd import TWD
>>> model = TWD(Lambda=.6, Gamma=.15, PP=0, BP=25, NP=5, PN=10, BN=100, NN=0)
>>> model.predict(x_train, y_train, x_test)
```

> More details for [example.py](example.py) folder and [twd.py](twd.py) source code.

## License

MIT License. [@Zeroto521](https://github.com/Zeroto521)

## Reference

-   [ZHANG Chun-ying, WANG Li-ya, LI Ming-xia, LIU Bao-xiang. Model of three-way decision based on the space of set pair information granule and its application[J] Journal on Communications, 2016, 37 (Z1): 15-24.](http://www.infocomm-journal.com/txxb/CN/abstract/abstract158290.shtml)
