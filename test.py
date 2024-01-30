from prover import Prover
from verifier import Verifier
import numpy as np
from typing import List
from py_ecc.bn128 import G1, multiply, add

def require_ConsistentSystem(A : np.ndarray, x : np.ndarray, b : np.ndarray):
    '''
    test_ConsistentSystem is a helper function that tests whether Ax=b is a consistent system of equations.
    '''

    # check dimensions
    assert A.shape[0] == b.shape[0], "A and b must have same number of rows"
    assert A.shape[1] == x.shape[0], "A and x must have same number of columns"

    # check if Ax = b across each row
    for i in range(A.shape[0]):
        assert np.dot(A[i], x) == b[i], "System of equations is inconsistent"
    

def test_makeProof():
    '''
    This test makes sure that the makeProof method of the prover works as expected.

    The makeProof method should return a list of eliptic curve points that are the 
    each the generator multiplied by the class's private solution to the system of
    equations.
    '''

    A = np.array([[3, 4, 2],[2, 3, 1],[1, 2, 3]])
    x = np.array([3, 2, 1])    
    b = np.array([19, 13, 10])


    # instantiate prover
    prover = Prover()

    # make claim
    prover.makeClaim(A, x, b)

    # make proof
    proof = prover.makeProof()

    proofCheck = [multiply(G1, 3), multiply(G1, 2), multiply(G1, 1)]

    # check if proof is correct
    for i in range(len(proof)):
        assert proof[i] == proofCheck[i], "Proof is invalid"



# def test_ElipticDotProduct():
#     '''
#     This test makes sure that the eliptic dot product method of the verifier works as expected.
#     '''

#     # instantiate verifier
#     verifier = Verifier()

#     vector_1 : List = [5, 6, 2]
#     vector_2 : List = [6, 7, 5]
#     integer_dot : int = 0

#     for i in range(3):
#         integer_dot += vector_1[i] * vector_2[i]

#     # generator multiplied by the dot
#     elipticDot_fromIntegerDot = multiply(G1, integer_dot)

#     # eliptic dot product accepts a list of eliptic curve points (the proof)
#     # and a list of integer scalars (the rows of A). We will pass in a list 
#     # of eliptic curve points where each term is the generator multiplied by
#     # a term in vector 1
#     proof : List = [multiply(G1, element) for element in vector_1] 

#     elipticDot_fromVerifier = verifier.elipticDotProduct(vector_2, proof)
    
#     print(elipticDot_fromVerifier)


#     print(integer_dot)
#     print(elipticDot_fromIntegerDot)



# def test_ValidProof(A : np.ndarray, x : np.ndarray, b : np.ndarray):
#     '''
#     Test valid proof tests the process of commiting a private solution to a system of equations
#     and then verifying that the prover knows the solution to the system of equations without
#     revealing the actual solution using the Verifier class.
#     '''

#     # test if system is consistent
#     require_ConsistentSystem(A, x, b)

#     # instantiate prover and verifier
#     prover = Prover()
#     verifier = Verifier()

#     # make claim
#     prover.makeClaim(A, x, b)

#     # view claim
#     prover.viewClaim()

#     # make proof
#     proof = prover.makeProof()

#     # verify proof
#     verified = verifier.verify(proof, A, b)
#     assert verified, "Proof is invalid"



if __name__ == "__main__":

    print("Running Tests...")

    # coefficient matrix
    A_consistent = np.array(
        [[3, 4, 2], 
         [2, 3, 1],
         [1, 2, 3]]
         )
    
    # solution vector
    x_consistent = np.array(
        [3, 2, 1]
        )
    
    # constant vector
    b_consistent = np.array(
        [19, 13, 10]
        )
    
    require_ConsistentSystem(A_consistent, x_consistent, b_consistent)

    test_makeProof()


    # test_ElipticDotProduct()

    # test_ValidProof(A_consistent, x_consistent, b_consistent)

    
    print("Tests Passed!")