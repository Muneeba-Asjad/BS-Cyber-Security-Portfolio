
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
            }