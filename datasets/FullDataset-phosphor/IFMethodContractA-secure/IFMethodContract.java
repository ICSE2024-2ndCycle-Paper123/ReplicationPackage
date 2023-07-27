import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

public class IFMethodContract {
    public static int low;
    private static int high = MultiTainter.taintedInt(42, "high"); // @Phosphor
  
    
   public static void main(String[] args){
      IFMethodContract ifm = new IFMethodContract();
      ifm.secure_if_high_n5_n1();
   }
       
    
    void secure_if_high_n5_n1() {
        if (high > 0) {
            low = n5(high);
        } else {
            high = -high;
            low = n5(high + low);
        }
        Taint t = MultiTainter.getTaint(low); // @Phosphor
        if (t.getLabels().length > 0) { // @Phosphor
        	System.out.println("Phosphor: 'low' is tainted"); // @Phosphor
        	System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        } else System.out.println("Phosphor: 'low' is not tainted"); // @Phosphor
    }
    
    
    int n5(int x) {
        high = 2 * x;
        return 15;
    }
    
    
}
