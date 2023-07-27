import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

class DirectAssignment {

    public static void main (String [] args) {
        leakyMethod(randInt());
    }

	public static int leakyMethod(int high) {
		int high_ = MultiTainter.taintedInt(high, "high_"); // @Phosphor
		int ret; // @Phosphor
		ret = high_; //@Phosphor
		Taint t = MultiTainter.getTaint(ret); // @Phosphor
        	if (t.getLabels().length > 0) { // @Phosphor
        		System.out.println("Phosphor: 'ret' is tainted"); // @Phosphor
        		System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        	} else System.out.println("Phosphor: 'ret' is not tainted"); // @Phosphor
		return ret; // @Phosphor
	}

    /** Helper methot to obtain a random integer */
    static int randInt() {
        return 42;
    }
}
