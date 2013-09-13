#include "pso.h"

int cur_n;
struct PARTICLE particle;
struct SWARM swarm;

//初始化种群
void RandInitofSwarm(void)
{
	int i, j;
        //学习因子C1,C2
	swarm.C1 = 2.0;
	swarm.C2 = 2.0;
	for(j = 0; j < Dim; j++)
	{
		swarm.Xdown[j] = -10;    //搜索空间范围
		swarm.Xup[j] = 10;
		swarm.Vmax[j] = 0.1;       //粒子飞翔速度最大值
	}

	srand((unsigned)time(NULL));
	for(i = 0; i < PNum; i++)
	{
		for(j = 0; j < Dim; j++)
		{
			swarm.Particle[i].X[j] = rand() / (double)RAND_MAX * (swarm.Xup[j] - swarm.Xdown[j]) + swarm.Xdown[j];	//-Xdown~Xup
			swarm.Particle[i].V[j] = rand() / (double)RAND_MAX * swarm.Vmax[j] * 2 - swarm.Vmax[j];					//-Vmax~Vmax
		}
	}
}
/*计算适应度函数的适应度，待进一步完善*/
static double ComputAFitness(double X[])
{
	/*
		OK
		min-f(0,0)=3
	*/
#if TEST
	return X[0]*X[0]+X[1]*X[1]+3;
#endif

	/*
		
		min-f(0,-1)=3.x,y-(-2,2)
	*/
#if GOLDSTEIN_PRICE
	return (1+pow(X[0]+X[1]+1,2)*(19-14*X[0]+3*pow(X[0],2)-14*X[1]+6*X[0]*X[1]+ 3*pow(X[1],2))*(30+pow((2*X[0]-3*X[1]),2)*\
		(18-32*X[0]+12*pow(X[0],2)+48*X[1]-36*X[0]*X[1]	+ 27*pow(X[1],2))));
#endif

	/*
		
		min-f(0,0)=-1.x,y-(-4,4)
	*/
#if SCHAFFER
	//函数:Schaffer's F6

	return -1*(0.5-(sin(sqrt(X[0]*X[0]+X[1]*X[1]))*\
		sin(sqrt(X[0]*X[0]+X[1]*X[1]))-0.5)/pow(( 1+0.001*(X[0]*X[0]+X[1]*X[1])),2));

#endif

	/*
		此函数局部极值点有760个。
		min-f(x,y)=-176.541793.x,y-(-10,10)
		(-7.589893,-7.708314),(-7.589893,-1.425128)
		(-7.5898893,4.858057),(-1.306708,-7.708314)
		(-1.306707,-1.425128),(-1.306708,4.858057)
		(4.976478,-7.708314),(4.976478,-1.425128)
		(4.976478,4.858057)
	*/
#if HANSEN
	int i;
	double temp1=0,temp2=0;
	double hansenf=0;
	for (i=1;i <= 5;i++)
	{
		temp1+=i*cos((i-1)*X[0]+i);
		temp2+=i*cos((i-1)*X[1]+i);
	}
	hansenf=-1*temp1*temp2;

	return hansenf;
#endif

	/*
		
		min-f(0,0)=-3600,x,y-(-5.12,5.12)
		该问题的全局最优解被最差解包围,
		局部极值点：(-5.12,5.12),(-5.12,-5.12)
					(5.12,-5.12),(5.12,5.12)
					f=-2748.78
	*/
#if NEEDLE
	return -1*pow((3/(0.05+pow(X[0]-1,2)+pow(X[1]-1,2))),2);
#endif

}

//update  V and X
void UpdateofVandX(void)
{
	int i, j;
	for(i = 0; i < PNum; i++)
	{
		for(j = 0; j < Dim; j++)
			swarm.Particle[i].V[j] = W_FUN * swarm.Particle[i].V[j] +
			rand() / (double)RAND_MAX * swarm.C1 * (swarm.Particle[i].P[j] - swarm.Particle[i].X[j]) +
			rand() / (double)RAND_MAX * swarm.C2 * (swarm.GBest[j] - swarm.Particle[i].X[j]);
		for(j = 0; j < Dim; j++)
		{
			if(swarm.Particle[i].V[j] > swarm.Vmax[j])
				swarm.Particle[i].V[j] = swarm.Vmax[j];
			if(swarm.Particle[i].V[j] < -swarm.Vmax[j])
				swarm.Particle[i].V[j] = -swarm.Vmax[j];
		}

		for(j = 0; j < Dim; j++)
		{
			swarm.Particle[i].X[j] += swarm.Particle[i].V[j];
			if(swarm.Particle[i].X[j] > swarm.Xup[j])
				swarm.Particle[i].X[j] = swarm.Xup[j];
			if(swarm.Particle[i].X[j] < swarm.Xdown[j])
				swarm.Particle[i].X[j] = swarm.Xdown[j];
		}
	}
}

/*更新个体极值P和全局极值GBest*/
void UpdatePandGbest(void)
{
	int i, j;
	//update of P if the X is bigger than current P
	for (i = 0; i < PNum; i++)
	{
		if (swarm.Particle[i].Fitness < ComputAFitness(swarm.Particle[i].P))
		{
			for(j = 0; j < Dim; j++)
			{
				swarm.Particle[i].P[j] = swarm.Particle[i].X[j];
			}
		}
	}
	//update of GBest
	for(i = 0; i < PNum; i++)
		if(ComputAFitness(swarm.Particle[i].P) < ComputAFitness(swarm.Particle[swarm.GBestIndex].P))
			swarm.GBestIndex = i;
	for(j = 0; j < Dim; j++)
	{
		swarm.GBest[j] = swarm.Particle[swarm.GBestIndex].P[j];
	}
	printf("The %dth iteraction.\n",cur_n);
	printf("GBestIndex:%d \n",swarm.GBestIndex );
	printf("GBest:" );
	for(j=0;j<Dim;j++)
	{
		printf("%.4f ,",swarm.GBest[j]);
	}
	printf("\n" );
	printf("Fitness of GBest: %f \n\n",ComputAFitness(swarm.Particle[swarm.GBestIndex].P));
}