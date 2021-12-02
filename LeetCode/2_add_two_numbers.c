#include <stdlib.h>

struct ListNode {
    int val;
    struct ListNode *next;
};

struct ListNode * addTwoNumbers(struct ListNode* l1, struct ListNode* l2);

int main(void)
{
    struct ListNode * a1 = (struct ListNode *)malloc(sizeof(struct ListNode));
    struct ListNode * a2 = (struct ListNode *)malloc(sizeof(struct ListNode));
    struct ListNode * a3 = (struct ListNode *)malloc(sizeof(struct ListNode));
    a1->val = 2; a1->next = a2;
    a2->val = 4; a2->next = a3;
    a3->val = 3; a3->next = 0;

    struct ListNode * b1 = (struct ListNode *)malloc(sizeof(struct ListNode));
    struct ListNode * b2 = (struct ListNode *)malloc(sizeof(struct ListNode));
    struct ListNode * b3 = (struct ListNode *)malloc(sizeof(struct ListNode));
    b1->val = 5; b1->next = b2;
    b2->val = 6; b2->next = b3;
    b3->val = 4; b3->next = 0;

    struct ListNode * out = addTwoNumbers(a1, b1);
    return 0;
}

struct ListNode * addTwoNumbers(struct ListNode* l1, struct ListNode* l2)
{
    struct ListNode * root = (struct ListNode *)malloc(sizeof(struct ListNode));
    struct ListNode * current = root;
    struct ListNode * a = l1;
    struct ListNode * b = l2;
    int carry = 0;
    int carryOn = 0;
    
    // Loop until we iterated both linked lists and there is no carry value
    do
    {        
        carryOn = 0;
        current->val = 0;
        current->next = 0;
        
        // Do maths
        if(a != 0)
        {
            current->val += a->val;
            a = a->next;
        }
        if(b != 0)
        {
            current->val += b->val;
            b = b->next;
        }
        if(carry > 0)
        {
            current->val += carry;
            carry = 0;
        }
        
        if(current->val > 9)
        {
            carry      = current->val / 10;
            current->val = current->val - ((current->val / 10) * 10);
        }
        
        if(a != 0 || b != 0 || carry > 0)
        {
            struct ListNode * next = malloc(sizeof(struct ListNode));
        
            // Set the node in place
            current->next = next;
            current = next;
            carryOn = 1;
        }
    } while(carryOn);
    return root;
}