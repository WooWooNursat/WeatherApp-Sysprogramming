#include <iostream>

int _maxTemp(int *temps, int n) {
    int max = temps[0];
    for (int i = 1; i < n; i++)
        if (temps[i] > max)
            max = temps[i];
    return max;
}

int _minTemp(int *temps, int n) {
    int min = temps[0];
    for (int i = 1; i < n; i++)
        if (temps[i] < min)
            min = temps[i];
    return min;
}

int _averageTemp(int *temps, int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += temps[i];
    }
    return sum / n;
}

extern "C" {
    int maxTemp(int *temps, int n){ return _maxTemp(temps, n); }
    int minTemp(int *temps, int n){ return _minTemp(temps, n); }
    int averageTemp(int *temps, int n){ return _averageTemp(temps, n); }
}

int main () {
    int temps[] = {10, 20, 30, 40};
    int count = sizeof(temps) / sizeof(temps[0]);
    int result = _averageTemp(temps, count);
    std::cout << result << std::endl;
    return 0;
}