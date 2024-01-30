from py_ecc.bn128 import G1, multiply, add
from typing import List, Tuple
import numpy as np


class Verifier:
    '''
    The Verifier class is used by the person who does not know the secret solution to the 
    system of equations to verify that the prover does indeed know the solution to the
    system of equations without revealing the actual solution.
    '''

    def __init__(self):
        pass

    def verify(self, proof : List, A : np.ndarray, b : np.ndarray) -> bool:
        '''
        This function will verify that the prover knows the solution to the system of equations
        without revealing the actual solution.

        It accepts the proof from and public variables A and b from the
        Prover class.

        The proof will be a tuple of tuples, where each tuple is a point in eliptic curve space.
        Verifications is done by check that the eliptic curve converted A and x multiplied together
        equal the eliptic curve converted b.
        ''' 

        # check dimensions
        assert A.shape[0] == b.shape[0], "A and b must have same number of rows"
        assert A.shape[1] == len(proof), "A and x must have same number of columns"

        # Convert A and b to list of ints
        A = [[int(col) for col in row] for row in A]
        b = [int(row) for row in b]

        print(A)
        print(b)

        # The the eliptic version of A must match the points in this list
        elipticB : List = [multiply(G1, row) for row in b]

        
        # compute the dot product of the rows of elipticA and proof using eliptic curve point addition/multiplication
        computedElipticB : List = []

        # dot product for each row of A with the proof
        for row in range(A.shape[0]):
        
            # compute dot product
            dot = self.elipticDotProduct(A[row], proof)

            # add to list
            computedElipticB.append(dot)


        print(computedElipticB)

        # check if the computed eliptic curve points are equal to the eliptic curve points of b
        for i in range(len(computedElipticB)):
            if computedElipticB[i] != elipticB[i]:
                return False

            
        return True    
    
    def elipticDotProduct(self, A_row : List, proof : List) -> Tuple:
        '''
        This function computes the dot product of a row of A with the 
        proof using eliptic curve point addition/multiplication

        The proof is expected to be a list of eliptic curve points

        The row is expected to be a list of scalars (ints)
        '''
        
        assert len(A_row) == len(proof), "row and proof must have same number of columns"

        # elemetwise multiply row of A (scalasrs) with the eliptic curve points of the proof
        A_row_ewMult_b = [multiply(proof[col], A_row[col]) for col in range(len(proof))]

        # add first and seond element
        dot = add(A_row_ewMult_b[0], A_row_ewMult_b[1])

        # add the rest of the elements to complete the dot product
        for (i, element) in enumerate(A_row_ewMult_b[1:]):  
            dot = add(dot, element)

        return dot



    
