#!/usr/bin/env python
# -*- coding: utf-8 -*-
# LIFE'S GAME
# https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
#
try:
    # for Python2
    import Tkinter as Tk   ## notice capitalized T in Tkinter
except ImportError:
    # for Python3
    import tkinter as Tk   ## notice lowercase 't' in tkinter here
import collections
from tkinter import ttk
from tkinter import Frame
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import LabelFrame
from tkinter import Radiobutton
from tkinter import Listbox
from random import choice
from random import randint
#from PIL import ImageTk, Image
class Cell(object):
    '''A class to create a cell at grid on Conway's Game of Life'''
    alife = False # create a propety alife , initially are dead(false)
    neighbor = [] # a list neighbors from cell(X)
    #  4  5  6  =>  NW N NE
    #  3  X  7  =>  W  x E
    #  2  1  0  =>  SW S SE
    def __init__(self):
        self.initializeCell()
    def initializeCell(self):
        # Initialize cell (if false, cell dead but if True, cell live)
        # First random grid expression
        #self.alife = choice([False, True])

        # Second random grid expression
        choice = randint(1,1000)
        # Ternary expression [on_true] if [expression] else [on_false]
        self.alife = True if (choice%17) < 8 else False
        self.neighbor = [None for x in range(8)] # create a list of neighbors

class GridGL(object):
    ''' A class to create a grid to put cells from Conway's Game of Life'''
    line = 0
    row  = 0
    def __init__(self, size):
        self.size = size
        self.matrix = self.initializeGridGL()
        self.startGridGL()
        for y in range(self.size):
            for x in range(self.size):
                self.line = y
                self.row  = x
                self.setNeighbor()
    def initializeGridGL(self):
        return [[None for x in range(self.size)] for y in range(self.size)]
    def startGridGL(self):
        try:
            if self.size < 3:
                raise ValueError
        except ValueError:
            exit("The grid must be greater 3 x 3")
        else:
            for y in range(self.size):
                for x in range(self.size):
                    self.matrix[y][x] = Cell()
    def setNeighbor(self): # organize neighbors around cells
        #  4  5  6
        #  3  X  7
        #  2  1  0
        y1 = self.line
        x1 = self.row
        length = self.size - 1
        #NW cell
        linha  = ((y1 - 1) < 0 ) * length  + (( y1 - 1 ) >= 0 ) * ( y1 - 1 )
        coluna = ((x1 - 1) < 0 ) * length + (( x1 - 1 ) >= 0 ) * ( x1 - 1 )
        self.matrix[linha][coluna].neighbor[4] = self.matrix[y1][x1].alife
        #N cell
        linha  = ((y1 - 1) < 0 ) * length  + (( y1 - 1 ) >= 0 ) * ( y1 - 1 )
        coluna = x1
        self.matrix[linha][coluna].neighbor[5] = self.matrix[y1][x1].alife
        #NE cell
        linha  = ((y1 - 1) < 0 ) * length  + (( y1 - 1 ) >= 0 ) * ( y1 - 1 )
        coluna = (( x1 + 1 ) >= length) * 0 + ((x1 + 1) < length ) * (x1 + 1)
        self.matrix[linha][coluna].neighbor[6] = self.matrix[y1][x1].alife
        #E cell
        linha = y1
        coluna = (( x1 + 1 ) >= length) * 0 + ((x1 + 1) < length ) * (x1 + 1)
        self.matrix[linha][coluna].neighbor[7] = self.matrix[y1][x1].alife
        #SE cell
        linha  = (( y1 + 1 ) >= length) * 0 + ((y1 + 1) < length ) * (y1 + 1)
        coluna = (( x1 + 1 ) >= length) * 0 + ((x1 + 1) < length ) * (x1 + 1)
        self.matrix[linha][coluna].neighbor[0] = self.matrix[y1][x1].alife
        #S cell
        linha  = (( y1 + 1 ) >= length) * 0 + ((y1 + 1) < length ) * (y1 + 1)
        coluna = x1
        self.matrix[linha][coluna].neighbor[1] = self.matrix[y1][x1].alife
        #SW cell
        linha  = (( y1 + 1 ) >= length) * 0 + ((y1 + 1) < length ) * (y1 + 1)
        coluna = ((x1 - 1) < 0 ) * length + (( x1 - 1 ) >= 0 ) * ( x1 - 1 )
        self.matrix[linha][coluna].neighbor[2] = self.matrix[y1][x1].alife
        #W cell
        linha = y1
        coluna = ((x1 - 1) < 0 ) * length + (( x1 - 1 ) >= 0 ) * ( x1 - 1 )
        self.matrix[linha][coluna].neighbor[3] = self.matrix[y1][x1].alife
    def showGridGL(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.matrix[y][x].alife == True:
                    print("O", end=' ')
                else:
                    print(" ", end=' ')
            print("\t")
        x = self.liveOrDead()
    def liveOrDead(self):
        for y in range(self.size):
            for x in range(self.size):
                quantity = self.matrix[y][x].neighbor.count(True)
                if self.matrix[y][x].alife == True: # live cell
                    if quantity < 2: # Any live cell with fewer than two live neighbors dies, as if by underpopulation.
                        self.matrix[y][x].alife = False
                    elif quantity > 3: # Any live cell with more than three live neighbors dies, as if by overpopulation.
                        self.matrix[y][x].alife = False
                    else: # Any live cell with two or three live neighbors lives on to the next generation.
                        self.matrix[y][x].alife = True
                else: # Dead cell
                    if quantity == 3: # Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
                        self.matrix[y][x].alife = True
        for y in range(self.size): # organize neighbors again
            for x in range(self.size):
                self.line = y
                self.row  = x
                self.setNeighbor()
class Window(Frame):
    grade = 0
    geracao = 0
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.initUI()
        self.sizeGrid = 0
    def initUI(self):
        self.frameA = Frame(self.toplevel)
        self.frameB = Frame(self.toplevel)
        self.frameA.grid(row=0, column=0)
        self.frameB.grid(row=1, column=0)
        labelA = Label(self.frameA, text='How many columns an rows are there in your grid? (>=3):')
        labelA.grid(row=0,column=0)
        self.entryA = Entry(self.frameA)
        self.entryA.grid(row=1, column=0)
        self.buttonA = Button(self.frameA, width=10,text='Gerar tabuleiro',  command=self.initGridGL)
        self.buttonA.grid(row=2, column=0)
        self.buttonB = Button(self.frameB, width=10,text='>>>',  command=self.mainloop)
        self.buttonB.grid(row=0, column=0,columnspan=2)
        labelB = Label(self.frameB, text='Geração')
        labelB.grid(row=0,column=3,columnspan=100)
    def initGridGL(self):
        self.geracao += 1
        string = "Geração " + str(self.geracao)
        labelB = Label(self.frameB, text=string)
        labelB.grid(row=0,column=3,columnspan=100)
        self.sizeGrid = int(self.entryA.get())
        self.createGrid()
        self.showGridGL1()
#        for y in range(self.sizeGrid): # organize neighbors again
#            for x in range(self.sizeGrid):
#                #pass
#                #self.line = y
#                #self.row  = x
#                #self.setNeighbor()
#                self.buttonB = Button(self.frameB, height=1, width=1)
#                self.buttonB.grid(row=y, column=x) 
    def createGrid(self):
        self.grade = GridGL(self.sizeGrid)
    def showGridGL1(self):
        for y in range(self.sizeGrid):
            for x in range(self.sizeGrid):
                if self.grade.matrix[y][x].alife == True:
                    self.cell = Button(self.frameB, width=1, height=1,text="X",fg="green", bg="green")
                    self.cell.grid(row=y+1, column=x+3)
                else:
                    self.cell = Button(self.frameB, width=1, height=1,text=' ', fg="cyan", bg="cyan")
                    self.cell.grid(row=y+1, column=x+3)
        x = self.grade.liveOrDead()
    def mainloop(self):
        self.geracao += 1
        string = "Geração " + str(self.geracao)
        labelB = Label(self.frameB, text=string)
        labelB.grid(row=0,column=3,columnspan=100)
        self.showGridGL1()

def Main():
    tabuleiro = int(input("How many coluns and row are there your grid?(>=3): "))
    grade = GridGL(tabuleiro)
    geracao = 1
    while True:
        print ("Generation "+str(geracao))
        grade.showGridGL()
        x = input("Press 0[ENTER] to exit : ")
        if x == "0":
            break
        geracao += 1

def Main2():
    root = Tk.Tk()
    root.geometry("300x280+300+300")
    Window(root)
    root.mainloop()

if __name__ == "__main__":
    Main2()
