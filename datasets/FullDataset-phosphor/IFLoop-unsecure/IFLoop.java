import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

public class IFLoop {
    public int low;
    private int high = MultiTainter.taintedInt(0, "high"); // @Phosphor


   public static void main(String[] args){
      IFLoop ifl = new IFLoop();
      ifl.insecure_ifl();
   }
      

    public void insecure_ifl() {
	int x = 0;
	int y = 0;
	while (y < 10) {
	    print(x);
	    if (y == 5) {
		x = high;
	    }
	    x++;
	    y++;
	}
	Taint t = MultiTainter.getTaint(low); // @Phosphor
        if (t.getLabels().length > 0) { // @Phosphor
        	System.out.println("Phosphor: 'low' is tainted"); // @Phosphor
        	System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        } else System.out.println("Phosphor: 'low' is not tainted"); // @Phosphor
    }

    public void print(int x) {
            low = x;
    }
}
