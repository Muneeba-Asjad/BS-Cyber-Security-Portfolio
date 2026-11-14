import java.util.Random;

public class Task4_PerformanceComparison {

    public static void main(String[] args) {
        int n = 1536; // Large enough to exceed L2/L3 cache limits
        int blockSize = 64; // Optimal tile size for typical 64-byte cache lines

        int[][] A = new int[n][n];
        int[][] B = new int[n][n];
        int[][] C_bestOrder = new int[n][n];
        int[][] C_blocked = new int[n][n];

        Random rand = new Random();
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                A[i][j] = rand.nextInt(10);
                B[i][j] = rand.nextInt(10);
            }
        }
        System.out.println("Running Comparison on Matrix Size: " + n + "x" + n + "\n");
        // 1. Best Loop Order (k -> i -> j) without Blocking
        long start1 = System.nanoTime();
        for (int k = 0; k < n; k++) {
            for (int i = 0; i < n; i++) {
                int r = A[i][k];
                for (int j = 0; j < n; j++) {
                    C_bestOrder[i][j] += r * B[k][j];
                }
            }
        }
        long end1 = System.nanoTime();
        double timeBestOrder = (end1 - start1) / 1e9;
        // 2. Cache Blocked (Tiled) Multiplication (Block Size = 64)
        long start2 = System.nanoTime();
        for (int ii = 0; ii < n; ii += blockSize) {
            for (int kk = 0; kk < n; kk += blockSize) {
                for (int jj = 0; jj < n; jj += blockSize) {
                    for (int i = ii; i < Math.min(ii + blockSize, n); i++) {
                        for (int k = kk; k < Math.min(kk + blockSize, n); k++) {
                            int r = A[i][k];
                            for (int j = jj; j < Math.min(jj + blockSize, n); j++) {
                                C_blocked[i][j] += r * B[k][j];
                            }
                        }
                    }
                }
            }
        }
        long end2 = System.nanoTime();
        double timeBlocked = (end2 - start2) / 1e9;
        // Results Table
        System.out.println("=======================================================");
        System.out.printf("%-30s | %-18s%n", "Implementation Approach", "Execution Time (s)");
        System.out.println("=======================================================");
        System.out.printf("%-30s | %-18.4f%n", "Best Loop Order (k -> i -> j)", timeBestOrder);
        System.out.printf("%-30s | %-18.4f%n", "Blocked Multiplication (B=64)", timeBlocked);
        System.out.println("=======================================================");
    }
}