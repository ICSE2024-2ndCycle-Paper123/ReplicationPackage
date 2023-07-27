import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

public class simpleArraySize {
	
	public static void main(String[] args) {
		int value = 5;
		simpleArraySize.arraySizeLeak(value);
	}

	/**
	 * Returns the number that was given, by passing
	 * it trough an array size.
	 * @param h secret value
	 * @return value given
	 */
	public static int arraySizeLeak(int h) {
		int h_ = MultiTainter.taintedInt(h, "h_"); // @Phosphor
		int[] array = new int[h_]; // @Phosphor
		
		int ret; // @Phosphor
        	ret = array.length; // @Phosphor
        	Taint t = MultiTainter.getTaint(ret); // @Phosphor
        	if (t.getLabels().length > 0) { // @Phosphor
        		System.out.println("Phosphor: 'ret' is tainted"); // @Phosphor
        		System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        	} else System.out.println("Phosphor: 'ret' is not tainted"); // @Phosphor
        	return ret; // @Phosphor
	}
}
