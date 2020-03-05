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
    def __init__(self, env):
        self.RAM = simpy.Container(env, init= capacityRAM, capacity=capacityRAM)
        self.CPU = simpy.Resource(env, capacity=numCPU)
        
class proceso:
    def __init__(self, id, no, env, sistema_op):
        self.id=id
        self.no=no
        self.instrucciones=random.randint(1,10)
        self.memRequerida = random.randint(1,10)
        self.env = env
        self.terminated = False
        self.sistema_op = sistema_op
        self.createdTime = 0
        self.finishedTime = 0
        self.totalTime = 0
        self.proceso = env.process(self.procesar(env, sistema_op))
        
    def procesar(self, env, sistema_op):
        inicio = env.now
        self.createdTime = inicio
        print('%s: Creado en %d' % (self.id, inicio))
        with sistema_op.RAM.get(self.memRequerida) as getRam:
            yield getRam
            
            print('%s: Obtiene RAM en %d (Estado: Wait)' % (self.id, env.now))
            siguiente = 0
            while not self.terminated:
                with sistema_op.CPU.request() as req:
                    print('%s: Espera al CPU en %d (Estado: Wait)' % (self.id, env.now))
                    yield req
                    
                    print('%s: Obtiene CPU en %d (Estado: Running)' % (self.id, env.now))
                    for i in range (insCPU):
                        if self.instrucciones > 0:
                            self.instrucciones -= 1
                            siguiente = random.randint (1,2)
                    yield env.timeout(1)
                    
                    if siguiente == 1:
                        print ('%s: Espera operacion in/out en %d (Estado: in/out)' % (self.id, env.now))
                        yield env.timeout(tempOpInOut)
                        
                    if self.instrucciones ==0:
                        self.terminated = True
            print('%s: Terminado en %d (Estado: Terminated)' % (self.id, env.now))
            sistema_op.RAM.put(self.memRequerida)
        fin = env.now
        self.finishedTime = fin
        self.totalTime = int(self.finishedTime-self.createdTime)
        tempProcesos.insert(self.no, self.totalTime)
        
def process_generator(env, sistema_op):
    for i in range (cantProcesos):
        tempCreacion = math.exp(1.0/interval)
        proceso('Proceso %d' % i, i, env, sistema_op)
        yield env.timeout(tempCreacion)
        
env = simpy.Environment()
sistema_op=sistemaOp(env)
env.process(process_generator(env, sistema_op))
env.run()

def promedio (s): return sum(s) * 1.0/len(s)
tempPromTot = promedio(tempProcesos)
varTempTot = map(lambda x: (x - tempPromTot) ** 2, tempProcesos)
desvTempTotal = math.sqrt(promedio(varTempTot))

print("El promedio de tiempo es de: ", tempPromTot, ", su desivacion estandar es de: ",desvTempTotal )
        