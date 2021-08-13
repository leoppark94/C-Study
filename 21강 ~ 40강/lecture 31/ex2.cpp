#include<stdio.h>

int plus(int a, int b) {
	return a + b;
}

int main() {
	int sum = plus(3, 5);

	printf("%d", sum);
}