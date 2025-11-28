/* example.c - Simple C library implementation for SWIG demonstration */
#include "example.h"

int add(int a, int b) {
    return a + b;
}

double multiply(double a, double b) {
    return a * b;
}

int factorial(int n) {
    if (n < 0) {
        return -1;  /* Error: undefined for negative numbers */
    }
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
    /* Iterative approach for O(n) time complexity */
    int a = 0, b = 1, temp;
    for (int i = 2; i <= n; i++) {
        temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}
