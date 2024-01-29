from py_ecc.bn128 import G1, multiply, add

# Claim: x + y == 15

# Prover
secret_x = 5
secret_y = 10

# Multiply Generator by 5, 10
x = multiply(G1, 5)
y = multiply(G1, 10)

proof = (x, y, 15)

# Verifier: If the two points in eliptic curve space add up to 15G, 
# the property that x + y == 15 is verifiably true, but the actual 
# values of x, y are hidden in eliptic curve space
if multiply(G1, proof[2]) == add(proof[0], proof[1]):
    print("statement is true")
else:
    print("statement is false")


