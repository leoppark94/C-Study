// �ڿ����� �Է¹ް�
// �ش� ������ ����� ���
// ex) 12�� ������. 1,2,3,4,6,12

#include<stdio.h>

int main() {
	int number;
	printf("����� ���� ���ڸ� �־��ּ��� : ");
	scanf_s("%d", &number);

	for (int i = 1; i <= number; i++) {
		if (number % i == 0) {
			printf("%d,", i);
		}
	}
}