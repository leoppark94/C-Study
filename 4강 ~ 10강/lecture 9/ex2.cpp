// 체중과 키를 입력받아서 체질량 지수를 구하는 프로그램을 만들어 보세요

#include<stdio.h>

int main() {
	int weight;
	float height, bmi, temp;

	printf("체중을 입력하세요(kg) : ");
	scanf_s("%d", &weight);
	printf("키를 입력하세요(m) : ");
	scanf_s("%f", &height);

	temp = height * height;
	bmi = (float)weight / temp;

	printf("당신의 BMI는 %f 입니다.", bmi);
}