import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

public class program {

    static int foo(int h) {
        int h_ = MultiTainter.taintedInt(h, "h_"); // @Phosphor
        int y = id(h_); // @Phosphor
        int x = 0;
        int ret; // @Phosphor
        ret = id(x); // @Phosphor
        Taint t = MultiTainter.getTaint(ret); // @Phosphor
        if (t.getLabels().length > 0) { // @Phosphor
        	System.out.println("Phosphor: 'ret' is tainted"); // @Phosphor
        	System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        } else System.out.println("Phosphor: 'ret' is not tainted"); // @Phosphor
        return ret; // @Phosphor
    }

    static int id(int x) {
      return x;
    }

    public static void main (String [] args) {
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
