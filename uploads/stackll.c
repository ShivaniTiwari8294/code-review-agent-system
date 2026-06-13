#include <stdio.h> 
#include <stdlib.h>

struct node
{
    int data;
    struct node* next;
};

struct node * head=NULL;

void push(int data){
    struct node *new=(struct node *)malloc(sizeof(struct node));

    if(new == NULL){
        printf("Stack overflow\n");
        return;
    }
    new->data=data;
    new->next=head;
    head=new;
}

void pop(){
    if (head==NULL)
    {
        printf("Stack underflow.\n");
        return;
    }
    struct node *temp=head;
    head=head->next;
    printf("%d popped from stack.\n",temp->data);
    free(temp);
    
}

void traverse(){
    if(head==NULL){
        printf("Stack Empty\n");
    }
    struct node* temp= head;

    printf("Stack elements: ");
    while (temp!=NULL)
    {
        printf("%d \t",temp->data);
        temp=temp->next;
    }
    printf("\n");
}

int main()
{
    push(45);
    push(46);
    push(6);
    traverse();
    pop();

    return 0;
}