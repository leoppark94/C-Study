#include<stdio.h>

int main() {
	
	
	int choice;
	makeChoice:
	printf("�� ���� : 1\n");
	printf("�ҷ����� : 2\n");
	printf("�� �� : 3\n");
	printf("ũ���� : 4\n");
	printf("���� �Է��ϼ��� :");


	scanf_s("%d", &choice);

	switch (choice) {
	case 1:
		printf("������");
		break;
	case 2:
		printf("�ҷ�����");
		break;
	case 3:
		printf("�� ��");
		break;
	case 4:
		printf("ũ����");
		break;
	default:
		printf("�ٸ����� �Է��ϼ���\n");
		goto makeChoice;
		break;
	}
}