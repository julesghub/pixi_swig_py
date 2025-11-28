/* example.i - SWIG interface file for Python bindings */
%module example

%{
#include "example.h"
%}

/* Include the header file to generate wrappers for all functions */
%include "example.h"
