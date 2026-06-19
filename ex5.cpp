#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <algorithm>

int main() {
    std::map<std::string, std::vector<int>> gradebook = {
        {"alice",   {90, 85, 92}},
        {"bob",     {78, 88}},
        {"charlie", {95, 70, 80}},
    };

    // 1. Создаем структуру для хранения средних баллов
    std::vector<std::pair<std::string, int>> averages;

    // 2. Рассчитываем средние баллы и переносим в вектор
    for (auto& [name, scores] : gradebook) {
        int sum = 0;
        for (int s : scores) sum += s;
        averages.push_back({name, sum / scores.size()});
    }

    // 3. Теперь вектор МОЖНО сортировать
    std::sort(averages.begin(), averages.end(), [](const auto& a, const auto& b) {
        return a.second > b.second; // Сортируем по убыванию среднего балла
    });

    std::cout << "Rankings (High to Low):" << std::endl;
    for (auto& [name, avg] : averages) {
        std::cout << "  " << name << ": " << avg << std::endl;
    }

    return 0;
}