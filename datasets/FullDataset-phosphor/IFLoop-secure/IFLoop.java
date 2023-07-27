import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

public class IFLoop {
  
    
   public static void main(String[] args){
      IFLoop ifl = new IFLoop();
      ifl.secure_ifl(17);
   }
      

    public int secure_ifl(int high) {
    	int high_ = MultiTainter.taintedInt(high, "high_"); // @Phosphor
	int x = 0;
	int y = 0;
	int low = 23;
        //@ loop_invariant 0 <= y && y <= 10;
        //@ determines low, y, (y < 10 ? x : 0) \by \itself;
        //@ assignable low;
        //@ decreases 10 - y;
	while (y < 10) {
	    low = x;
	    if (y == 5) {
		x = high_; //@Phosphor
		y = 9;
	    }
	    x++;
	    y++;
	}
	int ret = low; // @Phosphor
	Taint t = MultiTainter.getTaint(ret); // @Phosphor
        if (t.getLabels().length > 0) { // @Phosphor
        	System.out.println("Phosphor: 'ret' is tainted"); // @Phosphor
        	System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        } else System.out.println("Phosphor: 'ret' is not tainted"); // @Phosphor
	return ret; // @Phosphor
    }
}
