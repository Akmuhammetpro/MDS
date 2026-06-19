#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

// Эмулируем тяжелую работу процессора без OpenSSL
unsigned long stretch_hash(const char* path) {
    unsigned long sum = 0;
    // Просто нагружаем процессор долгим циклом
    for (int i = 0; i < 100000000; i++) {
        sum += i % 13;
    }
    return sum;
}

const char* files[4] = {"a.html", "b.html", "c.html", "d.html"};
unsigned long results[4];

void* thread_routine(void* arg) {
    int idx = *(int*)arg;
    results[idx] = stretch_hash(files[idx]);
    return NULL;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        printf("Usage: %s <1|4>\n", argv[0]);
        return 1;
    }
    
    int mode = atoi(argv[1]);

    if (mode == 1) {
        // Однопоточный режим
        for(int i = 0; i < 4; i++) {
            results[i] = stretch_hash(files[i]);
        }
    } else if (mode == 4) {
        // Многопоточный режим
        pthread_t threads[4];
        int ids[4] = {0, 1, 2, 3};
        for(int i = 0; i < 4; i++) {
            pthread_create(&threads[i], NULL, thread_routine, &ids[i]);
        }
        for(int i = 0; i < 4; i++) {
            pthread_join(threads[i], NULL);
        }
    }

    for(int i = 0; i < 4; i++) printf("Result %d: %lu\n", i, results[i]);
    return 0;
}