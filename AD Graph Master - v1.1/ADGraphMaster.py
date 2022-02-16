from pyvis.network import Network
import pandas as pd
import numpy
import sys
import os


def exportToGraph(filename, filetype):
    if filetype == "Users":
        nbcase = 12
    else :
        nbcase = 3

    file = open(filename, "r", encoding="utf-8")
    filesplited = ""
    for l in file.readlines():
        lcut = l.split('|')
        if lcut[nbcase] != "distinguishedName":
            filesplited += lcut[nbcase] + '\n'
    readandwritelines(filesplited, filetype)
    file.close()


def readandwritelines(filename, type):
    ans = "csv1,csv2,csv3,csv4,csv5,csv6,csv7,csv8,csv9,csv10,csv11,csv12,csv13,csv14\n"
    file = filename.split('\n')
    for l in file:
        l = l.strip().split(',')
        l.reverse()
        for e in l[:-1]:
            ans += str(e) + ","
        ans += l[-1] + "\n"

    filewrite = open(str(type)+".csv", "w", encoding="utf-8")
    filewrite.write(ans)
    filewrite.close()


def colorNode(net, e, title, file):
    N_DC = '#F04D4D'
    N_OU = '#70DB70'

    if file == ".\\Users.csv":
        N_CN = '#80B2FF'
    else:
        N_CN = '#DE7B52'

    if "DC=" in e:
        COLOR=N_DC
    elif "OU=" in e:
        COLOR=N_OU
    else:
        COLOR=N_CN

    net.add_node(title, size=80,  title='<p style="font-weight: bold;">'+e+'<p>'+title, color=COLOR, label=e)


def colorEdge(net, e0, e1, e2, file):
    E_DC = '#A00000'
    E_OU = '#70DB70'

    if file == ".\\Users.csv":
        E_CN = '#2839A0'
    else:
        E_CN = '#FD9F91'

    if "DC=" in e0:
        COLOR = E_DC
    elif "OU=" in e0:
        COLOR = E_OU
    else:
        COLOR = E_CN
    net.add_edge(e1, e2, width=30, color=COLOR)


def dataImplement(net, file):
    data = pd.read_csv(file)
    data = data.replace(numpy.nan, '')
    os.remove(file)

    csv1 = data['csv1']
    csv2 = data['csv2']
    csv3 = data['csv3']
    csv4 = data['csv4']
    csv5 = data['csv5']
    csv6 = data['csv6']
    csv7 = data['csv7']
    csv8 = data['csv8']
    csv9 = data['csv9']
    csv10 = data['csv10']
    csv11 = data['csv11']
    csv12 = data['csv12']
    csv13 = data['csv13']
    csv14 = data['csv14']

    edge_data = zip(csv1, csv2, csv3, csv4, csv5, csv6, csv7, csv8, csv9, csv10, csv11, csv12, csv13, csv14)

    listBranches = ['']

    for e in edge_data:
        titleFromOrigin = str(e[0])
        titleFromOriginSave = str(e[0])
        colorNode(net, e[0], titleFromOrigin, file)

        for i in range(1, len(e)):
            titleFromOrigin += ',' + str(e[i])
            titleFromOrigin = titleFromOrigin.strip(",")

            if titleFromOrigin not in listBranches:
                listBranches.append(titleFromOrigin)
                colorNode(net, e[i], titleFromOrigin, file)
                colorEdge(net, e[i], titleFromOrigin, titleFromOriginSave, file)

            titleFromOriginSave = titleFromOrigin


def HELP():
    print("   _   ___   ___               _    __  __         _           ")
    print("  /_\ |   \ / __|_ _ __ _ _ __| |_ |  \/  |__ _ __| |_ ___ _ _ ")
    print(" / _ \| |) | (_ | '_/ _` | '_ \ ' \| |\/| / _` (_-<  _/ -_) '_|")
    print("/_/ \_\___/ \___|_| \__,_| .__/_||_|_|  |_\__,_/__/\__\___|_|  ")
    print("                         |_|                                     v1.1")
    print("Arguments:\n  -u : users file (from AD Audit Master)\n  -c : computers file (from AD Audit Master)\n  -b : enable physics buttons\n  -n : name of the file (default : Carto)\n")
    print("examples :\n  python3 ADCarto.py -c DC=domain-Computers.csv -u DC=domain-Users.csv")
    print("  python3 ADCarto.py -u DC=domain-Users.csv -b -n HTMLUsers\n")
    exit()


def cartoCreation(usr, cpt, namehtml):
    net = Network(height='900px', width='100%', bgcolor='#222222', font_color='white')
    net.barnes_hut()

    if usr :
        dataImplement(net, ".\\Users.csv")
    if cpt :
        dataImplement(net, ".\\Computers.csv")

    if "-b" in sys.argv[1:]:
        net.show_buttons(filter_=['physics'])
    net.show_buttons(filter_=['edges'])

    net.show(namehtml + '.html')


if __name__ == "__main__":

    if not sys.argv[1:]:
        HELP()

    usr = cpt = False
    namehtml = "Carto"
    for arg in range(1,len(sys.argv)):
        if sys.argv[arg] == "-u":
            exportToGraph(sys.argv[arg+1], "Users")
            usr = True
        elif sys.argv[arg] == "-c":
            exportToGraph(sys.argv[arg+1], "Computers")
            cpt = True
        elif sys.argv[arg] == "-n":
            namehtml = str(sys.argv[arg+1])

        elif sys.argv[arg] == "-h":
            HELP()

    cartoCreation(usr, cpt, namehtml)
