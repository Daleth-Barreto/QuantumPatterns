
import random
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import Sampler
from qiskit_aer import AerSimulator

import matplotlib
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
num_qubits = 3
width = 100
height = 100
num_px = width * height
#Create quantum and classical registers
qr = QuantumRegister(num_qubits, 'q')
cr = ClassicalRegister(num_qubits, 'c')

#Create a simulator instance
simulator = AerSimulator()
def create_simple_pattern_circuite(qubits, x, y):
  qc = QuantumCircuit(qubits)
  # Apply rotations based on pixel coordinates to introduce correlation
  for i in range(num_qubits):
    qc.h(i)
    qc.ry(np.sin(x * i) + np.cos(y * i), i)  # Introduce correlation
  qc.measure_all(qr,cr)
  return qc
def create_pattern_circuit(qubits, x, y, pattern_type):
    qc = QuantumCircuit(qubits)
    for i in range(num_qubits):
        qc.h(i)  # Hadamard gate for superposition

        if pattern_type == "circular":
            qc.ry(np.sin(np.sqrt(x**2 + y**2)) * i, i)
        elif pattern_type == "waves":
            qc.ry(np.sin(x + y) * i, i)
        elif pattern_type == "checkerboard":
            qc.ry((x + y) % 2 * np.pi/2, i)
        else:  # Default pattern with random rotations
            # Introduce random rotations for each qubit based on x, y
            random_rotation = random.uniform(0, 2 * np.pi)  # Random angle between 0 and 2π
            qc.ry(random_rotation, i)  # Apply random rotation to qubit 'i'
    qc.measure_all(qr,cr) # measure all in the quantum and classical registers.
    return qc
def quantum_pattern_word(qubits, x, y):
  qc = QuantumCircuit(qubits)
  for i, char in enumerate(word):
    rotation_angle = ord(char) * np.pi / 180
    # Use modulo operator to wrap the qubit index
    qc.ry(rotation_angle, i % num_qubits)
  for i in range(num_qubits):
    qc.cry(x * i + y * (num_qubits - i), i, (i + 1) % num_qubits)
  qc.measure_all(qr,cr)
  return qc
def generate_image(qubits, width, height, circuit_function, pattern_type=None):
       pixel_data = []
       for y in range(height):
           for x in range(width):
               if pattern_type:
                   qc = circuit_function(qubits, x, y, pattern_type)
               else:
                   qc = circuit_function(qubits, x, y)
               job = simulator.run(qc, shots=1)
               result = job.result()
               counts = result.get_counts()

               pixel_value = list(counts.keys())[0]
               pixel_value = pixel_value[::-1]

               r = int(pixel_value[0]) * 255
               g = int(pixel_value[1]) * 255
               b = int(pixel_value[2]) * 255

               pixel_data.append((r, g, b))
       image = np.array(pixel_data).reshape((height, width, 3))
       return image
# Generate the first image (original pattern)
image1 = generate_image(qr, width, height, create_simple_pattern_circuite)
plt.imshow(image1)
plt.title(f"Original Pattern")
plt.show()
# Generate the second image (circular pattern)
image2 = generate_image(qr, width, height, create_pattern_circuit, "circular")
plt.imshow(image2)
plt.title(f"Circular Pattern")
plt.show()
#Generate Quantum Pater Word
word = "Quantum"
image_pattern = generate_image(qr, width, height, quantum_pattern_word)
plt.imshow(image_pattern)
plt.title(f"Quantum Pattern For The Word: {word}")
plt.show()

#Print the circuits
qc_pixel = create_simple_pattern_circuite(qr, 50, 50)
qc_pattern_circular = create_pattern_circuit(qr, 50, 50, "circular")
qc_pattern_waves = create_pattern_circuit(qr, 50, 50, "waves")
qc_pattern_checkerboard = create_pattern_circuit(qr, 50, 50, "checkerboard")
qc_pattern_default = create_pattern_circuit(qr, 50, 50, "other")
qc_word = quantum_pattern_word(qr, 50, 50)


print("Circuit: create_simple_pattern_circuite")
print(qc_pixel.draw())

print("Circuit: create_pattern_circuit (circular)")
print(qc_pattern_circular.draw())

print("Circuit: create_pattern_circuit (waves)")
print(qc_pattern_waves.draw())

print("Circuit: create_pattern_circuit (checkerboard)")
print(qc_pattern_checkerboard.draw())

print("Circuit: create_pattern_circuit (default)")
print(qc_pattern_default.draw())

print("Circuit: quantum_pattern_word")
print(qc_word.draw())
