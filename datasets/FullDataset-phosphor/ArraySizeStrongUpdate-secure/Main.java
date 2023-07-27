import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

public class Main {

    static int secret = MultiTainter.taintedInt(42, "secret"); // @Phosphor

    public static void main(String[] args) {
        int[] a = new int[secret];
        a = new int[5];
        int print; // @Phosphor
        print = a.length; // @Phosphor
        Taint t = MultiTainter.getTaint(print); // @Phosphor
        if (t.getLabels().length > 0) { // @Phosphor
        	System.out.println("Phosphor: 'print' is tainted"); // @Phosphor
        	System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        } else System.out.println("Phosphor: 'print' is not tainted"); // @Phosphor
        System.out.println(print);
    }
}
