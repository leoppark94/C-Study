// 두 숫자를 입력받아서 그 숫자들의 합을 출력하는 프로그램을 만들어보세요.
#include<stdio.h>

int main() {
	float a, b, sum;

	printf("첫번째 숫자를 입력하세요 :");
	scanf_s("%f", &a, sizeof(float));
	
	printf("두번째 숫자를 입력하세요 :");
	scanf_s("%f", &b, sizeof(float));
	sum = a + b;

	printf("두 숫자의 합은 %.2f 입니다", sum);

}