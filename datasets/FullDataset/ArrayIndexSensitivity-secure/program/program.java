public class program {
    public static int foo(int h) {
        int [] a = new int [2];
        a[0] = h;
        int ret; // @HyperTesting
        ret = a[1]; // @HyperTesting
        return ret; // @HyperTesting
    }
}
