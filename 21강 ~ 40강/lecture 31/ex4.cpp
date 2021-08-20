#include<stdio.h>

int main() {
	int a, b, temp;

	scanf_s("%d%d", &a, &b);
	temp = b;
	a = b;
	b = a;
}