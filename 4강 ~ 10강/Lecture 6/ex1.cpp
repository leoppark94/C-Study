#include<stdio.h>

int main() {
	//sizeof 연산자?
	//sizeof(x): x의 크기를 알려줌
	//x 에는 형의 이름이 들어갈수 있음(int, float이런거)
	//x 에는 변수의 이름이 들어갈수 있음(a)

	printf("%d %d %d %d\n", sizeof(int), sizeof(char), sizeof(float), sizeof(double));

	int a; char b; float c; double d;
	printf("%d %d %d %d\n", sizeof(a), sizeof(b), sizeof(c), sizeof(d));

}