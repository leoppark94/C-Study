// 자연수를 입력받고
// 해당 숫자의 약수를 출력
// ex) 12를 넣으면. 1,2,3,4,6,12

#include<stdio.h>

int main() {
	int number;
	printf("약수를 구할 숫자를 넣어주세요 : ");
	scanf_s("%d", &number);

	for (int i = 1; i <= number; i++) {
		if (number % i == 0) {
			printf("%d,", i);
		}
	}
}