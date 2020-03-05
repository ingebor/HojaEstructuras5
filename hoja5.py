#Ingebor Ayleen Rubio Vasquez 19003
#Algoritmos y Estructura de Datos
#Hoja de trabajo No. 5

import simpy
import random
import math

capacityRAM = 100
cantProcesos = 200
numCPU= 2
interval = 10
insCPU = 6
tempOpInOut = 1
tempProcesos = []
random.seed(15)

class sistemaOp:
    def _init_(self, env):
        self.RAM = simpy.Container(env, init= capacityRAM, capacity=capacityRAM)
        sel.CPU = simpy.Resource(env, capacity=numCPU)
        
class proceso:
    def _init_(self, id, no, env, sistema_op):
        self.id=id
        self.no=no
        self.instrucciones=random.randint(1,10)
        self.memRequerida = random.randint(1,10)
        self.env = env
        self.terminated = false
        