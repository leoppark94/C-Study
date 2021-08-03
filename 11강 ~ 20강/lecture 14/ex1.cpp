// switch 문은 if문을 완전히 대체할 수 있음

#include<stdio.h>

int main() {
	int choice;

	printf("새 게임 : 1\n");
	printf("불러오기 : 2\n");
	printf("설 정 : 3\n");
	printf("크레딧 : 4\n");
	printf("값을 입력하세요 :");

	
	scanf_s("%d", &choice);

	if (choice == 1) {
		printf("새로운 게임이 시작되어따");
	}
	else if (choice == 2) {
		printf("새로운 게임을 불러오는중?");
	}
	else if (choice == 3) {
		printf("설정....");
	}
	else if (choice == 4) {
		printf("크레딧...레오");
	}
	else {
		printf("필요한거만 입력하라고!");

	}
}