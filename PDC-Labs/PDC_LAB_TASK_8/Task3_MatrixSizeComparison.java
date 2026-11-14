import java.util.Random;

public class Task3_MatrixSizeComparison {
    public static void main(String[] args) {
        int[] sizes = { 128, 256, 512, 1024, 1536, 2048 };
        Random rand = new Random();

        System.out.println("=====================================================");
        System.out.printf("%-15s | %-15s | %-18s%n", "Matrix Size", "Memory (MB)", "Time (k->i->j) [s]");
        System.out.println("=====================================================");

        for (int n : sizes) {
            int[][] A = new int[n][n];
            int[][] B = new int[n][n];
            int[][] C = new int[n][n];

            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    A[i][j] = rand.nextInt(10);
                    B[i][j] = rand.nextInt(10);
                }
            }
            // Calculate total memory footprint of 3 matrices (in Megabytes)
            double memoryMB = (3.0 * n * n * 4) / (1024 * 1024);

            long start = System.nanoTime();
            // Best Loop Order from Lab Task 7: k -> i -> j
            for (int k = 0; k < n; k++) {
                for (int i = 0; i < n; i++) {
                    int r = A[i][k]; // Temporal locality in register
                    for (int j = 0; j < n; j++) {
                        C[i][j] += r * B[k][j];
                    }
                }
            }
            long end = System.nanoTime();

            double timeSec = (end - start) / 1e9;
            System.out.printf("%-15s | %-15.2f | %-18.4f%n", n + "x" + n, memoryMB, timeSec);
        }
        System.out.println("=====================================================");
    }
}