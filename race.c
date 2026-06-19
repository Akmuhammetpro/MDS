#include <stdio.h>
#include <pthread.h>
#include <stdatomic.h> // Это критически важно для C11

atomic_int counter = 0; // Использование типа atomic_int

void* increment(void* arg) {
    for(int i = 0; i < 1000000; i++) {
        atomic_fetch_add(&counter, 1); // Атомарное прибавление
    }
    return NULL;
}

int main() {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, increment, NULL);
    pthread_create(&t2, NULL, increment, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    printf("Final counter: %d\n", counter);
    return 0;
}