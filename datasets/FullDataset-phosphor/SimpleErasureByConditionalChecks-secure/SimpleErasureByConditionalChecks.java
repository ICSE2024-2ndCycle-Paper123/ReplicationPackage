import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

class SimpleErasureByConditionalChecks {
    
		public static void main(String args[]) {
        computeSecretly(12);
    }
    
		// compare the secret input to 0, set the return value to some
    // intermediate value, but set the return value to 5 eventually
    private static int computeSecretly(int h) {
    	int h_ = MultiTainter.taintedInt(h, "h_"); // @Phosphor
        int a = 42;

        if (h_ > 0) { // @Phosphor
            a  = 5;
        } else {
            a = 3;
        }

        if (h_ <= 0) { // @Phosphor
            a = 5;
        }

	int ret = a; // @Phosphor
	Taint t = MultiTainter.getTaint(ret); // @Phosphor
        if (t.getLabels().length > 0) { // @Phosphor
        	System.out.println("Phosphor: 'ret' is tainted"); // @Phosphor
        	System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        } else System.out.println("Phosphor: 'ret' is not tainted"); // @Phosphor
        return ret; // @Phosphor
    }
}

