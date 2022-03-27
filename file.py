from cgi import print_arguments
from dataclasses import dataclass
import math
from operator import index
from pyexpat.errors import XML_ERROR_XML_DECL
from re import T
from typing import Tuple
import matplotlib.pyplot as plt
from numpy import percentile
import seaborn as sns
import pandas as pd
import random


# VALORES 
dataSet = [0,2,3,4,5,11,12,13,14,15,16,17,18,19,21,21,21,21,21,23,23,23,23,23,25,25,25,25,25,26,26,26,26,26,29,29,29,29,29,35,35,35,35,35,35,35,35,35,35,36,36,36,36,36,36,36,36,36,36,36,31,31,31,31,31,31,31,31,31,31,32,32,41,41,41,41,41,42,42,42,42,42,45,45,45,45,45,46,46,46,46,46,48,48,48,48,48,48,51,52,53,54,55,56,57,60]



minV = 120; maxV  = 200; n = 30
#dataSet = [random.randint(minV,maxV) for _ in range(n)]   

# si quieres valores aleatorios quitale el "#" a la linea de arriba




UsarOpcion = False     # Cambiar por "True"  sin comillas para usar esa opción 

# Si ya te dan la tabla llena estos datos 
#A = amplitud ; K = numero de clases o "filas" de la tabla; ValorMinimo = primer limite inferior

A = 14; K = 6; ValorMinimo = 120


frecueciaAbsoluta = [7,5,5,5,4,4]   # llena la frecuencia absoluta 



Percentiles = [n for n in range(1,101)]
class Stats:

    def __init__(self,UsarOpcion,dataSet = []) -> None:
        self.dataSet = dataSet
        dataSet.sort()
        self.NotificationLastInterval = False
        self.WithoutNumbers = UsarOpcion 


    def getParameters(self,A = 0 , K = 0, valorMinimo = 0,frecueciaAbsoluta = []):
        
        if self.WithoutNumbers == False:
            self.maxVal = max(self.dataSet)  # obtenemos el valor máximo 
            self.minVal = min(self.dataSet)  # obtenemos el valor mínimos

            self.R = self.maxVal - self.minVal   # obtenemos rango

            self.K = math.ceil(1+ 3.332*math.log10(len(self.dataSet)))   # obtenemos intervalo de clase y lo redondeamos 1+ 3.332 * log10(n)
            K = math.ceil(1+ 3.332*math.log10(len(self.dataSet)))
            A = self.R / self.K  # obtenemos amplitud R/K
            
            # print((math.ceil(A) * K) + min(dataSet) > (max(dataSet) + 1))


            if math.floor(A) * K + min(self.dataSet) > max(self.dataSet):     # si redondeamos hacia abajo
                self.A = math.floor(A)

            
            elif math.ceil(A) * K + min(self.dataSet) > max(self.dataSet): # ceil case
                self.A = math.ceil(A)
                

            else: 
                self.A =  math.ceil(A) 
                self.NotificationLastInterval = True
                


        else:
            self.minVal = valorMinimo
            self.A = A
            self.K = K
            valorMaximo = valorMinimo + (A * K)
            self.R = valorMaximo - valorMinimo

            lenDataSet = sum(frecueciaAbsoluta)
            
            dataSet = [n for n in range(lenDataSet)]
            self.dataSet = dataSet


    def getIntervals(self):

        print(self.dataSet)
        startingLim = self.minVal   #seteamos limite inferior
        self.intervalos = []   

        for _ in range(int(self.K)):    #creamos K itervalos 

            limInf = startingLim 
            limSup = limInf + self.A    #obtenemos limite superior sumando A a lim Inferior
            startingLim = limSup        # setemaos el nuevo limite inferior


            self.intervaloActual = f"{limInf}-{limSup}"       


            self.intervalos.append([[limInf,limSup],0])   #array con el intervalo y su frecuencia absoluta
        if self.NotificationLastInterval == True:
            lastInterval = len(self.intervalos) - 1
            self.intervalos[lastInterval][0][1] +=1

    
    def getFrequency(self):
        
        if self.WithoutNumbers == False:
            self.freqNums = {}  #diccionario con todos los numeros y sus frecuencias 
        
            # print(dataSet)
            vals = list(set(dataSet))   # eliminamos repetidos y nos quedamos con los valores 
            vals.sort()
            for val in vals: 
                self.freqNums[f"{val}"] = 0    # creamos diccionario por default frecuencia = 0


            for n in dataSet:
                self.freqNums[f"{n}"] += 1   # iteramos por los valores cada que encotramos un valor sumamos uno 

            # print(self.freqNums)


    def marcaDeClase(self):

        self.marcaDeClase =  [ (intervalos[0][0] + intervalos[0][1])/ 2 for intervalos in self.intervalos ]
        if self.NotificationLastInterval == True:
            self.marcaDeClase[len(self.marcaDeClase) - 1] = (max(dataSet) + (max(dataSet) - self.A)) / 2

        
    def analize(self,frecueciaAbsoluta = []):

        if self.WithoutNumbers == False:
            Finished = False #control vars
            iterFreq = 0 #aumenta para obtener valores del diccionario de frecuencias  self.freqNums = {}
            iterIntervals = 0 #aumenta para llegar a un nuevo intervalo  self.intervalos

            freqVals = [int(k) for k,v in self.freqNums.items()]   # obtenemos solo los numeros del diccionario self.freqNums = {}
            intervals = [interval[0] for interval in self.intervalos] # obtenemos solo los intervalos del array self.intervalos
            # print(intervals)

            while Finished == False:
                
                try:
                    currentInterval = intervals[iterIntervals]   # obtenemos el intervalo con el que trabajamos en el ciclo
                    currentFeqVal = freqVals[iterFreq]  # obtenemos el valor a comparar

                    if currentFeqVal >= currentInterval[0] and currentFeqVal < currentInterval[1]: # validation

                        freqCurrentVal = self.freqNums[f"{currentFeqVal}"]  # unavez encontrada el intervalo correcto 
                                                                            # obtenemos la frecuencia de ese numero
                        # print(currentInterval,currentFeqVal,freqCurrentVal)

                        self.intervalos[iterIntervals][1] += freqCurrentVal  # accedemos al intervalo acutal en el array   self.intervalos y le sumamos 
                                                                            # la frecuencia del número actual 

                        iterFreq += 1 # pasamos al siguiente valor 

                    else: iterIntervals += 1  # si no se encuentra en ese intervalo avanzamos 

                        
                    
                
                except: 
                    Finished = True
        
        else:

            for valor in range(len(self.intervalos)):


                self.intervalos[valor][1] = frecueciaAbsoluta[valor]

        
            
    def frecuenciaAcumalada(self):
        cache = 0
        freqAbs = [interval[1] for interval in self.intervalos]
        self.frecuenciaAcumulada = []
        for n in freqAbs:
            cache += n
            self.frecuenciaAcumulada.append(cache)


    def FrecuenciaRelativa(self):
        self.FrecuencieRelativa = []
        N = len(self.dataSet)
        for freq in [interval[1] for interval in self.intervalos]:
            val = freq / N
            self.FrecuencieRelativa.append(val)
        


    def FrecuenciaPorcentual(self):
        self.FrecuenciaPorcentual = []

        for n in self.FrecuencieRelativa:
            freq = n * 100
            self.FrecuenciaPorcentual.append(freq)


    
    def calcXF(self): #media 
        XF = []
        for n in range(len(self.marcaDeClase)):
            xfCurrentn = self.marcaDeClase[n] * self.intervalos[n][1]
            XF.append(xfCurrentn)
        
        X = sum(XF) / len(self.dataSet)
        len(self.dataSet)
        self.XF = XF
        self.X = X

    def calc2(self):  # (X - Xi)**2    (marca de clase - media) ** 2
        X_X2 = []
        for n in self.marcaDeClase:
            currentVal = (self.X - n)**2
            X_X2.append(currentVal)

        self.X_X2 = X_X2
    

            
    def calc3(self): # (X - Xi)² * f
            X_X2_F = []
            for n in range(len(self.X_X2)):
                currentVal = self.X_X2[n] * self.intervalos[n][1]

                X_X2_F.append(currentVal)

            self.X_X2_F = X_X2_F

            
    def calquartils(self):
        quartils = {}
        for q in range(1,5):
            first = (q*len(self.dataSet))/4

            if first in self.frecuenciaAcumulada:
                
                valor = self.frecuenciaAcumulada.index(first)
                quartil = self.intervalos[valor][0]

                quartils[f"{q}"] = quartil[1]  #limite superior
            else:
                for n in range(len(self.frecuenciaAcumulada)):
                    try:
                        freq1 = self.frecuenciaAcumulada[n]
                        freq2 = self.frecuenciaAcumulada[n+1]
                        if self.frecuenciaAcumulada[n] < first and first < self.frecuenciaAcumulada[n+1]:
                            intervalos = [self.frecuenciaAcumulada[n],self.frecuenciaAcumulada[n+1]]
                            
                            LimInf = self.intervalos[self.frecuenciaAcumulada.index(intervalos[1])][0][0]
                            Kn = (n*len(self.dataSet)) / 4



                            quartil =  (((Kn - intervalos[0]) / (intervalos[1] - intervalos[0]) * self.A)) + LimInf
                          
                            quartils[f"{q}"] = quartil

                            intervalos = []

                    except: pass
      
        self.quartils = quartils


    def caldecils(self):
        decils = {}
        for q in range(1,11):
            first = (q*len(self.dataSet))/10

            if first in self.frecuenciaAcumulada:
                
                valor = self.frecuenciaAcumulada.index(first)
                quartil = self.intervalos[valor][0]

                decils[f"{q}"] = quartil[1]  #limite superior
            else:
                for n in range(len(self.frecuenciaAcumulada)):
                    try:
                        freq1 = self.frecuenciaAcumulada[n]
                        freq2 = self.frecuenciaAcumulada[n+1]
                        if self.frecuenciaAcumulada[n] < first and first < self.frecuenciaAcumulada[n+1]:
                            intervalos = [self.frecuenciaAcumulada[n],self.frecuenciaAcumulada[n+1]]
                            
                            LimInf = self.intervalos[self.frecuenciaAcumulada.index(intervalos[1])][0][0]
                            Kn = (q*len(self.dataSet)) / 10



                            quartil =  (((Kn - intervalos[0]) / (intervalos[1] - intervalos[0]) * self.A)) + LimInf
                          
                            decils[f"{q}"] = quartil

                            intervalos = []

                    except: pass
        print("\n\n")


        self.decils = decils


    def createTable(self):
        Table = pd.DataFrame()
        Table["Intervalos"] = [f"{interval[0][0]}-{interval[0][1]}" for interval in self.intervalos]
        Table["Marca de Clase"] = self.marcaDeClase
        Table["Frecuencia Absoluta"] = [interval[1] for interval in self.intervalos]
        Table["Frecuencia Acumulada"] = self.frecuenciaAcumulada
        Table["Frecuencia Relativa"] = self.FrecuencieRelativa
        Table["Frecuencia Porcentual"] =  self.FrecuenciaPorcentual
        Table["X * Fi"] = self.XF
        Table["(Xi - X)²"] = self.X_X2
        Table["(Xi - X)² * f"] = self.X_X2_F

        Table= Table.append({
                              'Intervalos': "Total",
                              'Marca de Clase' : "-",
                              'Frecuencia Absoluta' : sum([interval[1] for interval in self.intervalos]) ,
                              'Frecuencia Relativa' : sum(self.FrecuencieRelativa),
                              'Frecuencia Porcentual' : sum(self.FrecuenciaPorcentual),
                              'Frecuencia Acumulada' : "-",
                              'X * Fi' : sum(self.XF),
                              '(Xi - X)²' : sum(self.X_X2),
                              '(Xi - X)² * f' : sum(self.X_X2_F)
                              
                              } , ignore_index=True)

        Table.to_csv('tablaDeFrecuencia.csv')



    def calcMedian(self):

        x = (len(self.dataSet) % 2)
        if len(self.dataSet) % 2 != 0:
            
            n2 = (len(self.dataSet) + 1) / 2
        else: n2 = len(self.dataSet) / 2



        
        for n in range(len(self.frecuenciaAcumulada)):
            try:
                freq1 = self.frecuenciaAcumulada[n]
                freq2 = self.frecuenciaAcumulada[n+1]
                if self.frecuenciaAcumulada[n] < n2 and n2 < self.frecuenciaAcumulada[n+1]:
                    intervalos = [self.frecuenciaAcumulada[n],self.frecuenciaAcumulada[n+1]]
                            
                    LimInf = self.intervalos[self.frecuenciaAcumulada.index(intervalos[1])][0][0]
                    
                    freqAbsPos = self.frecuenciaAcumulada.index(intervalos[1])


                    freqAbs = self.intervalos[freqAbsPos][1]
                    
                    median = LimInf + (((n2 - intervalos[0]) / freqAbs)) * self.A

                    self.median = median


                          

            except: pass


    def calcMode(self):
        freq =  [interval[1] for interval in self.intervalos]

        freqValModa = max(freq)
        positionModa = freq.index(freqValModa)

        limInf = self.intervalos[positionModa][0][0]

        try:freqAnterior = freq[positionModa -1]
        except: freqAnterior = 0

        try: freqPost = freq[positionModa + 1]
        except: freqPost = 0


        moda = limInf + ( (freqValModa - freqAnterior) / ( (freqValModa - freqAnterior ) + (freqValModa - freqPost) )  )*self.A
        
        self.moda = moda


    def createValueCsv(self):
        values = pd.DataFrame()
        values["Rango (R)"] = [self.R]
        values["Amplitud (A)"] = [self.A]
        values["Numero de clases (K)"] = [self.K]

        values["Varianza (S²)"] = [sum(self.X_X2_F) /len(self.dataSet)]
        values["Desviación Estándar"] = [math.sqrt(sum(self.X_X2_F) /len(self.dataSet) )]
        values["Coeficiente de variación "] =[math.sqrt(sum(self.X_X2_F) /len(self.dataSet) ) / self.X] 
        values["Media X"] =  [self.X] 
        values["Moda"] = self.moda
        values["Mediana"] = [self.median]



        values.to_csv('valores.csv',index = False)




    def printNdils(self):

        quartilsDF = pd.DataFrame()
        quartilsDF["Cuartil"] = [k for k,v in self.quartils.items()]
        quartilsDF["Valor"] = [v for k,v in self.quartils.items()]



        quartilsDF.to_csv('Quartils.csv',index = False)



        decilsDF = pd.DataFrame()
        decilsDF["Decil"] = [k for k,v in self.decils.items()]
        decilsDF["Valor"] = [v for k,v in self.decils.items()]



        decilsDF.to_csv('Decils.csv',index = False)


        percentilsDF = pd.DataFrame()
        percentilsDF["Percentil"] = [k for k,v in self.percentils.items()]
        percentilsDF["Valor"] = [v for k,v in self.percentils.items()]



        percentilsDF.to_csv('Percentils.csv',index = False)


    def calcPercentils(self,percentiles):
        percentiles.sort()
        percentils = {}
        for q in percentiles:
            first = (q*len(self.dataSet))/100

            if first in self.frecuenciaAcumulada:
                
                valor = self.frecuenciaAcumulada.index(first)
                percentil = self.intervalos[valor][0]

                percentils[f"{q}"] =    percentil[1]  #limite superior
            else:
                for n in range(len(self.frecuenciaAcumulada)):
                    try:
                        freq1 = self.frecuenciaAcumulada[n]
                        freq2 = self.frecuenciaAcumulada[n+1]
                        if self.frecuenciaAcumulada[n] < first and first < self.frecuenciaAcumulada[n+1]:
                            intervalos = [self.frecuenciaAcumulada[n],self.frecuenciaAcumulada[n+1]]
                            
                            LimInf = self.intervalos[self.frecuenciaAcumulada.index(intervalos[1])][0][0]
                            Kn = (q*len(self.dataSet)) / 100



                            percentil =  (((Kn - intervalos[0]) / (intervalos[1] - intervalos[0]) * self.A)) + LimInf
                          
                            percentils[f"{q}"] =    percentil

                            intervalos = []

                    except: pass


        self.percentils = percentils


    

    

#En caso de tener datos de la tabla llenar esto 



Stats = Stats(UsarOpcion,dataSet)
Stats.getParameters(A,K,ValorMinimo,frecueciaAbsoluta)
Stats.getIntervals()
Stats.getFrequency()
Stats.analize(frecueciaAbsoluta)
Stats.marcaDeClase()
Stats.frecuenciaAcumalada()
Stats.FrecuenciaRelativa()
Stats.FrecuenciaPorcentual()


Stats.calcXF()
Stats.calc2()
Stats.calc3()
Stats.calcMedian()
Stats.calcMode()
Stats.createTable()
Stats.createValueCsv()
Stats.calquartils()
Stats.caldecils()
Stats.calcPercentils(Percentiles)

Stats.printNdils()



