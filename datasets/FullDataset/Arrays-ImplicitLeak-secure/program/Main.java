public class Main {

    static private int secret = 42;

    public static void main(String[] args) {

        int[] arr = new int[5];
        arr[0] = secret;

	String print; // @HyperTesting
        if (arr[0] == 42) {
            print = "checked"; // @HyperTesting
            System.out.println(print); // @HyperTesting
        } else {
            print = "checked"; // @HyperTesting
            System.out.println(print); // @HyperTesting
        }
        print = print; // @HyperTesting

    }

}
