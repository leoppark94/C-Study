// 변수에 관하여 알아보자

#include<stdio.h>

int main() {
	// int 는 32bit, 4byte
	int a; // 선언
	
	// a 에다가 3을 집어넣어버리겠다
	a = 3; // 대입
	printf("%d\n", a);

	// 3이라는 a의 값을 날려버리고 5를 넣어버리게따
	a = 5; // 대입
	printf("%d", a);
}