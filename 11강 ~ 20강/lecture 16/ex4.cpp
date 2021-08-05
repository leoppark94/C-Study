#include <stdio.h>
// for¹® ¿¬½À
int main() {
	int n;
	scanf_s("%d", &n);

	for (int i = 1; i <= n; i++) {
		printf("\n");
		for (int j = 1; j <= i; j++) {
			printf("*");
		}
	}

}