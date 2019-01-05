# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 16:15:00 2015

@author: Piaktipik
"""

class logica():
    def __init__(self):
        self.tablero=[ [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,-1,1,0,0,0],
                       [0,0,0,1,-1,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],]
                  
        self.map_heu = [[10,2, 3,  3,  3,  3, 2, 10], 
                        [2, 1, 1,  1,  1,  1, 1, 2], 
                        [3, 1, 2,  2,  2,  2, 1, 3], 
                        [3, 1, 2,  2,  2,  2, 1, 3],
                        [3, 1, 2,  2,  2,  2, 1, 3],
                        [3, 1, 2,  2,  2,  2, 1, 3],
                        [2, 1, 1,  1,  1,  1, 1, 2],
                        [10, 2, 3,  3,  3,  3, 2, 10]]

    # aplicamos la matriz heuristica para obtener el puntaje de la matriz
    def evaluar_tab(self, tab):
        valorjugada = -0
        for x in range(0, len(tab)):
            for y in range(0, len(tab)):
                valorjugada += tab[y][x]*self.map_heu[y][x]
        return valorjugada


class arbol():
    
    def __init__(self):
        self.raiz = None
        self.nivel = None
        self.tablero = None
        self.hijos = [None]
        self.value = 0
        self.length = 0
        
        self.map_heu = [[10,2, 3,  3,  3,  3, 2, 10], 
                        [2, 1, 1,  1,  1,  1, 1, 2], 
                        [3, 1, 2,  2,  2,  2, 1, 3], 
                        [3, 1, 2,  2,  2,  2, 1, 3],
                        [3, 1, 2,  2,  2,  2, 1, 3],
                        [3, 1, 2,  2,  2,  2, 1, 3],
                        [2, 1, 1,  1,  1,  1, 1, 2],
                        [10, 2, 3,  3,  3,  3, 2, 10]]
        
    def numhijos(self, num):
        self.hijos = [arbol()]*num
        
    def setraiz(self, raiz):
        self.raiz = raiz
    
    def setnivel(self, nivel):
        self.nivel = nivel
        
    def settablero(self, tablero):
        self.tablero = tablero
     
    def setvalue(self):
        self.value = self.evaluar_tab(self.tablero)
        
    # aplicamos la matriz heuristica para obtener el puntaje de la matriz
    def evaluar_tab(self, tab):
        valorjugada = -0
        for x in range(0, len(tab)):
            for y in range(0, len(tab)):
                valorjugada += tab[y][x]*self.map_heu[y][x]
        return valorjugada
                