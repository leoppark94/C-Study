#include<stdio.h>

// break 에 대해서 아라보자
// 하는김에 continue 도

// break? : 반복문 한개를 빠져나옴

int main() {
	for (int i = 1; ; i++) {
		int k;
		scanf_s("%d", &k);

		if (k == 0) {
			break;
		}

		printf("%d번째: %d\n", i, k);

	}
}