#include <stdio.h> 
#include <stdlib.h>

struct node
{
    int data;
    struct node *next;  
};

struct node *head=NULL;

void append(int data){
    struct node* new=(struct node*)malloc(sizeof(struct node));
    new->data=data;
    new->next=NULL;

    if(head==NULL){
        head=new;
        return;
    }
    else{
        struct node* temp=head;
        while(temp->next != NULL){
            temp=temp->next;
            printf("%d",(*temp).data);
        }
        temp->next=new;
    }
}

void atbegin(int data){
    struct node *n=(struct node*)malloc(sizeof(struct node));
    n->data=data;
    n->next=head;
    head=n;
}

void pop(){
    if(head==NULL){
        printf("Linked list is empty\n");
        return;
    }
    struct node* temp=head;
    head=head->next;
    free(temp);
}

void removeend(){
    if(head==NULL){
        printf("Linked list is empty\n");
        return;
    }
    if(head->next==NULL){
        free(head);
        head=NULL;
        return;
    }
    struct node* temp=head;
    while(temp->next->next!=NULL){
        temp=temp->next;
    }
    free(temp->next);
    temp->next=NULL;
}

void display(){
    struct node* temp=head;
    if (head==NULL)
    {
        printf("Linked list is empty\n");
        return;
    }
    
    printf("Linked list elements: ");
    while(temp!=NULL){
        printf("%d ",temp->data);
        temp=temp->next;
    }
}

int main()
{
    append(23);
    append(34);
    append(45);
    display();

    printf("\n");
    printf("First element: %d", head->next->next->data);
    return 0;
}