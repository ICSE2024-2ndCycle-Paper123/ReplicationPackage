import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

class Eg1 {
	public static void main(String args[]){
		f(randInt(), randInt());
	}

	public static int f(int h, int l)
	{
		int h_ = MultiTainter.taintedInt(h, "h_"); // @Phosphor
		l = h_; // @Phosphor
		Taint t = MultiTainter.getTaint(l); // @Phosphor
        	if (t.getLabels().length > 0) { // @Phosphor
        		System.out.println("Phosphor: 'l' is tainted"); // @Phosphor
        		System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        	} else System.out.println("Phosphor: 'l' is not tainted"); // @Phosphor
		return l;
	}

    /** Helper methot to obtain a random integer */
    static int randInt() {
        return 42;
    }

}
