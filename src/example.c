/* example.c - Simple C library implementation for SWIG demonstration */
#include "example.h"

int add(int a, int b) {
    return a + b;
}

double multiply(double a, double b) {
    return a * b;
}

int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int fibonacci(int n) {
    if (n <= 0) {
        return 0;
    }
    if (n == 1) {
        return 1;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}
