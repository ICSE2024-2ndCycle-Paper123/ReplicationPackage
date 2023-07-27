public class program {

    public static int foo(int h) { // @HyperTesting
        int y = id(h);
        int x = 0;
        int ret; // @HyperTesting
        ret = id(x); // @HyperTesting
        return ret; // @HyperTesting
    }

    static int id(int x) {
      return x;
    }

    public static void main (String[] args) {
        foo(randInt());
    }

    /** Helper method to obtain a random boolean */
    static boolean randBool() {
        return true;
    }
    /** Helper methot to obtain a random integer */
    static int randInt() {
        return 42;
    }

}
