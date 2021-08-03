#include<stdio.h>

int main() {
	int n;

	do {
		printf("제발 0을 입력해주세요!!\n");
		scanf_s("%d", &n);
	} while (n != 0);

	printf("0이 입력되었군요!");
}