#include <stdio.h>
#include <stdlib.h>

#define COUNT 16

int compiled_dance(int spin, char *programs);

int main() {
    int spin = 0;
    char *programs = malloc(COUNT + 1);
    for (int i = 0; i < COUNT; i++) {
        programs[i] = 'a' + i;
    }
    programs[COUNT] = '\0';

    for (int i = 0; i < 100000; i++) {
        spin = compiled_dance(spin, programs);
    }

    printf("%s", programs + (COUNT - spin));
    programs[COUNT - spin] = '\0';
    printf("%s\n", programs);
    return 0;
}
