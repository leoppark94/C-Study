// �� ���ڸ� �Է¹޾Ƽ� �� ���ڵ��� ���� ����ϴ� ���α׷��� ��������.
#include<stdio.h>

int main() {
	float a, b, sum;

	printf("ù��° ���ڸ� �Է��ϼ��� :");
	scanf_s("%f", &a, sizeof(float));
	
	printf("�ι�° ���ڸ� �Է��ϼ��� :");
	scanf_s("%f", &b, sizeof(float));
	sum = a + b;

	printf("�� ������ ���� %.2f �Դϴ�", sum);

}