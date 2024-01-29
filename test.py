from prover import Prover
import numpy as np

def require_ConsistentSystem(A : np.ndarray, x : np.ndarray, b : np.ndarray):
    '''
    test_ConsistentSystem tests whether Ax=b is a consistent system of equations.
    '''

    # check dimensions
    assert A.shape[0] == b.shape[0], "A and b must have same number of rows"
    assert A.shape[1] == x.shape[0], "A and x must have same number of columns"

    # check if Ax = b across each row
    for i in range(A.shape[0]):
        assert np.dot(A[i], x) == b[i], "System of equations is inconsistent"
    



if __name__ == "__main__":

    print("Running Tests...")

    # coefficient matrix
    A = np.array(
        [[3, 4, 2], 
         [2, 3, 1],
         [1, 2, 3]]
         )
    
    # solution vector
    x = np.array(
        [3, 2, 1]
        )
    
    # constant vector
    b = np.array(
        [19, 13, 10]
        )
    
    # test if system is consistent
    require_ConsistentSystem(A, x, b)

    # instantiate prover
    prover = Prover()

    # make claim
    prover.makeClaim(A, x, b)

    # view claim
    prover.viewClaim()

    print("Tests Passed!")