#include<stdio.h>

int main() {

	int n;
	int arr[100];

	scanf_s("%d", &n);
	for (int i = 0; i < n; i++){
		scanf_s("%d", &arr[i]);
	}

	int max = arr[0];
	for (int i = 1; i < n; i++) {
		if (max < arr[i]) max = arr[i];
	}

	printf("%d", max);
}