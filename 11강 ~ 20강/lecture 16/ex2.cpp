#include<stdio.h>

int main() {

	int  n;
	scanf_s("%d", &n);

	// �߰�ȣ �ȿ� ������ ���������� ħ ����
	for (int i = 1; i <= n; i*=2) {
		printf("%d\n", i);
	}

}