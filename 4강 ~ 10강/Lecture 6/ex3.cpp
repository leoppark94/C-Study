// ����ȯ? �װ� ���� �Դ°ǰ�?

#include<stdio.h>

int main() {
	int math = 90, korean = 95, english = 96;
	int sum = math + korean + english;
	double avg = (double)sum / 3; // sum�� ���������� double�� �ǵ�
	
	printf("%f\n", avg); // 93.6666667 �̷��� ���;��ϴµ�... 93.00000 �̷��� ����

	// ���� / ���� = ���� �̱� ������ �׷�����
	// �Ǽ� / ���� = �Ǽ�
	// ���� / �Ǽ�  >>> �������ƾ�
	// �Ǽ� / �Ǽ� = �Ǽ�

}