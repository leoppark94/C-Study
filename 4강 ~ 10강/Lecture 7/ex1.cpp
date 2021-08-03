//define _CRT_SECURE_NO_WARNINGS 를 쓰면 되긴함
#include <stdio.h>

int main() {
	float a;
	//scanf 안됨
	// scanf_s 를 사용해야함
	// 인자 뒤에 사이즈 넣어줘야됌(array사이즈)(sizeof)활용
	scanf_s("%f", &a); //& 는 포인터 개념

	float hap = a + 5;

	printf("%f + 5 = %f\n", a, hap);
}