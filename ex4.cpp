#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
#include <unordered_set> 
#include <map>
std::vector<std::string> tokenize(const std::string& text) {
    std::vector<std::string> words;
    std::istringstream stream(text);
    std::string word;
    while (stream >> word) {
        for (auto& c : word) c = std::tolower(c);
        words.push_back(word);
    }
    return words;
}

// Оптимизированная версия
std::vector<std::string> unique_words(const std::vector<std::string>& words) {
    std::unordered_set<std::string> seen;
    std::vector<std::string> result;
    for (const auto& w : words) {
        if (seen.find(w) == seen.end()) {
            seen.insert(w);
            result.push_back(w);
        }
    }
    return result;
}

// Вместо count_word перебором, используем карту частот
int main(int argc, char* argv[]) {
    // ... (код чтения файла оставляем тот же) ...
    const char* filename = argc > 1 ? argv[1] : "big.txt";
    std::ifstream file(filename);
    if (!file) return 1;

    std::string text((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    auto words = tokenize(text);
    
    // Подсчет частот через map (гораздо быстрее)
    std::map<std::string, int> counts;
    for (const auto& w : words) counts[w]++;

    std::vector<std::pair<std::string, int>> freqs(counts.begin(), counts.end());

    std::partial_sort(freqs.begin(),
        freqs.begin() + std::min<size_t>(10, freqs.size()),
        freqs.end(),
        [](const auto& a, const auto& b) { return a.second > b.second; });

    for (int i = 0; i < 10 && i < (int)freqs.size(); i++) {
        std::cout << freqs[i].first << " " << freqs[i].second << std::endl;
    }
    return 0;
}