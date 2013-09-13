#include <stdlib.h>
#include <time.h>
#include <iostream>
#include <fstream>
#include <math.h>
#include <stdio.h>
using namespace  std;

/////////////////////////////////////////////////
//产生（0，1）均匀分布的随机数
double randnum()
{
	double x;
	x = (double) rand()/RAND_MAX;
	return x;
}

//////////////////////////////////////////////////
//目标函数表达式
inline double obfun(double x)
{
	double y;
//	y=pow(x,2)+2*x+3;
//	y=-fabs(sin(3.1415926*(x-3))/3.1415926/(x-3));
	y=2*pow(x,2)-x-1;
	return y;
}

/////////////////////////////////////////////////
//传统的模拟退火算法

double CSA(double x1,double x2)
{
	ofstream outf("data.txt");//输出数据文件,便于matlab画图
	double init_temperature,total_numk,step_size;//定义初始温度，
	//...温度k时循环总次数，步长
	double x,xprevs,ReceivNum;//定义变量当前值，前一个值，内循环的接受数据数
	//初始化SA参数
	init_temperature=0.01;
	total_numk=1000;
	step_size=0.001;
	ReceivNum=50;
	x=(x2-x1)*randnum()+x1;//随机产生变量x
	int k=0;//温度下降次数控制变量
	double temperature_k=init_temperature;//定义第k次温度
	double best_x;

	//SA算法核心
	do
	{
		xprevs=x;//保留前一个变量值

		//以下三个参数用于估算接受概率
		int rec_num=0;//接受次数计数器
		double temp_i=0;//记录下面for循环的循环次数
		int temp_num=0;//记录fxi<fx的次数

        int i;
		for(i=1;i<total_numk&&(rec_num<ReceivNum);i++)
		{
			//产生满足要求的下一个数
			double xi;
			do
			{
				xi=x+(2*randnum()-1)*step_size;
			}
			while(xi<x1||xi>x2);

			double fxi=obfun(xi);
			double fx=obfun(x);
			if(fxi<fx)
			{best_x=xi;x=xi;rec_num++;temp_num++;}//函数值小的直接进入下次迭代
			else if(exp((fx-fxi)/temperature_k)>randnum())
			{	x=xi;rec_num++;}//以概率的形式接受使函数值变大的数
		}
		temp_i=i-1;
				outf<<x-xprevs<<"    "<<obfun(x)<<"    "<<temperature_k<<"    "
			<<(rec_num-temp_num)/(temp_i-temp_num)<<endl;
		k++;
		temperature_k=init_temperature/(k+1);//温度下降原则
	}
	while(k<5000||fabs(best_x-0.25)<0.001);
	outf<<flush;outf.close();//关闭文件
	return best_x;
}

int main()
{
	srand( (unsigned)time(NULL) );
	ofstream outf1("result.txt");
	double x1,x2;
	cout<<"请输入数据"<<endl;
	cin>>x1>>x2;
	double y;
	for(int i=0;i<20;i++)
	{
		y=CSA(x1,x2);
			cout<<"("<<y<<"  "<<obfun(y)<<")"<<endl;
			outf1<<y<<"  "<<obfun(y)<<endl;
	}
	outf1<<flush;outf1.close();//关闭文件
	getchar();
	return 1;
}
