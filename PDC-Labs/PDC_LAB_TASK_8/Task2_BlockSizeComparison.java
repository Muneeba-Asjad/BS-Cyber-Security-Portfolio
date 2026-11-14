
import java.util.Random;

public class Task2_BlockSizeComparison {

    public static void main(String[] args) {

    }
}

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