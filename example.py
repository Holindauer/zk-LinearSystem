from prover import Prover
from verifier import Verifier
import numpy as np



'''
Setup:      

    This example shows off the dynamic between the prover and verifier classes. The prover a person with a matrix A, 
    vector x, and vector b. Each of these with integer elements. The prover makes the claim that their x vector solves 
    the system of equations Ax = b. They want to prove this to the verifier without revealing the actual solution.

Agreed Upon Zero Knowledge Proof Protocol:

    The agreed upon protocol between the prover and the verifier roles is that the prover creates a proof using the Prover class.
    This proof is just a list of the Generator multiplied by each element in the private solution vector x. In order for this 
    proof to be valid, it must contain the property that Ax=b when A, x, b are reprepresented as eliptic curve points. The 
    Verifier class converts the elements of the public A and b into eliptic curve points. Then the Verifier class computes the
    homomorphic equivalent to Ax using these eliptic curve points. If the homomorphic equivalent of Ax matches the eliptic curve
    points of b, then the prover has proven that they know the solution to the system of equations without revealing the actual
    solution.
'''

if __name__ == "__main__":

    # consistent system known only to the prover
    A = np.array([[3, 4, 2], [2, 3, 1],[1, 2, 3]])
    x = np.array([3, 2, 2])
    b = np.array([21, 14, 13])

    # prover generates a proof that they know the solution 
    prover = Prover()
    prover.makeClaim(A, x, b)
    proof = prover.makeProof()

    # prover publicises A, b, and the proof
    prover.viewClaim() 
    print(f"Proof: {proof}\n")

    # verifier checks the public A and b 
    verifier = Verifier()
    verified = verifier.verify(proof, A, b)

    print(f"Verified: {verified}\n")
    