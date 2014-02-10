#define LOCAL
#define DEBUG

#include <vector>
#include <list>
#include <map>
#include <set>
#include <queue>
#include <deque>
#include <stack>
#include <bitset>
#include <algorithm>
#include <iostream>
#include <iomanip>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <cstring>

using namespace std;
#ifdef DEBUG
#define cvar(x) cerr << "<" << #x << ": " << x << ">"
#define evar(x) cvar (x) << endl
#define debug(...) printf( __VA_ARGS__) 
template<class T> void DISP(const char *s, T x, int n) {cerr << "[" << s << ": "; for (int i = 0; i < n; ++i) cerr << x[i] << " "; cerr << "]" << endl;}
#define disp(x,n) DISP(#x " to " #n, x, n)
#else
#define debug(...) 
#define cvar(...) ({})
#define evar(...) ({})
#define disp(...) ({})
#endif

#define FILL(x) memset(x, 0, sizeof(x));

template<class T> inline T cub(T a){return a*a*a;}
template <typename T> T gcd(T x, T y) {for (T t; x; t = x, x = y % x, y = t); return y; }
typedef long long int64;


const int INF = 0x3f3f3f3f;
const int M = 110000;
const int MOD = int(1e9) + 7;
const double EPS = 1E-9;
const int TIMES = 10;
const int lens = 10; 
double pb = 0.94, p0 = 0.5, pd = 0.1, ts =7, vmax = 20, gap_safe = 7, lenmax = 20;
int road_len = 100;
class C {
    public: double v[TIMES], x[TIMES], b[TIMES];
        double curx; int curt, id;
        double d, deff, t;
        C() {
            memset(v, 0, sizeof(v));
            memset(x, 0, sizeof(x));
            memset(b, 0, sizeof(b));
            curx = 0;
            curt = 0;
            d = deff = gap_safe;
            t = ts;
        }
};

bool outborder(const C& tmp) {
    double ans = tmp.x[tmp.curt-1];
    return (ans > lenmax);
}
int main() {
#ifdef LOCAL 
    freopen("data.in","r",stdin);  
    //freopen("data.out", "w", stdout):
#endif
    list<C> lis;
    srand(time(NULL));
    for (int T=0; T<TIMES; T++) {
        C tmp;
        tmp.curt = 0;
        tmp.id = T;
        double r = ((double) rand() / (RAND_MAX));
        double tmpv = r * vmax;
        tmp.v[tmp.curt] = tmpv;
        cout<<tmpv<<endl;
        lis.push_back(tmp);
        //update 
        for (std::list<C>::iterator it = lis.begin(); it != lis.end(); it++) {
            int cur = (*it).curt;
            // update x
            if (cur == 0) (*it).x[0] = (*it).v[cur];
            else (*it).x[cur] = (*it).x[cur-1] + (*it).v[cur];
            // update v
            if (cur == 0) (*it).v[1] = (*it).v[0];
            else (*it).v[cur+1] = (*it).v[cur];
            (*it).curt++;

        }
        
        //delete outborder
        lis.remove_if(outborder);
        // print tmp
        for (std::list<C>::iterator it = lis.begin(); it != lis.end(); it++){
            int cur = (*it).curt-1;
            printf("(%d, %d, %f, %f) ", (*it).id, (*it).v[cur], (*it).curt, (*it).x[(*it).curt-1]);
        }
        printf("\n");
    }

}
