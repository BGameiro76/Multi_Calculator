#!/usr/bin/env python3

"""
This code is under Apache License 2.0
Written by B_Gameiro (Bernardo Bernardino Gameiro)
More in 
    SoloLearn: https://www.sololearn.com/Profile/8198571
    GitHub: https://github.com/BGameiro76
    Repl.it: https://repl.it/@B_Gameiro

GUI para as atividades laboratoriais de Física do secundário em Python 3 e Tkinter
"""

#==========
# imports
#==========
import tkinter as tk
from tkinter import ttk, Menu
from tkinter import messagebox as msg
from Data.AtividadesClasses import *
import Data.AtividadesClasses

#==========
# variables, lists, dictionairies, constants
#==========
title =  "Atividades Laboratoriais do Secundário"
maxTries = 20
pad = 4
triesObjDict = {}

#==========
# define window
#==========
# creating instance of main window
mainWin = tk.Tk()
# Title of the window
mainWin.title(title)
# size
#mainWin.geometry('550x450')

#==========
# version
#==========
verGUI = ""
verPDF = ""
verGeral = "0.G%s.A%s.P%s" % (verGUI, verAtvLab, verPDF)

#==========
# toplevel and other windows
#==========
#insert here different windows

#==========
# functions
#==========
def _exitWin():
    close = msg.askyesnocancel("AVISO: Está a fechar a janela", "Tem a certeza que deseja fechar %s?\nA informação será perdida." % (title))
    return close

def updateCurrent(event=None):
    currentTrySP.config(to=noTries.get())
    if noTries.get() == 1: currentTryNo.set(1) # Needed to set spinbox value = 1
    triesObjDict.clear() # Needed to empty the dictionairy before being used
    for no in range(1, noTries.get()+1):
        triesObjDict["Try"+str(no)] = cls2()

def updateTryChange(event=None):#nada feito
    pass

#==========
# structure
#==========
# main container/window level
mainContainer = ttk.LabelFrame(mainWin, text="Escolha a disciplina:") # main container
mainContainer.grid(padx=pad, pady=pad)
tabControl0 = ttk.Notebook(mainContainer) # main notebook inside container

#==========
# tests
#==========
def vars():
    print("global", globals())
    print("local", locals())

testBut = ttk.Button(mainWin, text="Test", command=vars)
testBut.grid()



# discipline level
for cls0 in LaboratoryActivities.__subclasses__(): # create tabs for notebook 0 and a container inside each tab
    tabLabel = str(cls0.specialAttribute)
    tab = ttk.Frame(tabControl0)
    tabControl0.add(tab, text=tabLabel)
    container = ttk.LabelFrame(tab, text="Escolha o ano:")
    container.grid(padx=pad, pady=pad)
    tabControl1 = ttk.Notebook(container)

    # year level
    for cls1 in cls0.__subclasses__(): # create tabs for notebook 1 and a container inside each tab
        tabLabel = str(cls1.specialAttribute)
        tab = ttk.Frame(tabControl1)
        tabControl1.add(tab, text=tabLabel)
        container = ttk.LabelFrame(tab, text="Escolha a atividade laboratorial:")
        container.grid(padx=pad, pady=pad)
        tabControl2 = ttk.Notebook(container)
        
        # activity level
        for cls2 in cls1.__subclasses__(): # create tabs for notebook 2 and a container inside each tab
            tabLabel = str(cls2.specialAttribute)
            tab = ttk.Frame(tabControl2)
            tabControl2.add(tab, text=tabLabel)
            container = ttk.LabelFrame(tab, text=(cls0.specialAttribute, cls1.specialAttribute, cls2.specialAttribute))
            container.grid(padx=pad, pady=pad)
            ttk.Label(container, text=cls2.name).grid(column=0, row=0, sticky="W")

            # Data&results level -> containers
            containerVal = ttk.LabelFrame(container, text="Dados")
            containerVal.grid(column=0, row=1, sticky="W", padx=pad, pady=pad)
            noActivities = ttk.LabelFrame(containerVal, text="Número de repetições")
            noActivities.grid(column=0, row=0, padx=pad, pady=pad)
            currentVal = ttk.LabelFrame(containerVal, text="Repetição atual")
            currentVal.grid(column=0, row=1, sticky="W", padx=pad, pady=pad)
            allVal = ttk.LabelFrame(containerVal, text="Repetições")
            allVal.grid(column=0, row=2, sticky="W", padx=pad, pady=pad)

            # Data&results level -> Number of data inserts
            ttk.Label(noActivities, text="Quantas repetições da atividade laboratorial vai realizar?").grid(column=0, row=0, sticky="W", padx=pad, pady=pad)
            noTries = tk.IntVar()
            noTriesSP = tk.Spinbox(noActivities, from_=1, to=maxTries, textvariable=noTries, state="readonly", width=3, command=updateCurrent)
            noTriesSP.grid(column=1, row=0, padx=pad, pady=pad)
            noTries.set(0)     # Needed to set spinbox value = 0 (No tries initially)
            ttk.Label(noActivities, text="Qual a repetição que quer inserir/alterar?").grid(column=0, row=1, sticky="W", padx=pad, pady=pad)
            currentTryNo = tk.IntVar()
            currentTrySP = tk.Spinbox(noActivities, from_=1, to=1, textvariable=currentTryNo, state="readonly", width=3, command=updateTryChange)
            currentTrySP.grid(column=1, row=1, padx=pad, pady=pad)
            currentTryNo.set(0)     # Needed to set spinbox value = 0 (No tries initially)

            # Data&results level -> Current data insert
            # need to associate the results with a try (object)
            for val in cls2.PhysicalQuantitiesVar:
                idx = list(cls2.PhysicalQuantitiesVar).index(val)
                ttk.Label(currentVal, text=cls2.PhysicalQuantitiesExpDic[val]+":").grid(column=0, row=idx, sticky="W", padx=pad, pady=pad)
                cls2.PhysicalQuantitiesValuesDic[val] = tk.DoubleVar()
                valueBox = ttk.Entry(currentVal, width=10, textvariable=cls2.PhysicalQuantitiesValuesDic[val], justify="right")
                valueBox.grid(column=1, row=idx, sticky="E", padx=pad, pady=pad)
                valueUnit = ttk.Combobox(currentVal, width=5, text=cls2.PhysicalQuantitiesUnitsDic[val], state="readonly")
                valueUnit['values'] = list(cls2.PhysicalQuantitiesUnitsDic[val])
                valueUnit.grid(column=2, row=idx, padx=pad, pady=pad)

            # Data&results level -> All data inserts and average
            # First they have to be associated with each try

            # Creation of data results
            # Average of each data in order to calculate the average result

            # Results -> containers
            containerAns = ttk.LabelFrame(container, text="Resultados")
            containerAns.grid(column=1, row=1, sticky="W", padx=pad, pady=pad)

            # Results -> All answers being the last the average
            for ans in cls2.AnsVar:
                idx = list(cls2.AnsVar).index(ans)
                ttk.Label(containerAns, text=cls2.AnsExpDic[ans]+":").grid(column=0, row=idx, sticky="W", padx=pad, pady=pad)
      
        tabControl2.grid(padx=pad, pady=pad) # show notebook 2
    tabControl1.grid(padx=pad, pady=pad) # show notebook 1
tabControl0.grid(padx=pad, pady=pad) # show notebook 0

#======================
# menu bar
#======================
# Creating a Menu Bar
menuBar = Menu(mainWin)
mainWin.config(menu=menuBar)

# Add menu items
# File menu
file_menu = Menu(menuBar, tearoff=0)
file_menu.add_command(label="Novo")
file_menu.add_separator()
file_menu.add_command(label="Versão")
file_menu.add_separator()
file_menu.add_command(label="Sair", command=_exitWin)
menuBar.add_cascade(label="Ficheiro", menu=file_menu)
edit_menu = Menu(menuBar, tearoff=0)
edit_menu.add_command(label="Procurar atualização")
edit_menu.add_separator()
edit_menu.add_command(label="Alterar atividades laboratoriais")
menuBar.add_cascade(label="Editar", menu=edit_menu)
help_menu = Menu(menuBar, tearoff=0)
help_menu.add_command(label="Informação")
help_menu.add_separator()
help_menu.add_command(label="Ajuda")
menuBar.add_cascade(label="Ajuda", menu=help_menu)
donate_menu = Menu(menuBar, tearoff=0)
donate_menu.add_command(label="Donativos")
donate_menu.add_separator()
donate_menu.add_command(label="Sugestões")
menuBar.add_cascade(label="Contribuir", menu=donate_menu)

#======================
# Start GUI
#======================
mainWin.mainloop()