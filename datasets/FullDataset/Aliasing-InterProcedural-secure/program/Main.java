public class Main {

    static class A {
        int val;

        A(int val) {
            this.val = val;
        }

        void update(int val) {
            this.val = val;
        }
    }

    static int secret = 42;

    public static void main(String[] args) {
        A a = new A(1);
        A b = new A(1);
        A c = b;

        doUpdate(a, secret);
        int print; // @HyperTesting
        print = c.val; // @HyperTesting
        System.out.println(print); // @HyperTesting
    }

    static void doUpdate(A a, int val) {
        a.update(val);
    }
}
