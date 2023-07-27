public class IFMethodContract {
    public static int low;
    private static int high;
  
    
   public static void main(String[] args){
      IFMethodContract ifm = new IFMethodContract();
      ifm.secure_if_high_n5_n1();
   }
       
    
   public void secure_if_high_n5_n1() { // @HyperTesting
        if (high > 0) {
            low = n5(high);
        } else {
            high = -high;
            low = n5(high + low);
        }
        low = low; // @HyperTesting
        
    }
    
    
    int n5(int x) {
        high = 2 * x;
        return 15;
    }
    
    
}
