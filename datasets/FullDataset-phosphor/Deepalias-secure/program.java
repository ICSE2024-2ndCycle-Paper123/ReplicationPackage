  import edu.columbia.cs.psl.phosphor.runtime.MultiTainter; // @Phosphor
  import edu.columbia.cs.psl.phosphor.runtime.Taint; // @Phosphor
  import java.util.Arrays; // @Phosphor
  
  class program {
      public static class A {
        private boolean x;
        public A(boolean x) {this.x=x;}
        public boolean get() {return (this.x);}
      }
      public static boolean foo(boolean h) {
        boolean h_ = MultiTainter.taintedBoolean(h, "h_"); // @Phosphor
        A a1 = new A(h_); // @Phosphor
        A a2 = new A(true);

        A a3 = new A(a1.get());
        A a4 = new A(a2.get());

        A a5 = new A(a3.get());
        A a6 = new A(a4.get());

        A a7 = new A(a5.get());
        A a8 = new A(a6.get());

        A a9 = new A(a7.get());
        A a10 = new A(a8.get());

        A a11 = new A(a9.get());
        A a12 = new A(a10.get());

        A a13 = new A(a11.get());
        A a14 = new A(a12.get());

        A a15 = new A(a13.get());
        A a16 = new A(a14.get());

        A a17 = new A(a15.get());
        A a18 = new A(a16.get());

        A a19 = new A(a17.get());
        A a20 = new A(a18.get());

        A a21 = new A(a19.get());
        A a22 = new A(a20.get());

        A a23 = new A(a21.get());
        A a24 = new A(a22.get());

        A a25 = new A(a23.get());
        A a26 = new A(a24.get());

        boolean ret; // @Phosphor
	ret = a26.get(); // @Phosphor
	Taint t = MultiTainter.getTaint(ret); // @Phosphor
	if (t.getLabels().length > 0) { // @Phosphor
        	System.out.println("Phosphor: 'ret' is tainted"); // @Phosphor
        	System.out.println("Phosphor: taint labels " + Arrays.toString(t.getLabels())); // @Phosphor
        } else System.out.println("Phosphor: 'ret' is not tainted"); // @Phosphor
        return ret; // @Phosphor
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

