# megapy
A python application to make the disk/raid management tool MegaCLI easier to use.

# MegaPy Usage

```

MegaPy v.1
usage: megapy.py [-h] [--enclosure ENCL] [--physical PHYS] [--vdrive VDRIVE]
                 [--controller CONTROL]

A wrapper to make MegaCLI commands more user friendly and easier to remember

optional arguments:
  -h, --help            show this help message and exit
  --enclosure ENCL      View the servers enclosure information
  --physical PHYS       View the servers physical drive information
  --vdrive VDRIVE       View the servers virtual drive information
  --controller CONTROL  View the servers controller information

```

# Usage of MegaCLI class
```
>>from megapy import MegaCLI
>> thing = MegaCLI()
```
