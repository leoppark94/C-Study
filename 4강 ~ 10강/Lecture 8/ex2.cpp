#include<stdio.h>

int main() {

	char a;

	scanf_s("%c", &a, sizeof(char));

	printf("당신이 입력한 숫자는 %d 입니다\n", a);
	printf("당신이 입력한 문자는 %c 입니다", a);

}