#include <stdio.h>

int main() {
	// %d : 정수를 출력
	printf("%d + %d = %d\n", 2, 3, 5);

	// %f : 실수를 출력(소수점)
	printf("%f\n", 3.14);
	
	// %.2f : 두자리 소수점까지만 출력
	printf("%.2f\n", 3.141592);

	// %g : 실수출력(지수형태로도 출력됨 - 기다란 숫자)
	printf("%g\n", 3.141592);
	
	// %.3g  : 3자리 이후부터는 지수형태로 치환
	printf("%.3g\n", 847231345.13209454932348);

	// %c : 문자 출력 ( 알파벳, 숫자, 몇몇 기호, \n) - 한글, 한자, 유니코드 안됌
	printf("%c %c %c\n", 'a', 'b', 'c');

	// %s : 문자열 출력 (한글도 출력가능)
	printf("%s\n", "안녕하세요");

	//문자열을 표현하기 위해서는 "" 이고, 문자는 '' 를 사용함
	printf("%s\n", "안녕하세요2");
}