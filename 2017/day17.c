#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct entry {
    int value;
    struct entry* next;
} entry;

entry* new_entry(entry *buffer, int value, entry *next) {
    entry *e = buffer + value;
    e->value = value;
    e->next = next;
    return e;
}

entry *spinlock(entry *buffer, int step_size, int cycles) {
    entry *head = new_entry(buffer, 0, NULL);
    head->next = head;

    entry *prev = NULL;
    entry *pos = head;

    for (int i = 0; i < cycles; i++) {
        for (int j = 0; j < step_size; j++) {
            prev = pos;
            pos = pos->next;
        }

        entry *e = new_entry(buffer, i + 1, pos);
        prev->next = e;
    }

    return head;
}

int main() {
    int step_size = 355;
    int cycles = 50000000;
    entry *buffer = malloc(sizeof(entry) * (cycles + 1));
    entry *head = spinlock(buffer, step_size, cycles);
    printf("%d\n", head->value);
    printf("%d\n", head->next->value);
}
