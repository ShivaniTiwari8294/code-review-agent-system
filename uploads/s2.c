// merge sort
// 1.divide in half
// 2.Sort left half and right half 
// 3.merge both sorted array

#include <stdio.h> 

void mergeSort(int arr[],int l, int r){
    if(l<r){
        int m=l+r/2;
        mergeSort(arr,l,m);  //left half
        mergeSort(arr,m+1,r);  //right half

        merge(arr,l,m,r); //combine
    }
}

void merge(int arr[],int l,int m,int r){
    int i,j,k;
    // create temp array n1 and n2 are size of left and right sub array
    int n1=m-l+1;
    int n2=r-m;

    // create temp array
    int L[n1],R[n2];

    // copy data to temp array
    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    i=0;
    j=0;
    k=l;

    // merge the temp arrays back into arr[l..r]
    while(i<n1 && j<n2){
        if (L[i]<=R[j])
        {
            arr[k]=L[i];
            i++;
        }
        else{
            arr[k]=R[j];
            j++;
        }
        k++;
    }

    // copy remaining element of L[] if any
    while(i<n1){
        arr[k]=L[i];
        i++;
        k++;
    }

    while(j<n2){
        arr[k]=R[j];
        j++;
        k++;
    }
}

int main()
{
    int arr[] = {34, 32, 32, 11, 12, 4, 5, 98};
    int n = sizeof(arr) / sizeof(arr[0]);
    mergeSort(arr,0,n-1);
    for (int i = 0; i < n; i++)
    {
        printf("%d ",arr[i]);
    }
    
    return 0;
}
