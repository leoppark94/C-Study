//define _CRT_SECURE_NO_WARNINGS �� ���� �Ǳ���
#include <stdio.h>

int main() {
	float a;
	//scanf �ȵ�
	// scanf_s �� ����ؾ���
	// ���� �ڿ� ������ �־���߉�(array������)(sizeof)Ȱ��
	scanf_s("%f", &a); //& �� ������ ����

	float hap = a + 5;

	printf("%f + 5 = %f\n", a, hap);
}