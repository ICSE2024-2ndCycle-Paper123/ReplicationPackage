import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

class BooleanOperations {
	public static boolean leakyMethod(boolean high) {
		boolean high_ = MultiTainter.taintedBoolean(high, "high_"); //@Phosphor
		boolean ret;
		ret = (high_ && true); // @Phosphor
		Taint t = MultiTainter.getTaint(ret); // @Phosphor
        	if (t.getLabels().length > 0) { // @Phosphor
        		System.out.println("Phosphor: 'ret' is tainted"); // @Phosphor
        		System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
       	} else System.out.println("Phosphor: 'ret' is not tainted"); // @Phosphor
		return ret;
	}
	public static void main(String[] args) { // @Phosphor
		leakyMethod(true); // @Phosphor
	} // @Phosphor
}
