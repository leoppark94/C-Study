#include<stdio.h>

int main() {
	
	
	int choice;
	makeChoice:
	printf("새 게임 : 1\n");
	printf("불러오기 : 2\n");
	printf("설 정 : 3\n");
	printf("크레딧 : 4\n");
	printf("값을 입력하세요 :");


	scanf_s("%d", &choice);

	switch (choice) {
	case 1:
		printf("새게임");
		break;
	case 2:
		printf("불러오기");
		break;
	case 3:
		printf("설 정");
		break;
	case 4:
		printf("크레딧");
		break;
	default:
		printf("다른값을 입력하세요\n");
		goto makeChoice;
		break;
	}
}