import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

public class lostInCast {

        public static int getRandomInt(){return 42;}
	
	public static int doIt(int h){
		int h_ = MultiTainter.taintedInt(h, "h_"); // @Phosphor
		// Assign the high variable h to the most significant half of the long variable x
		long x = h_*256*256*256*256; // 4bytes to the left // @Phosphor
		
		// Fill the least-significant part of x with random garbage
		x+= (getRandomInt());
		
		
		// Assign x to the low variable l
		// Here is where the "magic" happens
		// The casting form long to int drops the four most significant bytes, which contain the secret
		int l = (int) x;
		
		Taint t = MultiTainter.getTaint(l); // @Phosphor
        	if (t.getLabels().length > 0) { // @Phosphor
        		System.out.println("Phosphor: 'l' is tainted"); // @Phosphor
        		System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        	} else System.out.println("Phosphor: 'l' is not tainted"); // @Phosphor
		return l;
	}
	
	public static void main(String[] args) {	
		// Assign first input parameter to the high variable
		int h=getRandomInt();
		
		// Do very important math
		doIt(h);		
	}
}
