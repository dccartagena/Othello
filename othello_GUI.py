
"""
Created on Wed Aug 12 15:15:24 2015

@author: Piaktipik
"""
import wx
import logica
#from time import sleep
# variables dibujo tablero
size_x = 600
size_y = 600
# variables juego
tam = 8


class Shapes(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(size_x, size_y))
        #wx.Panel = wx.Panel(self, wx.ID_ANY)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_UP, self.OnClick)
        self.Bind(wx.EVT_RIGHT_UP, self.Pasar)

        self.Centre()
        #self.Update()
        self.Show(True)
        self.negro = True;
        
        self.log = logica.logica()
    
    # dibuja el tablero inicial
    def OnPaint(self, event=0):
        self.dc = wx.PaintDC(self)
        # dibujo el tableroA
        self.dib_malla(self.dc)
        #self.board = [[0 for j in range_size] for i in range_size]

        self.dib_fichas(self.dc,self.log.tablero)
    
    # funcion evento click derecho -> pasamos la jugada al blanco
    def Pasar(self, event):
        print "Pasaste"
        self.negro = False # entregamos la jugada al blanco
        self.Jugar_PC()
        
        
    # ejecuto la jugada como PC
    def Jugar_PC(self):
        # juego

        mis_posi = []
        puntaje_r = []
        # pruebas
        for mmx in range(0,tam):
            for mmy in range(0,tam):
                res = self.simular_jugada(map(list,self.log.tablero), mmx, mmy, self.negro)
                if(res != False):
                    # almaceno posibilidades 
                    mis_posi.append([mmx,mmy])
                    evalu = self.log.evaluar_tab(res)
                    puntaje_r.append(evalu)
                    
                    #print "jugada: (" + str(mmx) +","+ str(mmy) +")"
                    #print ( "Eval: " + str(evalu))
                    #print (res)
                    
        #print ( "mis posi: " + str(mis_posi))
    
        # expandimos arbol
        
        arbolito = logica.arbol()
        arbolito.settablero(map(list,self.log.tablero))
        arbolito.setvalue()
        arbolito.setnivel(0)
        
        mat1 = self.obtener_posibles_j(arbolito.tablero, 0)
        arbolito.numhijos(len(mat1))
        global posicion3
        #v = [None]*len(mat1)
        
        for i in range(0, len(mat1)):
            arbolito.hijos[i].settablero(mat1[i])
            arbolito.hijos[i].setvalue()
            arbolito.hijos[i].setnivel(1)
        
            mat2 = self.obtener_posibles_j(arbolito.hijos[i].tablero, 1)
            arbolito.hijos[i].numhijos(len(mat2))   
            
            #Creacion del arbol
            for se in range(0, len(mat2)):
                arbolito.hijos[i].hijos[se].settablero(mat2[se])
                arbolito.hijos[i].hijos[se].setvalue()
                arbolito.hijos[i].hijos[se].setnivel(2)
            
                mat3 = self.obtener_posibles_j(arbolito.hijos[i].hijos[se].tablero, 0)
                arbolito.hijos[i].hijos[se].numhijos(len(mat3))
                
                for k in range(0, len(mat3)):
                    arbolito.hijos[i].hijos[se].hijos[k].settablero(mat3[k])
                    arbolito.hijos[i].hijos[se].hijos[k].setvalue()
                    arbolito.hijos[i].hijos[se].hijos[k].setnivel(3)
                    
                    #Exploracion del arbol
                    if k == 0:
                        arbolito.hijos[i].hijos[se].value = arbolito.hijos[i].hijos[se].hijos[k].value
                    elif arbolito.hijos[i].hijos[se].hijos[k] > arbolito.hijos[i].hijos[se].value:
                        arbolito.hijos[i].hijos[se].value = arbolito.hijos[i].hijos[se].hijos[k].value
                        
                if se == 0:
                    arbolito.hijos[i].value = arbolito.hijos[i].hijos[se].value
                elif arbolito.hijos[i].hijos[se].value < arbolito.hijos[i].value:
                    arbolito.hijos[i].value = arbolito.hijos[i].hijos[se].value
                    
            if i==0:
                posicion3 = i
                arbolito.value = arbolito.hijos[i].value
            elif arbolito.hijos[i].value > arbolito.value:
                posicion3 = i
                arbolito.value = arbolito.hijos[i].value
        
        #print posicion3
        if posicion3 <= len(mis_posi):
            mejor_h = mis_posi[posicion3]
        else:
            mejor_h = mis_posi
        
        
        # realizamos una jugada
        
        if self.negro == False:
                '''
                if(len(mis_posi)>0):
        
                    # busco dentro de las posibilidades la que mejor heuristica tiene
                    mayor_h = -64000
                    mejor_h = []
                    for n in range(0,len(mis_posi)):
                        if (puntaje_r[n] > mayor_h):
                            mejor_h = mis_posi[n]
                            mayor_h = puntaje_r[n]
                '''
                xjm = mejor_h[0]
                yjm = mejor_h[1]
                self.validar_jugada(yjm, xjm)
                self.log.tablero[yjm][xjm] = -int(self.negro)*2+1
                # le doy la jugada al oponente
                self.negro = not(self.negro)  
                
                # se analiza el estado del tablero
                self.analizar_tab()            
                
                # actulizo el frame
                self.Refresh()
        
        
    # funcion evento click up
    def OnClick(self, event):
        # obtengo la posicion de la matriz clikeada
        x = ((size_x)/(tam+2))
        y = ((size_y)/(tam+2))
        mx = (event.GetX())/x
        my = (event.GetY())/y
        
        # verifico si la posicion es valida para jugar
        if self.validar_jugada(my-1,mx-1):
            # manejo los turnos de los jugadores - pintando su respectiva ficha
            if(self.negro):
                self.log.tablero[my-1][mx-1] = -1
            else:
                self.log.tablero[my-1][mx-1] = 1   
                
            # le doy la jugada al oponente
            self.negro = not(self.negro)
            
        # imprimo la posicion jugada y luego el tablero
        #print "[" + str(mx) + " , " + str(my) + "]"
        self.most_fichas_con(self.log.tablero)
        
        contador = 0
        for x in range (0, 8):
            for y in range(0, 8):
                contador += abs(self.log.tablero[x][y])

        if contador <= 62:
        # juega la computadora
            self.Jugar_PC()
        
        #posibles_tab = logica.Ptablero
        #posibles_tab.tab = map(list,self.log.tablero)
                
        # actulizo el frame
        self.Refresh()
    
    def analizar_tab(self):
        conn = 0
        conb = 0
        for n1 in self.log.tablero:
            for n2 in n1:
                if n2 > 0:
                    conb += 1
                elif n2 < 0:
                    conn += 1
        dis = tam**2-(conn+conb)
        #print ("Estado tablero: " + " N: " + str(conn) + ", B: " + str(conb) + ", Dis: " + str(dis))
        if (dis <= 0 or conn == 0 or conb == 0):
            print "GAME OVER"
            print "GANADOR:"
            if(conn==conb):
                print "EMPATE"
            elif(conn>conb):
                print "NEGRO"
            else:
                print "BLANCO"
    
    # funcion de validacion de jugadas
    def validar_jugada(self, y, x):
        #print "jugada: (" + str(x) +","+ str(y) +")"
        # evito jugar sobre piezas
        if self.log.tablero[y][x] != 0:
            return False
            
        # capturo fichas
        jugador = (-int(self.negro)*2+1)
        hay_capturas = False
        # me permiten recorrer las direcciones
        dire = ((0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1))
        # busco en cada una de las direcciones
        for n in dire:
            #print "dir: " + str(n)
            xm=int(x)
            ym=int(y)
            # lista con las capturas realizadas
            lista_capturadas = []
            # mientras el punto sea valido seguimos buscando
            while (xm>=0 and xm<tam and ym>=0 and ym<tam):
                xm=xm+n[0]
                ym=ym+n[1]
                
                # si ym o xm salen del rango saltamos
                if (xm<0 or xm>tam-1 or ym<0 or ym>tam-1):
                    lista_capturadas = []
                    break
                #print "buscado: (" + str(xm) +","+ str(ym) +")"
                # verificamos el estado de este punto en el tablero
                # si esta vacio o (es ficha del jugador y no hay captura)
                if(self.log.tablero[ym][xm] == 0 or (self.log.tablero[ym][xm] == jugador and len(lista_capturadas) == 0)):
                    # lista con las capturas realizadas
                    lista_capturadas = []
                    break # finalizo busqueda en esta direccion
                
                if (self.log.tablero[ym][xm] == (jugador)):
                    # fichas para capturar
                    for fichas in lista_capturadas:
                        #print "ganadas: (" + str(xm) +","+ str(ym) +")"
                        self.log.tablero[fichas[1]][fichas[0]] = jugador
                        # jugada valida
                        hay_capturas = True
                    break
                lista_capturadas.append([xm,ym])
                #print "capturadas: (" + str(xm) +","+ str(ym) +")"
                
        # no hay captura, no hay jugada
        return hay_capturas
        
     # funcion de validacion de jugadas
    def simular_jugada(self, tab, x, y, player):
        # evito jugar sobre piezas
        if tab[y][x] != 0:
            return False
            
        # capturo fichas
        jugador = (-int(player)*2+1)
        hay_capturas = False
        # me permiten recorrer las direcciones
        dire = ((0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1))
        # busco en cada una de las direcciones
        for n in dire:
            xm=int(x)
            ym=int(y)
            # lista con las capturas realizadas
            lista_capturadas = []
            # mientras el punto sea valido seguimos buscando
            while (xm>=0 and xm<tam and ym>=0 and ym<tam):
                xm=xm+n[0]
                ym=ym+n[1]
                
                # si ym o xm salen del rango saltamos
                if (xm<0 or xm>tam-1 or ym<0 or ym>tam-1):
                    lista_capturadas = []
                    break
                # verificamos el estado de este punto en el tablero
                # si esta vacio o (es ficha del jugador y no hay captura)
                if(tab[ym][xm] == 0 or (tab[ym][xm] == jugador and len(lista_capturadas) == 0)):
                    lista_capturadas = []
                    break # finalizo busqueda en esta direccion
                
                if (tab[ym][xm] == (jugador)):
                    # fichas para capturar
                    for fichas in lista_capturadas:
                        tab[fichas[1]][fichas[0]] = jugador
                        # jugada valida
                        hay_capturas = True
                    break
                lista_capturadas.append([xm,ym])
                
        # no hay captura, no hay jugada
        if hay_capturas:
            # pintando su respectiva ficha
            tab[y][x] = jugador
            return tab
        else:
            return False
           
    def obtener_posibles_j(self,tablero, tipo):
        vec = []
        for mmx in range(0,tam-1):
            for mmy in range(0,tam-1):
                res = self.simular_jugada(map(list,tablero), mmx, mmy, tipo)
                if(res != False):
                    vec.append(res)
                    #print vec
        return vec
        
        
    # dibuja la rejilla del tablero
    def dib_malla(self, dc):
        x = ((size_x)/(tam+2))
        y = ((size_y)/(tam+2))
        for i in range(1,tam+2):
            dc.DrawLine(x*i, y, x*i, size_y-y)
            dc.DrawLine(x, y*i, size_x-x, y*i)

    # dibuja las fichas sobre la rejilla
    def dib_fichas(self, dc, fich):
        x = ((size_x)/(tam+2))
        y = ((size_y)/(tam+2))
        for i in range(0,tam):
            for j in range(0,tam):
                if(fich[i][j] == 1):
                    dc.SetBrush(wx.Brush('#FFFFFF'))
                    dc.DrawEllipse((x)*(j+1), (y)*(i+1), x, y)
                elif(fich[i][j]==-1):
                    dc.SetBrush(wx.Brush('#000000'))
                    dc.DrawEllipse((x)*(j+1), (y)*(i+1), x, y)
    
    
    # muestra la matriz por consola
    def most_fichas_con(self,fich):
        for i in range(0,tam):
            aux = ""
            for j in range(0,tam):
                aux = aux + str(fich[i][j]) + ", "
            #print aux
        #print '\n'
    
# llamado al clase
app = wx.App()
Shapes(None, -1, 'Shapes')
app.MainLoop()
