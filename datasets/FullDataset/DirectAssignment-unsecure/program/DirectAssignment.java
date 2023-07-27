public class DirectAssignment { // @HyperTesting

    public static void main (String [] args) {
        leakyMethod(randInt());
    }

	public static int leakyMethod(int high) {
		int ret; // @HyperTesting
		ret = high; // @HyperTesting
		return ret; // @HyperTesting
	}

    /** Helper methot to obtain a random integer */
    static int randInt() {
        return 42;
    }
}
