public class IFMethodContract {
    public int low;
    private int high;
  
    
   public static void main(String[] args){
      IFMethodContract ifm = new IFMethodContract();
      ifm.insecure_if_high_n1(42);
   }
       
    
    public int insecure_if_high_n1(int high) { // @HyperTesting
		int low;
        if (high > 0) {
            low = n5(high);
        } else {
            low = 7;
        }
        low = n1(high);
        int ret = low; // @HyperTesting
		return ret; // @HyperTesting
    }

    int n1(int x){
		return 27;
    }
    
    int n5(int x) {
        return 15;
    }
    
    
}
