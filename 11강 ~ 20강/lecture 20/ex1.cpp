#include<stdio.h>

int main() {

	int a[] = { 1,2,3,4,5,6,7,8 };
	for (int i = 0; i < sizeof(a) / sizeof(int); i++) {
		printf("%d", a[i]);
	}
}