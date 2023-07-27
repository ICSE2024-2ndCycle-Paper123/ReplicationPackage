
  public class program { // @HyperTesting
      public static boolean foo(boolean h) {
        boolean ret; // @HyperTesting
        ret = deep1(h); // @HyperTesting
        return ret; // @HyperTesting
      }



      public static boolean deep1(boolean x) {
        return deep2(x);
      }


      public static boolean deep2(boolean x) {
        return deep3(x);
      }


      public static boolean deep3(boolean x) {
        return deep4(x);
      }


      public static boolean deep4(boolean x) {
        return deep5(x);
      }


      public static boolean deep5(boolean x) {
        return deep6(x);
      }


      public static boolean deep6(boolean x) {
        return deep7(x);
      }


      public static boolean deep7(boolean x) {
        return deep8(x);
      }


      public static boolean deep8(boolean x) {
        return deep9(x);
      }


      public static boolean deep9(boolean x) {
        return deep10(x);
      }


      public static boolean deep10(boolean x) {
        return deep11(x);
      }


      public static boolean deep11(boolean x) {
        return deep12(x);
      }


      public static boolean deep12(boolean x) {
        return deep13(x);
      }


      public static boolean deep13(boolean x) {
        return deep14(x);
      }


      public static boolean deep14(boolean x) {
        return deep15(x);
      }


      public static boolean deep15(boolean x) {
        return deep16(x);
      }


      public static boolean deep16(boolean x) {
        return deep17(x);
      }


      public static boolean deep17(boolean x) {
        return deep18(x);
      }


      public static boolean deep18(boolean x) {
        return deep19(x);
      }


      public static boolean deep19(boolean x) {
        return deep20(x);
      }


      public static boolean deep20(boolean x) {
        return deep21(x);
      }


      public static boolean deep21(boolean x) {
        return deep22(x);
      }


      public static boolean deep22(boolean x) {
        return deep23(x);
      }


      public static boolean deep23(boolean x) {
        return deep24(x);
      }


      public static boolean deep24(boolean x) {
        return deep25(x);
      }


      public static boolean deep25(boolean x) {
        return deep26(x);
      }


      public static boolean deep26(boolean x) { // @HyperTesting
        return x; // @HyperTesting
      }
  

      public static void main (String [] args) {
        foo(randBool());
      }

      /** Helper method to obtain a random boolean */
      static boolean randBool() {
          return System.currentTimeMillis() % 2 == 0;
      }

      /** Helper methot to obtain a random integer */
      static int randInt() {
        return (int) System.currentTimeMillis();
      }

  }

