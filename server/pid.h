#ifndef PID_H
#define PID_H

#include <stdlib.h>

/* struct for PID contoller*/
struct structPid
{
	/* PID parameters */
	struct
	{
		float kc; // Proportional gain
		int ts; // Timestep
		float ti; // Integrator time constant
		float td; // Derivative time constant
		float pmin; // Minimum power limit (W)
		float pmax; // Maximum power limit (W)
	} params;
	float k0; // (Kc*Ts/Ti)
	float k1; // (Kc*Td/Ts)
	float xk_1; // Temperature at k-1
	float xk_2; // Temperature at k-2
	float yk; // Output variable
	float pp;
	float pi;
	float pd;
	float setp; // Setpoint
};

/* Type definition */
typedef struct structPid Pid;

/* Constructor and destructor */
Pid* pidConstruct(const float kc, const int ts, const float ti, const float td, const float pmin, const float pmax, const float setp);
void pidDestruct(Pid *pid);

/* Functions */
float pidTick(Pid *pid, const float xk);
void pidSetSetpoint(Pid *pid, const float setp);
float pidGetSetpoint(Pid *pid);

#endif