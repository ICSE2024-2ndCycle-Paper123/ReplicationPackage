public class LeakyClass {

	public static boolean leakyMethod(boolean isSecret) {
		boolean ret;
		ret = (isSecret && true);
		return ret;
	}
	
}
