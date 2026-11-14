
import java.util.Random;

public class Task2_BlockSizeComparison {

    public static void main(String[] args) {

    }}

    // Define matrix size
    int N = 2048;
    // Different block sizes
    int[] blockSizes = { 16, 32, 64, 128, 256 };
    // Creating first matrix
    double[][] A = new double[N][N];
    // Creating second matrix
    double[][] B = new double[N][N];
    // Creating result matrix
    double[][] C = new double[N][N];
    // Create random number generator
    Random rand = new Random(42);
    // Initializing matrices A and B
    for(
    int i = 0;i<N;i++)
    {
        for (int j = 0; j < N; j++) {
            A[i][j] = rand.nextDouble();
            B[i][j] = rand.nextDouble();
        }
    }
    // Store execution times
    double[] times = new double[5];
    // Testing different block sizes
    for(
    int b = 0;b<blockSizes.length;b++)
    {

            int BLOCK_SIZE = blockSizes[b];

        }
    // Reset matrix C
    for(
    int i = 0;i<N;i++)
    {
        for (int j = 0; j < N; j++) {
            C[i][j] = 0;
        }
    }System.out.println("Testing Block Size: "+BLOCK_SIZE);

    long startTime = System.nanoTime();
    // Blocked Matrix Multiplication
    for(
    int ii = 0;ii<N;ii+=BLOCK_SIZE)
    {
        for (int jj = 0; jj < N; jj += BLOCK_SIZE) {
            for (int kk = 0; kk < N; kk += BLOCK_SIZE) {

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
long endTime = System.nanoTime();

times[b]=(endTime-startTime)/1e9
;