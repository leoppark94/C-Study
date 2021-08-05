//continue

#include <stdio.h>

int main() {
	int n;
	scanf_s("%d", &n);

	int sum = 0;

	// 1+2+4+5+7+8+10+11+13
	// 3의 배수는 뺴고 진행

	for (int i = 1; i <= n; i++) {
		if (i % 3 == 0) {
			continue;
		}
		sum += i;
	}
	printf("%d", sum);
}