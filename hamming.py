# Implementación del algoritmo de Hamming

'''
 Calculamos el numero de bit redundante que hay dentro de la cadena,
 utilizando la formula de combinaciones posibles 2**i >= n + i + 1
 n = numero de bit de información
'''
def calculoBits(n):
	#ciclos
	for i in range(n):
		if(2**i >= n+i+1):
			return i

'''
 Calculo de bit de paridad
'''
def calculoParidad(data, r):
	n = len(data)

	for i in range(r):
		value = 0
		for j in range(1, n+1):
			if(j&(2**i) == (2**i)):
				value = value ^ int(data[-1*j])
		data = data[:n-(2**i)] + str(value) + data[n-(2**i)+1:]

	return data	 

'''
 Ajustamos el bit de redundancia dentro de la cadena
'''
def posRedundante(data, r):

	#Dectectamos si es impar '0' o par '1'
	j = 0
	k = 1
	n = len(data)
	posicion = ''

	for i in range(1, n+(r+1)):
		# Si la posicion es 2 insteramos 0
		if(i== 2**j):
			posicion = posicion + '0'
			j += 1
		else:
			posicion = posicion + data[-1*k]
			k += 1

	return posicion[::-1]

	'''
	 Detección de errores
	'''
def deteccion(data, r):
	n = len(data)
	resultado = 0

	for i in range(r):
		value = 0
		for j in range(1, n+1):
			if(j & (2**i) == (2**i)):
				value = value ^ int(data[-1*j])

		resultado = resultado + value*(10**i)

	return int(str(resultado), 2)







