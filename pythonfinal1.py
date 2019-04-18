import sys

#Estructura que guarda la forma en como se llenaria la tabla de paginas
class Structure:
	def __init__ (self, a = -1, b = -1, c = -1, d = -1, e = 0):
		self.process = a
		self.logicPage = b
		self.reference = c
		self.dirty = d
		self.clock = e
#Estructura que guarda las instrucciones recibidas por archivo
class Process:
	def __init__ (self, a, b, c, d):
	        self.process = a
	        self.di = b
	        self.dm = c
	        self.type = d


#Funcion para abrir archivo y leer parametros iniciales
def leerParametros(archivo):
	list=[]
	try:
		file=open(archivo,'r')
	except :
		print('Error al leer el archivo con el nombre', archivo)

	for process in file:
		process = process[:len(process)-1].split()
		list.append(process[0])
	return list


#Funcion para abrir y leer un archivo
def leerProceso(nombre,list):
	try:
		file=open(nombre,'r')
	except:
		print('Error al leer el archivo con el nombre', nombre)
		return -1

	for process in file:
		process=process[:len(process)-1].split(' ')
		d=0
		if process[3] == 'W':
			d=1
		list.append(Process(int(process[0]),int(process[1]),int(process[2]),d))
	file.close
	return list


#Funcion para abrir y leer un archivo con un quantum diferente de 0
def leerProcesoQuantum(nombre):
	list=[]
	try:
		file=open(nombre,'r')
	except:
		print('Error al leer el archivo con el nombre', nombre)
		return -1

	for process in file:
		process=process[:len(process)-1].split(' ')
		d=0
		if process[3] == 'W':
			d=1
		list.append(Process(int(process[0]),int(process[1]),int(process[2]),d))
	file.close
	return list


#Funcion para crear un solo archivo con los x procesos y el quantum!=0
def crearArchivo(list,num_quantum):
	cont=0
	bool=True
	archivo=[]
	while bool:
		aux=0
		for i in range(len(list)):
			if cont>=(len(list[i])):
				aux+=1
		if aux==len(list):
			break

		for j in range(len(list)):
			q_cont=cont
			while q_cont<cont+num_quantum and q_cont<len(list[j]) :
				archivo.append(list[j][q_cont])
				q_cont+=1
		cont=cont+num_quantum
	return archivo


#Funcion para definir la estructura inicial de la lista
def startList(mem_size):
	list = []
	for _ in range(mem_size):
		list.append(Structure())
	return list


##__Funciones para 'Version1' y 'Version2'__##

##Busca un proceso en la estructura y devuelve su indexicion en la estructura si la encuentra
def buscarEnEstructura(Structure,Process,direccion,pg_size):
	find=False
	i=0
	for elemento in Structure:
		if elemento.process==Process.process and elemento.logicPage==direccion//pg_size:
			find=True
			break
		i+=1
	return i,find

#Revisa si hay una pagina libre
def estructuraLlena(Structure,mem_size):
	empty=False
	index=0
	while index<mem_size and not empty:
		if Structure[index].process==-1:
			empty=True
		else:
			index+=1
	return index,empty

##Busca una pagina para ser reemplazada de acuerdo a la prioridad de referencia y dirty 
def busquedaVersion1(Structure):
	find = False
	escritura = False
	case = [(0,0),(0,1),(1,0),(1,1)]
	i=0
	while i < 4 and not find:
		index = 0
		for elemento in Structure:
			if (elemento.reference,elemento.dirty)==case[i]:
				find=True
				if elemento.dirty==1:
					escritura=True
				return index , escritura
			index+=1
		i+=1
	return index,escritura

##Restablece el bit de referencia a 0 y devuelve la estructura
def refToZero(Structure):
	for elemento in Structure:
		elemento.reference = 0
	return Structure

##Retorna el indice de la pagina con el menor valor en clock y su estado de escritura 
def busquedaVersion2(Structure):
	index = lowerClock(Structure)
	write = Structure[index].dirty or 0
	return index , write

##Busca la pagina que tenga el menor valor en clock
def lowerClock(Structure):
	j = 0
	for i in range(len(Structure)):
		if Structure[i].clock < Structure[j].clock:
			j = i
	return j
##


#Version 1................................................................................
def Version1(archivo,Estructura,debug,pg_size,mem_size):
	contIns = 1
	cont = 1
	contFails = 0
	contWrites = 0
	for process in archivo:
		index1, find1 = buscarEnEstructura(Estructura,process,process.di,pg_size)
		if find1:
			Estructura[index1] = Structure(process.process,process.di//pg_size,1,Estructura[index1].dirty or 0,cont)
		else:
			contFails+=1
			index3 , empty= estructuraLlena(Estructura,mem_size)
			if empty:
				Estructura[index3] = Structure(process.process,process.di//pg_size,1,0,cont)
			else:
				index4, escritura = busquedaVersion1(Estructura)
				if debug:
					print (cont,index4,Estructura[index4].process,Estructura[index4].logicPage,Estructura[index4].dirty)
				if escritura:
					contWrites+=1
				Estructura[index4] = Structure(process.process,process.di//pg_size,1,0,cont)


		index2,find2 = buscarEnEstructura(Estructura,process,process.dm,pg_size)
		if find2:
			Estructura[index2] = Structure(process.process,process.dm//pg_size,1,Estructura[index2].dirty or process.type,cont)
		else:
			contFails+=1
			index3 , empty= estructuraLlena(Estructura,mem_size)
			if empty:
				Estructura[index3] = Structure(process.process,process.dm//pg_size,1,process.type,cont)
			else:
				index4, escritura = busquedaVersion1(Estructura)
				if debug:
					print (cont,index4,Estructura[index4].process,Estructura[index4].logicPage,Estructura[index4].dirty)
				if escritura:
					contWrites+=1
				Estructura[index4] = Structure(process.process,process.dm//pg_size,1,process.type,cont)

		if contIns == 200:
			Estructura = refToZero(Estructura)
			contIns = 0
		contIns+=1
		cont+=1
	return contFails,contWrites,Estructura


#Version 2...........................................................................................
def Version2(archivo,Estructura,debug,pg_size,mem_size):
	contIns = 1
	cont = 1
	contFails = 0
	contWrites = 0
	for process in archivo:
		index1, find1 = buscarEnEstructura(Estructura,process,process.di,pg_size)
		if find1:
			Estructura[index1] = Structure(process.process,process.di//pg_size,1,Estructura[index1].dirty or 0,cont)
		else:
			contFails+=1
			index3 , empty= estructuraLlena(Estructura,mem_size)
			if empty:
				Estructura[index3] = Structure(process.process,process.di//pg_size,1,0,cont)
			else:
				index4, escritura = busquedaVersion2(Estructura)
				if debug:
					print (cont,index4,Estructura[index4].process,Estructura[index4].logicPage,Estructura[index4].dirty)
				if escritura:
					contWrites+=1
				Estructura[index4] = Structure(process.process,process.di//pg_size,1,0,cont)


		index2,find2 = buscarEnEstructura(Estructura,process,process.dm,pg_size)
		if find2:
			Estructura[index2] = Structure(process.process,process.dm//pg_size,1,Estructura[index2].dirty or process.type,cont)
		else:
			contFails+=1
			index3 , empty= estructuraLlena(Estructura,mem_size)
			if empty:
				Estructura[index3] = Structure(process.process,process.dm//pg_size,1,process.type,cont)
			else:
				index4, escritura = busquedaVersion2(Estructura)
				if debug:
					print (cont,index4,Estructura[index4].process,Estructura[index4].logicPage,Estructura[index4].dirty)
				if escritura:
					contWrites+=1
				Estructura[index4] = Structure(process.process,process.dm//pg_size,1,process.type,cont)

		if contIns == 200:
			Estructura = refToZero(Estructura)
			contIns = 0
		contIns+=1
		cont+=1
	return contFails, contWrites,Estructura


#-----------------------------------------------#
#	        Funcion principal		#
#-----------------------------------------------#
def main():

	Parameter = sys.argv	#parametros: filename.py, filename.txt, version # (1,2), debug (_,1)
	Parametros=leerParametros(Parameter[1])	#lee param.txt
	pg_size  	=int(Parametros[0])		# page size
	mem_size 	=int(Parametros[1])		# memory size in frames
	num_quantum =int(Parametros[2])		# quantum number
	num_process =int(Parametros[3])		# number of processes

	if num_quantum!=0:
		arr=[]
		for i in range (num_process):
			arr.append(leerProcesoQuantum(Parametros[4+i]))
		archivo=crearArchivo(arr,num_quantum)
	else:
		arr=[]
		for i in range (1,num_process+1):
			archivo=leerProceso(Parametros[3+i],arr)
	print("READING DATA")
	l=len(Parameter)

	if l==3:
		Parameter.append('0')
		if Parameter[2] == '1':
			contFails, contWrites,_ =  Version1(archivo,startList(mem_size),int(Parameter[3]),pg_size,mem_size)
			print('PAGESIZE=',pg_size,'\nNumber of Frames=',mem_size,'\nQuantum=',num_quantum,'\nNumber of processes=',num_process)
			print ('Version: ',Parameter[2],'\nPage faults: ',contFails,'\tWritings: ',contWrites)

		elif Parameter[2] == '2':
			contFails, contWrites, _ =  Version2(archivo,startList(mem_size),int(Parameter[3]),pg_size,mem_size)
			print('PAGESIZE=',pg_size,'\nNumber of Frames=',mem_size,'\nQuantum=',num_quantum,'\nNumber of processes=',num_process)
			print ('Version: ',Parameter[2],'\nPage faults: ',contFails,'\tWritings: ',contWrites)

		else:
			print ('Version Desconocida')


	elif l < 3:
		print ('Error: La estructura es la siguiente, el tercer parametro es opcional')
		print ('''Menu:
		Parametro 1 : Nombre archivo
		Parametro 2 : Version(1/2)
		Parametro 3 : Debug(1/0) ''')


	else:
		if Parameter[2] == '1':
			contFails, contWrites,_ =  Version1(archivo,startList(mem_size),int(Parameter[3]),pg_size,mem_size)
			print('PAGESIZE=',pg_size,'\nNumber of Frames=',mem_size,'\nQuantum=',num_quantum,'\nNumber of processes=',num_process)
			print ('Version: ',Parameter[2],'\nPage faults: ',contFails,'\tWritings: ',contWrites)

		elif Parameter[2] == '2':
			contFails, contWrites, _ =  Version2(archivo,startList(mem_size),int(Parameter[3]),pg_size,mem_size)
			print('PAGESIZE=',pg_size,'\nNumber of Frames=',mem_size,'\nQuantum=',num_quantum,'\nNumber of processes=',num_process)
			print ('Version: ',Parameter[2],'\nPage faults: ',contFails,'\tWritings: ',contWrites)

		else:
			print ('Version Desconocida')


main()
