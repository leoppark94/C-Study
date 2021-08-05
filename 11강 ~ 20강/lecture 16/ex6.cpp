#include <stdio.h>

int main() {

	int n;
	scanf_s("%d", &n);

	for (int i = 0, t = 1; i <= n; i++,t *= 2) {
		printf("2^%d = %d\n", i, t);
		}
}