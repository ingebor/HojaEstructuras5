#Ingebor Ayleen Rubio Vasquez 19003
#Algoritmos y Estructura de Datos
#Hoja de trabajo No. 5

import simpy
import random
import math

#Variables que se iran modificando para hacer las pruebas
capacityRAM = 100
cantProcesos = 150
numCPU= 2
interval = 10
insCPU = 3
tempOpInOut = 1
tempProcesos = []
random.seed(10)

#Crear componentes de un sistema operativo
class sistemaOp:
    def __init__(self, env):
        self.RAM = simpy.Container(env, init= capacityRAM, capacity=capacityRAM)
        self.CPU = simpy.Resource(env, capacity=numCPU)
        
        
#Modelar cómo trabaja un proceso realmente
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
    #metodos par acontinuar con el comportamiento de un proceso
    def procesar(self, env, sistema_op):
        inicio = env.now
        self.createdTime = inicio
        print('%s: Creado en %d' % (self.id, inicio)) #Crear proceso
        with sistema_op.RAM.get(self.memRequerida) as getRam:
            yield getRam
            
            #Usar la RAM
            print('%s: Obtiene RAM en %d (Estado: Wait)' % (self.id, env.now))
            siguiente = 0
            while not self.terminated:
                with sistema_op.CPU.request() as req:
                    print('%s: Espera al CPU en %d (Estado: Wait)' % (self.id, env.now))
                    yield req
                    
                    #Usar el CPU
                    print('%s: Obtiene CPU en %d (Estado: Running)' % (self.id, env.now))
                    for i in range (insCPU):
                        if self.instrucciones > 0:
                            self.instrucciones -= 1
                            siguiente = random.randint (1,2)
                    yield env.timeout(1)
                    
                    #Incio de procefo de in/out
                    if siguiente == 1:
                        print ('%s: Espera operacion in/out en %d (Estado: in/out)' % (self.id, env.now))
                        yield env.timeout(tempOpInOut)
                            
                        #Fin uso de RAM
                    if self.instrucciones ==0:
                        self.terminated = True
            print('%s: Terminado en %d (Estado: Terminated)' % (self.id, env.now))
            sistema_op.RAM.put(self.memRequerida) #Regresa la RAM usada
        fin = env.now
        self.finishedTime = fin
        self.totalTime = int(self.finishedTime-self.createdTime) #tiempo que cada proceso estuvo en la computadora
        tempProcesos.insert(self.no, self.totalTime)
        
#Generador de procesos
def process_generator(env, sistema_op):
    for i in range (cantProcesos):
        tempCreacion = math.exp(1.0/interval)
        proceso('Proceso %d' % i, i, env, sistema_op)
        yield env.timeout(tempCreacion)#Tiempo que toca a cada creacion
        
#Correr programa
env = simpy.Environment()
sistema_op=sistemaOp(env)
env.process(process_generator(env, sistema_op))
env.run()

#promedio de tiempo total, desviación estándar y variaza
def promedio (s): return sum(s) * 1.0/len(s)
tempPromTot = promedio(tempProcesos)
varTempTot = list(map(lambda x: (x - tempPromTot) ** 2, tempProcesos))
desvTempTotal = math.sqrt(promedio(varTempTot))

print("El promedio de tiempo es de: ", tempPromTot, ", su desivacion estandar es de: ",desvTempTotal )
        