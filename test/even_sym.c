#include <stdio.h>
#include <assert.h>
#include <klee/klee.h>

/* funkcija vraca 1 ukoliko je x paran, inace 0 */
int even(int x) {
// 1. primer
/*
  if(x%5 == 0)
    x--;
  else
    x++;
  if(x%4 == 0)
    x+=2;
  else
    x-=2;
  if(x%3 == 1)
    x++;
  else
    x--;
*/
// 2. primer
/*
  if(x%5 == 0){
    x *= -2;
  }
  if(x < 5){
    if(x < -1){
      x = 1;
    }
    x = 2;
  }
*/
// 3. primer

  if(x > 5){
    if(x >= 10){
      if(x%2 == 0){
	x = 2;
      }
      else{
	x = 3;
      }
    }
    else{
      if(x % 2 != 0){
        x++;
      }
      else{
	x /= 2;
      }
    }
  }
  else{
    //x = 11;
    if(x < 3){
      x *= 12;
    }
    else{
      x--;
    }
  }


  klee_assert(0);
  return 1; // nedostizna naredba
}

int main(int argc, char* argv[]) {
  int x;
  /* oznacavamo da je x simbolicka promenljiva:
	argumenti funkcije:
		- adresa promenljive
		- velicina
		- ime (proizvoljna niska karktera)
  */
  klee_make_symbolic(&x, sizeof(x), "x");

  return even(x);

}
