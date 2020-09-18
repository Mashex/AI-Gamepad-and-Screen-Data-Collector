import numpy as np

keys = np.array(['HX', 'HY', 'A0', 'A1', 'A2', 'A3', 'N', 'E', 'S', 'W', 'THL', 'THR', 'TL', 'TR', 'TL2', 'TR3', 'M' ,'ST', 'SL'])
outputs = {'HX': 0, 'HY': 0, 'A0': 0, 'A1': 0, 'A2': 0, 'A3': 0, 'N': 0, 'E': 0, 'S': 0, 'W': 0, 'THL': 0, 'THR': 0, 'TL': 0, 'TR': 0, 'TL2': 0, 'TR3': 0, 'M': 0, 'ST': 0, 'SL': 0}

def loop_translate(keys, outputs):
	new_a = map(outputs.get, keys)
	return new_a

print (list(loop_translate(keys, outputs)))