# AD Graph Master

AD Graph Master is an Active Directory mapping tool. It allows the creation of an interactive and complete mapping of an AD, using the [pyvis](https://pyvis.readthedocs.io/en/latest/) library.


## Installation

```
$ git clone https://github.com/Teknexx/ADGraphMaster.git
$ cd ADGraphMaster
$ pip install -r requirements.txt
$ cd src
```

## Usage
### Collecting Data
On a Windows Machine in the destination Active Directory.
```
PS> .\Get-Data.ps1
```

### Making cartography
This can be done in remote. 

```
   _   ___   ___               _    __  __         _
  /_\ |   \ / __|_ _ __ _ _ __| |_ |  \/  |__ _ __| |_ ___ _ _
 / _ \| |) | (_ | '_/ _` | '_ \ ' \| |\/| / _` (_-<  _/ -_) '_|
/_/ \_\___/ \___|_| \__,_| .__/_||_|_|  |_\__,_/__/\__\___|_|
                         |_|                                     v1.5
Arguments:
  -u : users file (from AD Audit Master)
  -c : computers file (from AD Audit Master)
  -b : enable physics buttons
  -n : name or path of the output file (default : ADGraphMasterCarto.html)
  -f : find a particular CN

examples :
  python3 ADGraphMaster.py -c DC=domain-Computers.csv -u DC=domain-Users.csv -n Carto/CartoExample.html
  ./ADGraphMaster.py -u DC=domain-Users.csv -b -n HTMLUsers
  py ADGraphMaster.py -u DC=domain-Users.csv -f 'Jean MICHEL'
```

