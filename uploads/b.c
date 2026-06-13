#include <stdio.h> 

int binarySearch(int arr[],int n,int key){
    int l=0;
    int h=n-1;
    while(l<=h){
        int mid=(h+l)/2;
        if (arr[mid]==key)
        {
            return mid;
        }
        else if (arr[mid]>key)
        {
            h=mid-1;
        }
        else{
            l=mid+1;
        }
    }
    return -1;
}

int main()
{
    int arr[] = {2,4,7,9,11,12,33,44,56,78,92};
    int n=sizeof(arr)/sizeof(arr[0]);
    int result=binarySearch(arr,n,4);
    printf("%d",result+1);
    return 0;
}