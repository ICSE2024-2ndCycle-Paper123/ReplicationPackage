public class Main {

    static class A {
        int val;

        A(int val) {
            this.val = val;
        }
    }

    static private int secret = 42;

    public static void main(String[] args) {
        A a = new A(1);
        A b = a;

        if (secret == 42) {
            a.val = 2;
        }
	a.val = a.val; // @HyperTesting
	
        int print; // @HyperTesting
        print = b.val; // @HyperTesting
        System.out.println(print); // @HyperTesting
    }
}
