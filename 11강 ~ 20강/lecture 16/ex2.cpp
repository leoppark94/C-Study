#include<stdio.h>

int main() {

	int  n;
	scanf_s("%d", &n);

	// 중괄호 안에 있으면 지역변수로 침 ㅇㅋ
	for (int i = 1; i <= n; i*=2) {
		printf("%d\n", i);
	}

}