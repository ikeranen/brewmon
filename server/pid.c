#include <stdlib.h>
#include "pid.h"

/* Constructor */
Pid *pidConstruct(const float kc, const int ts, const float ti, const float td, const float pmin, const float pmax, const float setp)
{
	Pid *nPid = malloc(sizeof(Pid));
	nPid->params.kc = kc;
	nPid->params.ts = ts;
	nPid->params.ti = ti;
	nPid->params.td = td;
	nPid->params.pmin = pmin;
	nPid->params.pmax = pmax;
	nPid->k0 = (kc*ts)/ti;
	nPid->k1 = (kc*td)/ts;
	nPid->xk_1 = 20;
	nPid->xk_2 = 20;
	nPid->yk = 0;
	nPid->setp = setp;
	return nPid;
}

/* Destructor */
void pidDestruct(Pid *pid)
{
	free(pid);
}

/* Functions */
float pidTick(Pid *pid, const float xk)
{
	pid->pp = pid->params.kc * (pid->xk_1 - xk);
	pid->pi = pid->k0 * (pid->setp - xk);
	pid->pd = pid->k1 * (2.0 * pid->xk_1 - xk - pid->xk_2);
	pid->yk += pid->pp + pid->pi + pid->pd;
	if (pid->yk > pid->params.pmax)
	{
		pid->yk = pid->params.pmax;
	} else if (pid->yk < pid->params.pmin)
	{
		pid->yk = pid->params.pmin;
	}
	pid->xk_2 = pid->xk_1;
	pid->xk_1 = xk;
	return pid->yk/pid->params.pmax;
}

void pidSetSetpoint(Pid *pid, const float setp)
{
	pid->setp = setp;
}

float pidGetSetpoint(Pid *pid)
{
	return pid->setp;
}
