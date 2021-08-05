// 1. 시험점수를 입력받아서
// 2. 90점 ~ 100점이면 A
// 3. 80점 ~ 89점이면 B
// 4. 70점 ~ 79점이면 C
// 5. 60점 ~ 69점이면 D
// 6. 0점 ~ 59점이면 F

#include<stdio.h>

int main() {
	int score;
	printf("시험점수를 입력하세요 : ");
	scanf_s("%d", &score);

	if (score >= 90 && score <= 100) {
		printf("A");
	}
	else if (score >= 80) {
		printf("B");
	}
	else if (score >= 70) {
		printf("C");
	}
	else if (score >= 60) {
		printf("D");
	}
	else {
		printf("F");
	}

}

