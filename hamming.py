from bitarray import bitarray

class Hamming:

	def calc_redundant_bits(self, n):
		for i in range(n):
			if(2**i >= n+i+1):
				return i

	def calc_parity_bits(self, data, r):
		n = len(data)

		for i in range(r):
			value = 0
			for j in range(1, n+1):
				if(j&(2**i) == (2**i)):
					value = value ^ int(data[-1*j])
			data = data[:n-(2**i)] + str(value) + data[n-(2**i)+1:]
		return data	 

	def placed_redundancy_bits(self, data, r):
		j, k, n = 0, 1, len(data)
		posicion = ''

		for i in range(1, n+(r+1)):
			if(i == 2**j):
				posicion = posicion + '0'
				j += 1
			else:
				posicion = posicion + data[-1 * k]
				k += 1
		return posicion[::-1]

	def detect(self, data, r):
		n = len(data)
		resultado = 0

		for i in range(r):
			value = 0
			for j in range(1, n+1):
				if(j & (2**i) == (2**i)):
					value = value ^ int(data[-1*j])
			resultado = resultado + value*(10**i)

		return int(str(resultado), 2)
	
	def correct(self, arr, pos):
		print(f'arr to correct {arr}')
		print(f'post to correct {pos}')
		return arr[0:pos] + '1' if arr[pos] == '0' else '0' + arr[pos:]

	def correct(self, arr, pos):
		if(pos > len(arr)):
			return arr
		pos = pos - 1
		arr = list(arr)
		arr[pos] = '1' if arr[pos] == '0' else '0'
		return ''.join(arr)
