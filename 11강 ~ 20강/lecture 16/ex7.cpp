#include<stdio.h>

// break �� ���ؼ� �ƶ���
// �ϴ±迡 continue ��

// break? : �ݺ��� �Ѱ��� ��������

int main() {
	for (int i = 1; ; i++) {
		int k;
		scanf_s("%d", &k);

		if (k == 0) {
			break;
		}

		printf("%d��°: %d\n", i, k);

	}
}