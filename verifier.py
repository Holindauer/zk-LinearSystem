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
        @notice This function will verify that the prover knows the solution to the system of equations
        without revealing the actual solution.

        @dev elipticDotProduct() is used to validate the proof. If the eliptic dot product of the proof 
        matches the constant vector b (each term multiplied represented the generator multiplied by each 
        elment) then the private solution has the property that Ax = b.

        @param It accepts the proof  and public variables A and b from the Prover class.
        (a list of eliptic curve points that are each the generator added itself the amount
        of times as the actual values)
        ''' 

        # check dimensions
        assert A.shape[0] == len(b), "A and b must have same number of rows"
        assert A.shape[1] == len(proof), "A and x must have same number of columns"

        # save num rows and cols
        num_rows = A.shape[0]

        # Convert A and b to list of ints
        A = [[int(col) for col in row] for row in A]
        b = [int(row) for row in b]

        # The the Ax must match the points in this list when represented as eliptic curve points
        elipticB : List = [multiply(G1, row) for row in b]

        # compute the dot product for each row in A with the proof
        computedElipticB : List = [self.elipticDotProduct(proof, A[row]) for row in range(num_rows)]

        # check if the computed eliptic curve points are equal to the eliptic curve points of b
        for i in range(len(computedElipticB)):
            if computedElipticB[i] != elipticB[i]:
                return False
            
        return True    
    
    def elipticDotProduct(self, proof : List, A_row : List) -> Tuple:
        '''
        @notice elipticDotProduct is a helper function for the verify method. It recieves the proof generated
        by the Prover class (containing eliptic curve points generated by multiplying the generator by the 
        private solution to the system of equations) and a single row of A (a list of scalars). Eliptic curve 
        multiplication of the curve points in the proof with the scalars in the row of A is applied. Then all
        of these points are added together using eliptic curve point addition. The result is the homomorphic 
        equivalent of dot product of the row of A and the proof in elliptic curve space.
        '''
        
        assert len(A_row) == len(proof), "row and proof must have same number of elements"
        assert [type(proof[i]) == tuple and len(proof[i]) == 2 for i in range(len(proof))], "proof must contain tuple elements of eliptic curve points"

        # elemetwise multiply row of A (scalasrs) with the eliptic curve points of the proof
        A_row_ewMult_b = [multiply(proof[i], A_row[i]) for i in range(len(proof))]

        # add first and seond element
        dot = add(A_row_ewMult_b[0], A_row_ewMult_b[1])

        # add the rest of the elements to complete the dot product
        # start at 2 because we already added the first two elements
        for (i, element) in enumerate(A_row_ewMult_b[2:]):  
            dot = add(dot, element)

        return dot



    

