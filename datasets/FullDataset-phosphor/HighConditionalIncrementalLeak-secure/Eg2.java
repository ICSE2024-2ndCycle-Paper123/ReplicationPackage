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
			}
			return l;
    }
}
