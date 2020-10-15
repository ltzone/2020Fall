#include <stdio.h>


void longa()
 {
   int i,j;
   for(i = 0; i < 1e6; i++)
      j = i; 
 }

 void foo2()
 {
   int i;
   for(i=0 ; i < 10; i++)
        longa();
 }

 void foo1()
 {
   int i;
   for(i = 0; i< 100; i++)
      longa();
 }

 int main(void)
 {
   foo1();
   foo2();
 }
