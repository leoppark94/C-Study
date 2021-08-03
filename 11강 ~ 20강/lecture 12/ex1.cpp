// C언어 if문

#include<stdio.h>
int main(void) {
	int n;
	scanf_s("%d", &n);

	if (n % 2 == 0) {
		printf("n은 짝수\n");
	}
	else {
		printf("n은 홀수");
	}
}