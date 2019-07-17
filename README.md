# megapy
A python application to make the disk/raid management tool MegaCLI easier to use.

# MegaPy Usage

```
MegaPy v.1
usage: megapy.py [-h] [-enclosure] [-physical] [-vdrive] [-controller]
                 [-alarmoff] [-alarmon] [-basedir BASEDIR]

A wrapper to make MegaCLI commands moreuser friendly and easierto remember

optional arguments:
  -h, --help        show this help message and exit
  -enclosure        View the servers enclosure information
  -physical         View the servers physical drive information
  -vdrive           View the servers virtual drive information
  -controller       View the servers controller information
  -alarmoff         Turn the alarm off
  -alarmon          Turn the alarm on
  -basedir BASEDIR  Specify the base directory where MegaCLI is installed.
```


# Usage of MegaCLI class
```
>>from megapy import MegaCLI
>> mega = MegaCLI()
```
