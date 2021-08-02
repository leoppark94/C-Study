// 형변환? 그게 뭐야 먹는건가?

#include<stdio.h>

int main() {
	int math = 90, korean = 95, english = 96;
	int sum = math + korean + english;
	double avg = (double)sum / 3; // sum을 순간적으로 double로 맨듬
	
	printf("%f\n", avg); // 93.6666667 이렇게 나와야하는데... 93.00000 이렇게 나옴

	// 정수 / 정수 = 정수 이기 때문에 그런거임
	// 실수 / 정수 = 실수
	// 정수 / 실수  >>> 하지마아아
	// 실수 / 실수 = 실수

}