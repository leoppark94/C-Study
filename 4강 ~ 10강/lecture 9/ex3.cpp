// ���ĺ��� �Է¹޾Ƽ� �� ���� ���ĺ��� ����ϴ� ���α׷��� �����ÿ�

#include<stdio.h>

int main() {
	char a;
	printf("���ĺ��� �Է��ϼ��� :");
	scanf_s("%c", &a, sizeof(char));
	printf("%c �� ���� ���ĺ��� %c �Դϴ�", a, a + 1);
}