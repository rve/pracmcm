#ifndef _PSO_H_
#define _PSO_H_

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

/*各种适应度函数选择，要用哪个，就设置为1,但只能有一个为1*/
#define TEST 0
#define GOLDSTEIN_PRICE	0
#define SCHAFFER 1
#define HANSEN	0
#define NEEDLE	0

#define Dim 30 //粒子维度
#define PNum 20		//种群规模
#define ITE_N  100 //最大迭代次数
extern int cur_n;			//当前迭代次数

/*惯性权重函数*/
#define W_START 1.4
#define W_END	0.4
//#define W_FUN	(W_START-(W_START-W_END)*pow((double)cur_n/ITE_N,2))
//#define W_FUN 0.1
/*个体和种群结构体*/
struct PARTICLE
{
	double X[Dim];
	double P[Dim];
	double V[Dim];
	double Fitness;
};
extern struct PARTICLE particle;

struct SWARM
{
	struct PARTICLE Particle[PNum];
	int GBestIndex;
	double GBest[Dim];
	double C1;
	double C2;
  double W;
  int State;
	double Xup[Dim];
	double Xdown[Dim];
	double Vmax[Dim];
} ;
extern struct SWARM swarm;

/*是的，只要三个就好了，更好理解点感觉*/
void RandInitofSwarm(void);
void UpdateofVandX(void);
double UpdatePandGbest(void);
void UpdateParams(void);
void debug(void);

#endif

