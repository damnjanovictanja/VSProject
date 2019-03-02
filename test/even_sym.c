#include <stdio.h>
#include <assert.h>
#include <klee/klee.h>

/* funkcija vraca 1 ukoliko je x paran, inace 0 */
int even(int x) {
  if (x%3==0){
    if(x>5)
			x++;
    else {
			if ()
		}
			return 4;
	}
  if(x%2){
    if(x>7)
			return 11;
    else
			x++;
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
