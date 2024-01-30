from py_ecc.bn128 import G1, multiply, add
from typing import List, Tuple
import numpy as np

class Prover:
    '''
    Prover is where the person who knows the secret solution to the system of equations commits 
    their solutions. This solution is stored as a private variable, and the public variables are 
    the matrix A and vector b. When a proof is requested, the prover will use elliptic curve 
    cryptography to prove that they know the solution to the system of equations without revealing 
    the actual solution.

    Verification will be handled in a seperate class.
    '''

    def __init__(self):

        # public setup to Ax = b
        self.A_public = None
        self.b_public = None

        # private solution
        self.__x_private = None


    def makeClaim(self, A : np.ndarray, x : np.ndarray, b : np.ndarray) -> None:
        '''
        makeClaim is where the prover makes the claim that they know a vector x
        that solves the system of equations Ax = b. 
        '''

        assert A.shape[0] == b.shape[0], "A and b must have same number of rows"
        assert A.shape[1] == x.shape[0], "A and x must have same number of columns"

        # set class variables
        self.A_public, self.b_public = A, b
        self.__x_private = x


    def viewClaim(self) -> None:
        '''
        viewClaim is where the prover shows the verifier the claim they are making.
        '''

        # print func
        p = lambda col : print(f"{col}", end=" ")  
    
        print("Claim: Ax = b\n")
        print("A =")
        for i in range(self.A_public.shape[0]):
            [p(col) for col in self.A_public[i]] # print each column
            print()
 
        print("\nb = ( ", end="")
        [p(col) for col in self.b_public] # print each row of b
        print(")\n")

    
    def makeProof(self) -> List:
        '''
        makeProof is where the private solution is converted into eliptic curve space. 

        The agreed upon protocol between the prover and the verifier is that the the proof made 
        by this function (a vector of each x multiplied by the Generator) will be used in the 
        Verifier class to compute the constant vector b of Ax=b in elliptic curve space. The verifier 
        will do the public variable conversion, and the prover will do the private variable conversion.

        If the computed product vector is equal to the constant vector b multiplied by the Generator,
        then the verifier will know that the prover knows the solution to the system of equations.
        '''
        
        # multiply each x by the Generator into a tuple
        return [multiply(G1, x) for x in self.__x_private]



