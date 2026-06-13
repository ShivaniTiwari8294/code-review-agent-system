#include <stdio.h> 
#include <stdlib.h> 
#define MAX 6
int stack[MAX];
int top=-1;

int push(int val){
    if(top==MAX-1){
        printf("Stack overflow!\n");
        return;
    }
    top++;
    stack[top]=val;
    printf("%d pushed to stack.",val);
}

int pop(){
    if(top==-1){
        printf("Stack underflow!\n");
        return -1;
    }
    int data=stack[top];
    top--;
    return data;

}

void traversal(){
    if(top==-1){
        printf("Stack is empty");
    }
    int temp=top;
    while(temp==-1){
        printf("%d",stack[temp]);
        temp--;
    }
}



int main()
{
    
    return 0;
}