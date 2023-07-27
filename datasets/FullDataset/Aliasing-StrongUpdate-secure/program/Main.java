public class Main {

    static class A {
        int val;

        A(int val) {
            this.val = val;
        }
    }

    static int secret=42;

    public static void main(String[] args) {
        A a = new A(secret);
        A b = new A(5);
        A c = b;

        b = a;

        a.val = 2;
        int print; // @HyperTesting
        print = c.val; // @HyperTesting
        System.out.println(print); // @HyperTesting
    }
}
