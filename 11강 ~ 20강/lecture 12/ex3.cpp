//중첩 if문
//중괄호 코딩 스타일

#include <stdio.h>
int main() {
	int a, b, c;

	printf("3개의 숫자를입력하시오 : ");
	scanf_s("%d%d%d", &a, &b, &c);

	if (a > b) {
		// a > b > c
		if (b > c) {

		}
		// a > c > b
		if (c > b) {

		}
		// c > a > b
		if (c > a) {

		}
	}
}