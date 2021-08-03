#include<stdio.h>

int main() {
	int a, b;
	scanf_s("%d%d", &a, &b);

	bool p = a > b;
	bool q = a < b;
	bool r = a == b;

	printf("%d\n", p);
	printf("%d\n", q);
	printf("%d\n", r);
}