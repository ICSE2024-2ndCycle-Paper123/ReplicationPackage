public class Aliasing { // @HyperTesting

    static class A { 
        int i; 
    }

    static void set(A v1, A v2, int h) {
        v1.i = h;
    }

    static int getNumber() {return 42;}

    public static int test(int i){ // @HyperTesting
    	A v1 = new A();
        A v2 = new A();        
        v2 = v1;
        set (v1, v2, i);
        int ret; // @HyperTesting
        ret = v2.i // @HyperTesting
        return ret; // @HyperTesting
    }

    public static void main (String args[]) throws Exception {
        test(getNumber());
    }
}
