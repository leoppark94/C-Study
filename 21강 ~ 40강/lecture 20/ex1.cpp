#include <stdio.h>

int main(){
	int a = 20;
	int *ptr_a;

	ptr_a = &a;

	printf("a의 값 : %d\n", a);
	printf("a의 주솟값 : %d\n", &a);
	printf("ptr_a 에 저장된 값 : %d\n", ptr_a);
	printf("ptr_a 가 가리키는 변수의 값 : %d\n", *ptr_a);

}