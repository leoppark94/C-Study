//변수에 대해서 더 자세히 아라보자

//변수의 연산

// 자료형

#include<stdio.h>

int main() {

	// int : 32bit 정수형 자료형
	int a = 5;
	int b = 3;

	int hap = a + b;
	int cha = a - b;
	int gop = a * b;
	int mok = a / b;
	int namuji = a % b;
	
	printf("%d + %d = %d\n", a, b, hap);
	printf("%d - %d = %d\n", a, b, cha);
	printf("%d * %d = %d\n", a, b, gop);
	printf("%d / %d = %d\n", a, b, mok);
	// 5 / 3 = 1 로 나옴
	// 소수를 지원하지 않기때문임
	printf("%d %% %d = %d\n\n\n\n\n", a, b, namuji);

	
	// 소수를 나타내는 변수를 아라보자
	float a1 = 9.8;
	float b1 = 3.14;

	float hap1 = a1 + b1;
	float cha1 = a1 - b1;
	float gop1 = a1 * b1;
	float mok1 = a1 / b1;

	printf("%f + %f = %f\n", a1, b1, hap1);
	printf("%f - %f = %f\n", a1, b1, cha1);
	printf("%f * %f = %f\n", a1, b1, gop1);
	printf("%f / %f = %f\n\n\n\n", a1, b1, mok1);


	// double을 알아보자
	// 64bit 실수를 담는데 사용됨
	// 부동소수점(floating point)
	double a2 = 9.8;
	double b2 = 3.14;

	double hap2 = a2 + b2;
	double cha2 = a2 - b2;
	double gop2 = a2 * b2;
	double mok2 = a2 / b2;

	printf("%f + %f = %f\n", a2, b2, hap2);
	printf("%f - %f = %f\n", a2, b2, cha2);
	printf("%f * %f = %f\n", a2, b2, gop2);
	printf("%f / %f = %f\n", a1, b2, mok2);

}