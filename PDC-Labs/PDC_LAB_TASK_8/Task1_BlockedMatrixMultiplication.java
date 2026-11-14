
import java.util.Random;

public class Task1_BlockedMatrixMultiplication {

    public static void main(String[] args) {

    }
}

// Define matrix size
int N = 2048;

// Define block size
int BLOCK_SIZE = 64;

// Create first matrix
double[][] A = new double[N][N];

// Create second matrix
double[][] B = new double[N][N];

// Create result matrix
double[][] C = new double[N][N];
// Create random number generator
Random rand = new Random(42);