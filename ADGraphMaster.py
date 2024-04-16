#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pyvis.network import Network
import pandas as pd
import numpy
import sys
import os


def HELP():
    """
    Help file
    """

    print("""
    
   _   ___   ___               _    __  __         _           
  /_\ |   \ / __|_ _ __ _ _ __| |_ |  \/  |__ _ __| |_ ___ _ _ 
 / _ \| |) | (_ | '_/ _` | '_ \ ' \| |\/| / _` (_-<  _/ -_) '_|
/_/ \_\___/ \___|_| \__,_| .__/_||_|_|  |_\__,_/__/\__\___|_|  
                         |_|                                     v1.5
arguments:  
  -u : users file (from AD Audit Master)
  -c : computers file (from AD Audit Master)
  -b : enable physics buttons
  -n : name or path of the output file (default : ADGraphMasterCarto.html)
  -f : find a particular CN

examples :
  python3 ADGraphMaster.py -c examples/DC=teknex,DC=ex-Computers.csv -u examples/DC=teknex,DC=ex-Users.csv -n examples/Carto/CartoExample.html
  ./ADGraphMaster.py -u examples/DC=teknex,DC=ex-Users.csv -b -n HTMLUsers
  py ADGraphMaster.py -u examples/DC=teknex,DC=ex-Users.csv -f 'Benny Beak'
  
    """)
    exit()
    

def exportToGraph(filename, filetype):
    """
    Transform a export AD file into a restructured file
    :param filename: (str) name of the file to tranform
    :param filetype: (str) type of the file to tranforme (Users or Computers)
    """
    nbcase = -1
    file = open(filename, "r", encoding='utf-8')
    filesplited = ""
    for line in file.readlines():
        lcut = line.split('|')
        if nbcase == -1:
            for i in range(len(line)):
                if lcut[i] == "distinguishedName":
                    nbcase = i
                    break
        if lcut[nbcase] != "distinguishedName":
            filesplited += lcut[nbcase] + '\n'
    readandwritelines(filesplited, filetype)
    file.close()

    listDisabled(filename)


def listDisabled(file):
    """
    Modify the global variable globalListDisabled with Disabled Objects
    :param file: (str) name of the file to detect Disabled Objects
    """
    data = pd.read_csv(file, sep='|', encoding='utf-8')
    data = data.replace(numpy.nan, '')
    CN = data['CN']
    userEnabled = data['Enabled']

    for i in range(len(CN)):
        globalListDisabled["CN=" + CN[i]] = userEnabled[i]


def readandwritelines(filestr, type):
    """
    Write the string of the restructured file into an other file
    :param filestr: (str) string of the file to write
    :param type: (str) name of the file to create and write in
    """
    ans = "csv1,csv2,csv3,csv4,csv5,csv6,csv7,csv8,csv9,csv10\n"
    file = filestr.split('\n')
    for line in file:
        line = line.strip().split(',')
        line.reverse()
        for e in line[:-1]:
            ans += str(e) + ","
        ans += line[-1] + "\n"

    filewrite = open(str(type)+".csv", "w", encoding='utf-8')
    filewrite.write(ans)
    filewrite.close()


def colorNode(net, label, id, filetype):
    """
    Create a node
    :param net: (Network) network to use
    :param label: (str) label of the element
    :param id: (str) name of the id of the node
    :param filetype: (str) name of the file to test if the node is a user or a computer
    """
    N_DC = '#F04D4D'
    N_OU = '#70DB70'

    if filetype == os.path.join(".", "Users.csv"):
        N_CN_Enabled = '#80B2FF'
        N_CN_Disabled = '#464F71'
    else:
        N_CN_Enabled = '#DE7B52'
        N_CN_Disabled = '#9B5233'

    if "DC=" in label:
        COLOR = N_DC
    elif "OU=" in label:
        COLOR = N_OU
    elif label in globalListDisabled:
        if globalListDisabled[label]:
            COLOR = N_CN_Enabled
        else:
            COLOR = N_CN_Disabled
    else:
        COLOR = N_CN_Enabled
    net.add_node(id, size=80, title='<p style="font-weight: bold;">' +
                 label+'<p>'+id, color=COLOR, label=label)


def colorEdge(net, label, e1, e2, filetype):
    """
    Create a edge
    :param net: (Network) network to use
    :param label: (str) label of the element
    :param e1: (str) name of element 1
    :param e2: (str) name of element 2
    :param filetype: (str) name of the file to test if the edge is between users or computers
    """
    E_DC = '#A00000'
    E_OU = '#70DB70'

    if filetype == os.path.join(".", "Users.csv"):
        E_CN = '#2839A0'
    else:
        E_CN = '#FD9F91'

    if "DC=" in label:
        COLOR = E_DC
    elif "OU=" in label:
        COLOR = E_OU
    else:
        COLOR = E_CN
    net.add_edge(e1, e2, width=30, color=COLOR)


def dataImplement(net, file):
    """
    Implement data in a network from a file
    :param net: (Network) network to use
    :param file: (str) name of the csv file
    """
    data = pd.read_csv(file, encoding='utf-8')
    data = data.replace(numpy.nan, '')

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

    edge_data = zip(csv1, csv2, csv3, csv4, csv5, csv6, csv7, csv8, csv9, csv10)
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
                colorEdge(net, e[i], titleFromOrigin,
                          titleFromOriginSave, file)

            titleFromOriginSave = titleFromOrigin


def rechercheCN(net, CN, color):
    """
    Search a node id and change his color
    :param net: (Network) network to use
    :param CN: (str) common name to search
    :param color: (str) color of the CN found
    """
    listnodes = net.get_nodes()
    if CN[0:3] != "CN=":
        CN = "CN=" + CN
    for node in listnodes:
        if CN in node:
            net.get_node(node)['color'] = color
            break
    else:
        print("No CN found")
        
        
def fontSizeModification(filePath):
    """
    Modify the font size to a bigger one
    :param filePath: (str) path of the file to tranform
    """
    with open(filePath, "r", encoding='utf-8') as file:
        data = file.read()
    
    data = data.replace('"font": {"color": "white"}', '"font": {"color": "white", "size": 60}')
    
    with open(filePath, "w", encoding='utf-8') as file:
        file.write(data)
        

def cartoCreation(usr, cpt, HTMLpath):
    """
    Create a cartography
    :param usr: (boolean) implement a users file
    :param cpt: (boolean) implement a computers file
    :param HTMLpath: (str) path or name of the HTML cartography file
    """
    net = Network(height='900px', width='100%',
                  bgcolor='#222222', font_color='white')
    net.barnes_hut()
    net_usr = Network(height='900px', width='100%',
                      bgcolor='#222222', font_color='white')
    net_usr.barnes_hut()
    net_cpt = Network(height='900px', width='100%',
                      bgcolor='#222222', font_color='white')
    net_cpt.barnes_hut()

    if "-b" in sys.argv[1:]:
        net.show_buttons(filter_=['physics'])
        net_usr.show_buttons(filter_=['physics'])
        net_cpt.show_buttons(filter_=['physics'])

    if "-f" in sys.argv[1:]:
        try:
            rechercheCN(net, sys.argv[sys.argv.index("-f")+1], "white")
            rechercheCN(net_usr, sys.argv[sys.argv.index("-f") + 1], "white")
            rechercheCN(net_cpt, sys.argv[sys.argv.index("-f") + 1], "white")
        except IndexError:
            HELP()
            
    if not os.path.exists(os.path.dirname(HTMLpath)):
        os.makedirs(os.path.dirname(HTMLpath))
        
    if usr:
        dataImplement(net_usr, os.path.join(".", "Users.csv"))
        dataImplement(net, os.path.join(".", "Users.csv"))
        os.remove(os.path.join(".", "Users.csv"))
        fileUsers = os.path.splitext(HTMLpath)[0] + '_U.html'
        net_usr.show(fileUsers)
        fontSizeModification(fileUsers)
        print(fileUsers + " created")
    if cpt:
        dataImplement(net_cpt, os.path.join(".", "Computers.csv"))
        dataImplement(net, os.path.join(".", "Computers.csv"))
        os.remove(os.path.join(".", "Computers.csv"))
        fileComputers = os.path.splitext(HTMLpath)[0] + '_C.html'
        net_cpt.show(fileComputers)
        fontSizeModification(fileComputers)
        print(fileComputers + " created")
    if usr and cpt:
        fileCombined = os.path.splitext(HTMLpath)[0] + '_Full.html'
        net.show(fileCombined)
        fontSizeModification(fileCombined)
        print(fileCombined + " created")


if __name__ == "__main__":

    if not sys.argv[1:]:
        HELP()

    usr = cpt = False
    HTMLpath = os.path.join(".", "ADGraphMasterCarto.html")
    globalListDisabled = {}
    for arg in range(1, len(sys.argv)):
        if sys.argv[arg] == "-u":
            try:
                exportToGraph(sys.argv[arg+1], "Users")
            except IndexError:
                HELP()
            usr = True
        elif sys.argv[arg] == "-c":
            try:
                exportToGraph(sys.argv[arg+1], "Computers")
            except:
                HELP()
            cpt = True
        elif sys.argv[arg] == "-n":
            try:
                HTMLpath = str(sys.argv[arg+1])
                if HTMLpath[0:1] != os.path.join(".", HTMLpath):
                    HTMLpath = os.path.join(".", HTMLpath)
            except:
                HELP()

        elif sys.argv[arg] == "-h":
            HELP()

    cartoCreation(usr, cpt, HTMLpath)
