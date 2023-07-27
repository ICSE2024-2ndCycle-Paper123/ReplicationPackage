import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
import java.util.Arrays; // @Phosphor

public class PasswordManager {
	private String password = "supersecret";
	private int invalidTries = MultiTainter.taintedInt(0, "invalidTries"); // @Phosphor
	private int maximumTries = 10;
	private boolean loggedIn = MultiTainter.taintedBoolean(false, "loggedIn"); // @Phosphor
	
	public void tryLogin(String tryedPassword) {
		String print = ""; // @Phosphor
		if(this.invalidTries < this.maximumTries) {
			if(this.password.equals(tryedPassword)) {
				this.loggedIn = true;
				this.invalidTries=0;
			} else {
				this.loggedIn = false;
				this.invalidTries++;
			}
		} else {
			print = "No more password tries allowed"; // @Phosphor
		}
		Taint t1 = MultiTainter.getTaint(tryedPassword); // @Phosphor
        	if (t1.getLabels().length > 0) { // @Phosphor
        		System.out.println("Phosphor: 'tryedPassword' is tainted"); // @Phosphor
        		System.out.println("Phosphor: taint labels " + Arrays.toString(t1.getLabels())); // @Phosphor
        	} else System.out.println("Phosphor: 'tryedPassword' is not tainted"); // @Phosphor
		Taint t2 = MultiTainter.getTaint(print); // @Phosphor
        	if (t2.getLabels().length > 0) { // @Phosphor
        		System.out.println("Phosphor: 'print' is tainted"); // @Phosphor
        		System.out.println("Phosphor: taint labels " + Arrays.toString(t2.getLabels())); // @Phosphor
        	} else System.out.println("Phosphor: 'print' is not tainted"); // @Phosphor
		System.out.println(print); // @Phosphor
	}
	public static void main(String[] args) { // @Phosphor
		PasswordManager pm = new PasswordManager(); // @Phosphor
		pm.tryLogin("password"); // @Phosphor
	} // @Phosphor
}
