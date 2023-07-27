import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

class Aliasing {

    static class A { 
        int i; 
    }

    static void set(A v1, A v2, int h) {
        v1.i = h;
    }

    static int getNumber() {return 42;}

    static int test(int i){
    	int i_ = MultiTainter.taintedInt(i, "i_"); // @Phosphor
    	A v1 = new A();
        A v2 = new A();        
        set (v1, v2, i_); // @Phosphor
        int ret; // @Phosphor
        ret = v2.i; // @Phosphor
        Taint t = MultiTainter.getTaint(ret); // @Phosphor
        if (t.getLabels().length > 0) { // @Phosphor
        	System.out.println("Phosphor: 'ret' is tainted"); // @Phosphor
        	System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        } else System.out.println("Phosphor: 'ret' is not tainted"); // @Phosphor
        return ret; // @Phosphor
    }

    public static void main (String args[]) throws Exception {
        test(getNumber());
    }
}
