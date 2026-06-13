// bubble sort

#include <stdio.h> 

void bubbleSort(int arr[], int n){
    int i, j, temp;
    for (i = 0; i < n-1; i++){
        for (j = 0; j < n-i-1; j++){
            if (arr[j] > arr[j+1]){
                temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
}

void insertionSort(int arr[], int n){
    int i, key, j;
    for (i = 1; i < n; i++){
        key = arr[i];
        for ( j = i-1; j >= 0 && arr[j] > key; j--)
        {
            arr[j + 1] = arr[j];
        }
        
        arr[j + 1] = key;
    }
}

void selectionSort(int arr[], int n){
    int i, j, min_idx, temp;
    for (i = 0; i < n-1; i++){
        min_idx = i;
        for (j = i+1; j < n; j++)
            if (arr[j] < arr[min_idx]) 
                min_idx = j;
        temp = arr[min_idx];
        arr[min_idx] = arr[i];
        arr[i] = temp;
    }
}

int main(){
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    int arr2[] = {12, 11, 13, 5, 6};
    int arr3[] = {64, 25, 12, 22, 11};

    int n = sizeof(arr)/sizeof(arr[0]);
    int n2 = sizeof(arr2)/sizeof(arr2[0]);
    int n3 = sizeof(arr3)/sizeof(arr3[0]);


    bubbleSort(arr, n);
    printf("Sorted array using bubble sort: \n");
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");

    insertionSort(arr2, n2);
    printf("Sorted array using insertion sort: \n");
    for (int i = 0; i < n2; i++)
        printf("%d ", arr2[i]); 
    printf("\n");

    selectionSort(arr3, n3);
    printf("Sorted array using selection sort: \n");
    for (int i = 0; i < n3; i++)
        printf("%d ", arr3[i]);
    
    return 0;
}