#include <stdlib.h>
#include <Python.h>
#include "pid.h"

Pid *pid;

static PyObject* init_pid(PyObject* self, PyObject* args)
{
	const float kc;
	const int ts;
	const float ti;
	const float td;
	const float pmin;
	const float pmax;
	const float setp;
	
	if (!PyArg_ParseTuple(args, "fifffff", &kc, &ts, &ti, &td, &pmin, &pmax, &setp))
        return NULL;
 
	pid = pidConstruct(kc, ts, ti, td, pmin, pmax, setp);

    Py_RETURN_NONE;
}

static PyObject* free_pid(PyObject* self, PyObject* args)
{
	pidDestruct(pid);
	Py_RETURN_NONE;
} 

static PyObject* tick(PyObject* self, PyObject* args)
{
	const float xk;
	
	if (!PyArg_ParseTuple(args, "f", &xk))
		return NULL;
	
	return Py_BuildValue("f",pidTick(pid, xk));
}

static PyObject* set_setp(PyObject* self, PyObject* args)
{
	const float setp;
	
	if (!PyArg_ParseTuple(args, "f", &setp))
		return NULL;
		
	pidSetSetpoint(pid, setp);
	Py_RETURN_NONE;
}

static PyObject* get_setp(PyObject* self, PyObject* args)
{
	return Py_BuildValue("f",pidGetSetpoint(pid));
}

static PyMethodDef PidMethods[] =
{
     {"init_pid", init_pid, METH_VARARGS, "Initialize PID controller."},
	 {"free_pid", free_pid, METH_VARARGS, "Destruct PID controller"},
	 {"tick", tick, METH_VARARGS, "Update PID controller"},
	 {"set_setp", set_setp, METH_VARARGS, "Set PID setpoint"},
	 {"get_setp", get_setp, METH_VARARGS, "Get PID setpoint"},
     {NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC initpid(void)
{
     (void) Py_InitModule("pid", PidMethods);
}