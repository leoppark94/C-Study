// char: 1바이트 정수형을 가지고있음
// character : 문자(반각문자 ABCabc12378_+\#% 이런 다양한 키호들
// 해당이 안되는거 - 한자 , 일본어, 러시아어 이런거
#include <stdio.h>

int main() {
	char a = 65;

	printf("%d\n", a);
	printf("%c\n", 'F');
	printf("%c\n", a); //A가 나옴
	printf("%d\n", 'A'); // 65가 나옴
	// ASCII 문자와 숫자가 대응됨


}