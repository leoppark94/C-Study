// ü�߰� Ű�� �Է¹޾Ƽ� ü���� ������ ���ϴ� ���α׷��� ����� ������

#include<stdio.h>

int main() {
	int weight;
	float height, bmi, temp;

	printf("ü���� �Է��ϼ���(kg) : ");
	scanf_s("%d", &weight);
	printf("Ű�� �Է��ϼ���(m) : ");
	scanf_s("%f", &height);

	temp = height * height;
	bmi = (float)weight / temp;

	printf("����� BMI�� %f �Դϴ�.", bmi);
}