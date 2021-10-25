import org.apache.commons.math3.random.RandomGenerator;
import org.apache.commons.math3.random.MersenneTwister;

class QuickStart {
    public static void main(String[] args) {
        RandomGenerator prng = new MersenneTwister(0);
        for (int i = 0; i < 3; ++i) {
            long num = prng.nextLong();
            System.out.println(Long.toString(num) + "\t" + Long.toBinaryString(num));
        }
        System.out.println();
        for (int i = 0; i < 3; ++i) {
            int num = prng.nextInt();
            System.out.println(Integer.toString(num) + "\t" + Integer.toBinaryString(num));
        }
        System.out.println();
        for (int i = 0; i < 3; ++i) {
            double num = prng.nextDouble();
            System.out.println(Double.toString(num) + "\t" + Long.toBinaryString(Double.doubleToRawLongBits(num)));
        }
    }
}