import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

public class Main {

    static class A {
        int val;

        A(int val) {
            this.val = val;
        }
    }

    static int secret = MultiTainter.taintedInt(42, "secret"); // @Phosphor

    public static void main(String[] arg) {
        A a = new A(secret);
        A b = new A(5);
        A c = b;

        b = a;

        a.val = 2;

        int print; // @Phosphor
        print = c.val; // @Phosphor
        Taint t = MultiTainter.getTaint(print); // @Phosphor
        if (t.getLabels().length > 0) { // @Phosphor
        	System.out.println("Phosphor: 'print' is tainted"); // @Phosphor
        	System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        } else System.out.println("Phosphor: 'print' is not tainted"); // @Phosphor
        System.out.println(print); // @Phosphor
    }
}
