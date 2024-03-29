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
    

def require_InconsistentSystem(A : np.ndarray, x : np.ndarray, b : np.ndarray):
    '''
    test_InconsistentSystem is a helper function that ensures Ax=b is an inconsistent system of equations.
    '''

    # check dimensions
    assert A.shape[0] == b.shape[0], "A and b must have same number of rows"
    assert A.shape[1] == x.shape[0], "A and x must have same number of columns"

    # check if Ax = b across each row
    for i in range(A.shape[0]):
        assert np.dot(A[i], x) != b[i], "System of equations is consistent"


def test_makeProof(A : np.ndarray, x : np.ndarray, b : np.ndarray):
    '''
    This test makes sure that the makeProof method of the prover works as expected.

    The makeProof method should return a list of eliptic curve points that are the 
    each the generator multiplied by the class's private solution to the system of
    equations.
    '''

    # instantiate prover
    prover = Prover()

    # make claim
    prover.makeClaim(A, x, b)

    # make proof
    proof = prover.makeProof()

    proofCheck = [multiply(G1, row) for row in x]

    # check if proof is correct
    for i in range(len(proof)):
        assert proof[i] == proofCheck[i], "Proof is invalid"



def test_ElipticDotProduct(A : np.ndarray, x : np.ndarray, b : np.ndarray):
    '''
    This test makes sure that the eliptic dot product method of the verifier works as expected.
    '''

    # instantiate prover and verifier
    prover, verifier = Prover(), Verifier()

    # make claim and proof
    prover.makeClaim(A, x, b)
    proof = prover.makeProof()

    # seperate row 1 of A 
    A_row1 = A[0]

    # normal dot product
    normalDot = np.dot(A_row1, x).item()

    # multiply noremal dot product by generator
    normalDot_G = multiply(G1, normalDot)
    
    # use eliptic dot product
    elipticDot = verifier.elipticDotProduct(proof, A_row1)

    assert elipticDot == normalDot_G, "Eliptic dot product is invalid"


def test_ValidProof(A : np.ndarray, x : np.ndarray, b : np.ndarray):
    '''
    test_ValidProof tests the process of commiting a consistent private solution to a system of equations
    and then verifying that the prover knows the solution to the system of equations without
    revealing the actual solution using the Verifier class.

    Ax=b must be a consistent system of equations for this test to pass.
    '''

    # ensure system is consistent
    require_ConsistentSystem(A, x, b)

    # instantiate prover and verifier
    prover, verifier = Prover(), Verifier()

    # make claim
    prover.makeClaim(A, x, b)

    # make proof
    proof = prover.makeProof()

    # verify proof
    verified = verifier.verify(proof, A, b)
    assert verified, "Proof is invalid, but should be valid"

def test_InvalidProof(A : np.ndarray, x : np.ndarray, b : np.ndarray):
    '''
    test_InvalidProof tests the process of commiting an inconsistent private solution to a system of equations
    and then verifying that the prover knows the solution to the system of equations without
    revealing the actual solution using the Verifier class.
    '''

    # ensure system is consistent
    require_InconsistentSystem(A, x, b)

    # instantiate prover and verifier
    prover, verifier = Prover(), Verifier()

    # make claim
    prover.makeClaim(A, x, b)

    # make proof
    proof = prover.makeProof()

    # verify proof
    verified = verifier.verify(proof, A, b)
    assert not verified, "Proof is valid, but should be invalid"



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
        [3, 2, 2]
        )
    
    # constant vector
    b_consistent = np.array(
        [21, 14, 13]
        )
    
    # test that prover/verifier methods work as expected
    test_makeProof(A_consistent, x_consistent, b_consistent)
    test_ElipticDotProduct(A_consistent, x_consistent, b_consistent)

    #test that prover/verifier dynamic works for consistent systems
    require_ConsistentSystem(A_consistent, x_consistent, b_consistent)
    test_ValidProof(A_consistent, x_consistent, b_consistent)



    # coefficient matrix
    A_inconsistent = np.array(
        [[3, 4, 2], 
         [2, 3, 1],
         [1, 2, 3]]
         )
    
    # solution vector
    x_inconsistent = np.array(
        [1, 1, 2]
        )
    
    # constant vector
    b_inconsistent = np.array(
        [21, 14, 13]
        )

    #test that prover/verifier dynamic works for inconsistent systems
    require_InconsistentSystem(A_inconsistent, x_inconsistent, b_inconsistent)
    test_InvalidProof(A_inconsistent, x_inconsistent, b_inconsistent)

    print("Tests Passed!")