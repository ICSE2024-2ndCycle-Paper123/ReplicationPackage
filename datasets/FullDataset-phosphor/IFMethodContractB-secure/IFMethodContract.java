import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

public class IFMethodContract {
    public int low;
    private int high;
  
    
   public static void main(String[] args){
      IFMethodContract ifm = new IFMethodContract();
      ifm.insecure_if_high_n1(42);
   }
       
    
    int insecure_if_high_n1(int high) {
    	int high_ = MultiTainter.taintedInt(high, "high_"); // @Phosphor
		int low;
        if (high_ > 0) { // @Phosphor
            low = n5(high_); // @Phosphor
        } else {
            low = 7;
        }
        low = n1(high_); // @Phosphor
        int ret = low; // @Phosphor
	Taint t = MultiTainter.getTaint(ret); // @Phosphor
        if (t.getLabels().length > 0) { // @Phosphor
        	System.out.println("Phosphor: 'ret' is tainted"); // @Phosphor
        	System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        } else System.out.println("Phosphor: 'ret' is not tainted"); // @Phosphor
        return ret; // @Phosphor
    }

    int n1(int x){
		return 27;
    }
    
    int n5(int x) {
        return 15;
    }
    
    
}
