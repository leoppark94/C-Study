#include<stdio.h>


int main() {
	char s[100];

	scanf_s("%s", s, sizeof(s));

	printf("%s\n", s);
}