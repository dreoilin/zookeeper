# ZooKeeper
A python program to automate lab equipment using PyVisa

## Installing
You can install ZooKeeper using standard pip install:

`pip3 install .`

in the root directory

## Usage
### Command Line
You can run ZooKeeper from the root directory using:

`python -m zookeeper [-b <backend>]`

`backend`:  specifies the PyVisa backend
						`@py` default, PyVisa-py backend
						`@sim` simulation backend

### Scripting
For the moment, you can use the VISA device classes in a scripting environment by importing the SCPI package:

```python
import SCPI
```

## SCPI
The SCPI package implements all the functionality of an SCPI instrument. You can create an instrument with a valid port, connect to it and disconnect when you are finished (this destroys the python object).

```python
import SCPI

# create an SCPI instrument
inst = SCPI.Instrument(prot=<port>, backend=<backend>)
# now connect to the device
inst.connect()
```

### Commands
You can perform SCPI commands in multiple ways. The easiest method is to use a hierarchial attribute command:

```python
# SCPI -> MEASure:VOLTage 1
inst.measure.voltage(1)
```
Any command without an argument is a query.

## Device Drivers
### Rohde and Schwarz HM4040
A high level driver for the Rohde and Schwarz power supply

### Keysight 33500B


## NOTES
- check backend version number with `python -m visa info`
