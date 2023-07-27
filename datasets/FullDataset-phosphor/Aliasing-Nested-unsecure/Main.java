import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

public class Main {

    static class A {
        B b;

        A(B b) {
            this.b = b;
        }
    }

    static class B {
        int val;

        B(int val) {
            this.val = val;
        }
    }

    static int secret = MultiTainter.taintedInt(42, "secret"); // @Phosphor

    public static void main(String[] args) {
        B b = new B(1);
        A a = new A(b);

        b.val = secret;

        int print; // @Phosphor
        print = a.b.val; // @Phosphor
        Taint t = MultiTainter.getTaint(print); // @Phosphor
        if (t.getLabels().length > 0) { // @Phosphor
        	System.out.println("Phosphor: 'print' is tainted"); // @Phosphor
        	System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        } else System.out.println("Phosphor: 'print' is not tainted"); // @Phosphor
        System.out.println(print); // @Phosphor
    }
}
