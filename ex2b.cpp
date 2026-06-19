#include <iostream>
#include <cstdlib>
#include <cstring>

typedef struct {
    int* data;
    int size;
    int capacity;
} Vec;

Vec* vec_new(int capacity) {
    // В C++ нужно явно приводить (Vec*)
    Vec* v = (Vec*)malloc(sizeof(Vec));
    v->data = (int*)malloc(capacity * sizeof(int));
    v->size = 0;
    v->capacity = capacity;
    return v;
}

void vec_push(Vec* v, int value) {
    if (v->size == v->capacity) {
        v->capacity *= 2;
        // В C++ нужно явно приводить (int*)
        int* new_data = (int*)malloc(v->capacity * sizeof(int));
        memcpy(new_data, v->data, v->size * sizeof(int));
        free(v->data);
        v->data = new_data;
    }
    v->data[v->size++] = value;
}

void vec_free(Vec* v) {
    free(v->data);
    free(v);
}

int main() {
    Vec* scores = vec_new(2);
    vec_push(scores, 85);
    vec_push(scores, 92);

    // Вместо указателя используем индекс, чтобы избежать ошибки
    int top_score_idx = 1;

    vec_push(scores, 78);
    vec_push(scores, 95);
    vec_push(scores, 61);

    std::cout << "Top score was: " << scores->data[top_score_idx] << std::endl;

    vec_free(scores);
    return 0;
}