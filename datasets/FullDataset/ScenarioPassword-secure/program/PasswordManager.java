public class PasswordManager {
	private String password = "supersecret";
	private int invalidTries = 0;
	private int maximumTries = 10;
	private boolean loggedIn = false;
	
	public void tryLogin(String tryedPassword) {
		String print = ""; // @HyperTesting
		if(this.invalidTries < this.maximumTries) {
			if(this.password.equals(tryedPassword)) {
				this.loggedIn = true;
			} else {
				this.loggedIn = false;
				this.invalidTries++;
			}
		}
		print = "Login Attempt Completed"; // @HyperTesting
		System.out.println(print); // @HyperTesting
	}
}

