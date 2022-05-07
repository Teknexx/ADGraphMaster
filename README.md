# AD Graph Master

AD Graph Master is an Active Directory mapping tool. It works via the [Get-ADAuditData](https://github.com/azauditor/ADAudit) script of [Arizona Auditor General](https://github.com/azauditor/). AD Graph Master allows the creation of an interactive and complete mapping of an AD, using the [pyvis](https://pyvis.readthedocs.io/en/latest/) library.


## Installation

Use the package manager  to install foobar.

```
$ git clone https://github.com/Teknexx/ADGraphMaster.git
$ cd ADGraphMaster
$ pip install -r requirements.txt
```

## Usage

```
   _   ___   ___               _    __  __         _
  /_\ |   \ / __|_ _ __ _ _ __| |_ |  \/  |__ _ __| |_ ___ _ _
 / _ \| |) | (_ | '_/ _` | '_ \ ' \| |\/| / _` (_-<  _/ -_) '_|
/_/ \_\___/ \___|_| \__,_| .__/_||_|_|  |_\__,_/__/\__\___|_|
                         |_|                                     v1.4
Arguments:
  -u : users file (from AD Audit Master)
  -c : computers file (from AD Audit Master)
  -b : enable physics buttons
  -n : name or path of the output file (default : ADGraphMasterCarto.html)
  -f : find a particular CN

examples :
  python3 ADGrapMaster.py -c DC=domain-Computers.csv -u DC=domain-Users.csv
  python3 ADGrapMaster.py -u DC=domain-Users.csv -b -n HTMLUsers
  python3 ADGrapMaster.py -u DC=domain-Users.csv -f 'Jean MICHEL'
```

