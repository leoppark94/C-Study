#include<stdio.h>

int main() {
	int n;
	scanf_s("%d", &n);

	if (n > 0) {
		printf("n�� ���");
	}
	else if (n == 0) {
		printf("n�� 0\n");
	}
	else {
		printf("n�� ����\n");
	}

}