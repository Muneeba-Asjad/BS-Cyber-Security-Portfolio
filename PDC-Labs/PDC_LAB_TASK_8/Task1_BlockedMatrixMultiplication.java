
import java.util.Random;

public class Task1_BlockedMatrixMultiplication {

    public static void main(String[] args) {

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

        // Fill input matrices with random values
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {

                A[i][j] = rand.nextDouble();
                B[i][j] = rand.nextDouble();

            }
        }

        // Display matrix information
        System.out.println("Blocked Matrix Multiplication");
        System.out.println("Matrix Size: " + N + " x " + N);
        System.out.println("Block Size: " + BLOCK_SIZE);

        // Starting execution time
        long startTime = System.nanoTime();

        // Divide matrices into blocks
        for (int ii = 0; ii < N; ii += BLOCK_SIZE) {
            for (int jj = 0; jj < N; jj += BLOCK_SIZE) {
                for (int kk = 0; kk < N; kk += BLOCK_SIZE) {

                    // Multiply values inside each block
                    for (int i = ii; i < ii + BLOCK_SIZE; i++) {
                        for (int j = jj; j < jj + BLOCK_SIZE; j++) {

                            double sum = C[i][j];

                            for (int k = kk; k < kk + BLOCK_SIZE; k++) {
                                sum += A[i][k] * B[k][j];
                            }

                            C[i][j] = sum;

                        }
                    }

                }
            }
        }

        // Ending execution time
        long endTime = System.nanoTime();

        // Calculate execution duration
        double duration = (endTime - startTime) / 1e9;

        // Display execution time
        System.out.printf("Execution Time: %.4f seconds%n", duration);

    }
}
