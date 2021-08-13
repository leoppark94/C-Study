#include<stdio.h>
int itemCnt = 0;
int money = 100;

void buyItem() {
	itemCnt++;
	money -= 10;
	printf("아이템을 구매했습니다.\n");
	printf("아이탬 갯수 : %d\n", itemCnt);
	printf(" 잔액: %d\n", money);


}

int main() {
	buyItem();
	buyItem();

	printf("아이템갯수: %d, 남은금액: %d", itemCnt, money);
}