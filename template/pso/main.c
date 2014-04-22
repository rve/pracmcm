#include "pso.h"
#include <stdio.h>
#include <string.h>
#include <unistd.h>



int main(int argc, const char *argv[])
{
  srand((unsigned)time(NULL));
  double ret[ITE_N+10];
  memset(ret, 0, sizeof(ret));
  for (int i=0; i<30; i++) {
    cur_n=0;
    RandInitofSwarm();             //初始化粒子群
    while(cur_n++ != ITE_N)
    {
      UpdateofVandX();        //速度和位置更新，即飞翔
      ret[cur_n] += UpdatePandGbest();    //更新个体历史最优解P和全局最优解GBest
      UpdateParams();
      debug();
    }
    //usleep(900000);
  }
  /*
  for (int i=0; i<ITE_N; i++) {
    printf("%f ", ret[i]/30.0);
  }
  printf("\n\n");
  */
  for (int i=1; i<ITE_N; i++) {
    printf("%lf %lf %d %lf\n", W_FUN, MC1, i, ret[i]/30); 
  }

	return 0;
}
