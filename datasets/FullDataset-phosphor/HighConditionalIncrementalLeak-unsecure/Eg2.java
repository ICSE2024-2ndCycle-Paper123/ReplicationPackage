import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

class Eg2 {
    public static void main(String args[]){
			int h = 5;
			int l = 1;
                        f(h,l);	
			//System.out.println(f(h, l));
    }

    public static int f(int h, int l)
    {
    			int h_ = MultiTainter.taintedInt(h, "h_"); // @Phosphor
			while (h_>0){ // @Phosphor
				h_--; // @Phosphor
                    	    	l++;
			}
			Taint t = MultiTainter.getTaint(l); // @Phosphor
        		if (t.getLabels().length > 0) { // @Phosphor
        			System.out.println("Phosphor: 'l' is tainted"); // @Phosphor
        			System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        		} else System.out.println("Phosphor: 'l' is not tainted"); // @Phosphor
			return l;
    }
}
