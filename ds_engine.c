#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SIZE 100
#define STR_LEN 256

//STACK
typedef struct {
    char items[MAX_SIZE][STR_LEN];
    int top;
} Stack;

__declspec(dllexport) Stack* create_stack() {
    Stack* s = (Stack*)malloc(sizeof(Stack));
    s->top = -1;
    return s;
}

__declspec(dllexport) void push(Stack* s, const char* item) {
    if (s->top < MAX_SIZE - 1) {
        s->top++;
        strncpy(s->items[s->top], item, STR_LEN - 1);
        s->items[s->top][STR_LEN - 1] = '\0';
    }
}

__declspec(dllexport) const char* pop(Stack* s) {
    if (s->top >= 0) {
        return s->items[s->top--];
    }
    return "";
}

// --- QUEUE IMPLEMENTATION ---
typedef struct {
    char items[MAX_SIZE][STR_LEN];
    int front;
    int rear;
    int count;
} Queue;

__declspec(dllexport) Queue* create_queue() {
    Queue* q = (Queue*)malloc(sizeof(Queue));
    q->front = 0;
    q->rear = -1;
    q->count = 0;
    return q;
}

__declspec(dllexport) void enqueue(Queue* q, const char* item) {
    if (q->count < MAX_SIZE) {
        q->rear = (q->rear + 1) % MAX_SIZE;
        strncpy(q->items[q->rear], item, STR_LEN - 1);
        q->items[q->rear][STR_LEN - 1] = '\0';
        q->count++;
    }
}

__declspec(dllexport) const char* dequeue(Queue* q) {
    if (q->count > 0) {
        int idx = q->front;
        q->front = (q->front + 1) % MAX_SIZE;
        q->count--;
        return q->items[idx];
    }
    return "";
}

// --- LINKED LIST IMPLEMENTATION ---
typedef struct Node {
    char severity[32];
    char title[128];
    char endpoint[STR_LEN];
    struct Node* next;
} Node;

typedef struct {
    Node* head;
    Node* tail;
} VulnLinkedList;

__declspec(dllexport) VulnLinkedList* create_linked_list() {
    VulnLinkedList* list = (VulnLinkedList*)malloc(sizeof(VulnLinkedList));
    list->head = NULL;
    list->tail = NULL;
    return list;
}

__declspec(dllexport) void append_node(VulnLinkedList* list, const char* severity, const char* title, const char* endpoint) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    strncpy(newNode->severity, severity, sizeof(newNode->severity) - 1);
    strncpy(newNode->title, title, sizeof(newNode->title) - 1);
    strncpy(newNode->endpoint, endpoint, sizeof(newNode->endpoint) - 1);
    newNode->next = NULL;

    if (list->head == NULL) {
        list->head = newNode;
        list->tail = newNode;
    } else {
        list->tail->next = newNode;
        list->tail = newNode;
    }
}