// 1. ���������� �Է¹޾Ƽ�
// 2. 90�� ~ 100���̸� A
// 3. 80�� ~ 89���̸� B
// 4. 70�� ~ 79���̸� C
// 5. 60�� ~ 69���̸� D
// 6. 0�� ~ 59���̸� F

#include<stdio.h>

int main() {
	int score;
	printf("���������� �Է��ϼ��� : ");
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

