public class DirectAssignment { // @HyperTesting

    public static void main (String[] args) {
        leakyMethod(randInt());
    }

	public static int leakyMethod(int high) {
		int ret; // @HyperTesting
		ret = 0; // @HyperTesting
		return ret; // @HyperTesting
	}

    /** Helper methot to obtain a random integer */
    static int randInt() {
        return 42;
    }
}
