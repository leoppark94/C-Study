// switch ���� if���� ������ ��ü�� �� ����

#include<stdio.h>

int main() {
	int choice;

	printf("�� ���� : 1\n");
	printf("�ҷ����� : 2\n");
	printf("�� �� : 3\n");
	printf("ũ���� : 4\n");
	printf("���� �Է��ϼ��� :");

	
	scanf_s("%d", &choice);

	if (choice == 1) {
		printf("���ο� ������ ���۵Ǿ��");
	}
	else if (choice == 2) {
		printf("���ο� ������ �ҷ�������?");
	}
	else if (choice == 3) {
		printf("����....");
	}
	else if (choice == 4) {
		printf("ũ����...����");
	}
	else {
		printf("�ʿ��ѰŸ� �Է��϶��!");

	}
}