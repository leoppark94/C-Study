#include<stdio.h>
#include<string.h>

int main() {
	char str1[100] = "Hello";
	char str2[1000];

	strcpy_s(str2, str1);

	printf("%s", str2);
}