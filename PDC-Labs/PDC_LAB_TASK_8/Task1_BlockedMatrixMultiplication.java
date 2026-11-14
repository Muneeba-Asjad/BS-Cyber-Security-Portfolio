import java.util.Random;

public class Task1_BlockedMatrixMultiplication {

    public static void main(String[] args) {

        // Matrix size and block size
        int N = 2048;
        int BLOCK_SIZE = 64;

        // Creating three matrices
        double[][] A = new double[N][N];
        double[][] B = new double[N][N];
        double[][] C = new double[N][N];

        Random rand = new Random(42);

        // Filling matrices A and B with random values
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                A[i][j] = rand.nextDouble();
                B[i][j] = rand.nextDouble();
            }
        }
        System.out.println("Blocked Matrix Multiplication");
        System.out.println("Matrix Size: " + N + " x " + N);
        System.out.println("Block Size: " + BLOCK_SIZE);
        // Starting execution time
        long startTime = System.nanoTime();

        // Dividing matrices into blocks
        for (int ii = 0; ii < N; ii += BLOCK_SIZE) {
            for (int jj = 0; jj < N; jj += BLOCK_SIZE) {
                for (int kk = 0; kk < N; kk += BLOCK_SIZE) {

                    // Multiplication inside each block
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

        // Converting nanoseconds into seconds
        double duration = (endTime - startTime) / 1e9;

        System.out.printf("Execution Time: %.4f seconds%n", duration);

    }
}