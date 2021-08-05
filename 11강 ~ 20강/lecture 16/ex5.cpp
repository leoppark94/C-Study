#include<stdio.h>

int main() {
	int i;

	scanf_s("%d", &i);

	for (; ; i++) {
		printf("%d\n", i);
	}
}