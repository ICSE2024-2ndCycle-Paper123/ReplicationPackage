import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

public class program {
    public static int foo(int h) {
    	int h_ = MultiTainter.taintedInt(h, "h_"); // @Phosphor
        int [] a = new int [2];
        a[0] = h_; // @Phosphor
        int ret; // @Phosphor
        ret = a[1]; // @Phosphor
        Taint t = MultiTainter.getTaint(ret); // @Phosphor
        if (t.getLabels().length > 0) { // @Phosphor
        	System.out.println("Phosphor: 'ret' is tainted"); // @Phosphor
        	System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        } else System.out.println("Phosphor: 'ret' is not tainted"); // @Phosphor
        return ret; // @Phosphor
    }
    
    public static void main(String[] args) { // @Phosphor
    	foo(42); // @Phosphor
    } // @Phosphor
}
