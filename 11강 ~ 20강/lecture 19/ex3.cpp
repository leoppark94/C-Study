// 일의 자릿수가 3의 배수인경우 *을 출력

#include <stdio.h>
int main() {
	int number;
	printf("369의 최대 숫자를 입력하세요 :");
	scanf_s("%d", &number);


	for (int i = 1; i <= number; i++) {
		int k = i % 10;
		if (k == 3) {
			printf("*\n");
		}
		else if (k == 6) {
			printf("*\n");
		}
		else if (k == 9) {
			printf("*\n");
		}
		else {
			printf("%d\n", i);
		}
	}
}
