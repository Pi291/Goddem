#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void* safe_malloc(size_t size) {
    void* ptr = malloc(size);
    if (ptr == NULL) {
        fprintf(stderr, "Ошибка выделения памяти\n");
        exit(EXIT_FAILURE);
    }
    return ptr;
}

void process_number(int num) {
    if (num == 0) {
        fprintf(stderr, "Ошибка, число равно нулю\n");
        return;
    }

    char* buffer = (char*)safe_malloc(100 * sizeof(char));
    if (snprintf(buffer, 100, "%d", num) < 0) {
        fprintf(stderr, "Ошибка формирования строки\n");
        free(buffer);
        return;
    }

    printf("Result: %s\n", buffer);
    free(buffer);
}

int main()
{
    process_number(42);
    process_number(0);
    process_number(-1);

    return 0;
}