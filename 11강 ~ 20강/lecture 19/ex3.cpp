// ���� �ڸ����� 3�� ����ΰ�� *�� ���

#include <stdio.h>
int main() {
	int number;
	printf("369�� �ִ� ���ڸ� �Է��ϼ��� :");
	scanf_s("%d", &number);


	for (int i = 1; i <= number; i++) {
		int k = i % 10;
		if (k == 3) {
			printf("*\n");
		}
		else if (k == 6) {
			printf("*\n");
		}
		else if (k == 9) {
			printf("*\n");
		}
		else {
			printf("%d\n", i);
		}
	}
}
