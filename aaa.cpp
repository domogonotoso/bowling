#include <iostream>
#include <limits>
#include <windows.h>
using namespace std;

// 덧셈
bool add_overflow(long long a, long long b, long long &res) {
    if ((b > 0 && a > LLONG_MAX - b) ||
        (b < 0 && a < LLONG_MIN - b))
        return true;
    res = a + b;
    return false;
}

// 뺄셈
bool sub_overflow(long long a, long long b, long long &res) {
    if ((b < 0 && a > LLONG_MAX + b) ||
        (b > 0 && a < LLONG_MIN + b))
        return true;
    res = a - b;
    return false;
}

// 곱셈
bool mul_overflow(long long a, long long b, long long &res) {
    if (a == 0 || b == 0) {
        res = 0;
        return false;
    }

    if (a > 0) {
        if (b > 0 && a > LLONG_MAX / b) return true;
        if (b < 0 && b < LLONG_MIN / a) return true;
    } else {
        if (b > 0 && a < LLONG_MIN / b) return true;
        if (b < 0 && a < LLONG_MAX / b) return true;
    }

    res = a * b;
    return false;
}

// 나눗셈
bool div_error(long long a, long long b, long long &res) {
    if (b == 0) return true;
    if (a == LLONG_MIN && b == -1) return true;
    res = a / b;
    return false;
}

// 연산 수행
bool calculate(long long a, char op, long long b, long long &res) {
    switch (op) {
        case '+': return add_overflow(a, b, res);
        case '-': return sub_overflow(a, b, res);
        case '*': return mul_overflow(a, b, res);
        case '/': return div_error(a, b, res);
    }
    return true;
}

int main() {
    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);

    long long num[4];
    char op[3];

    // 입력
    cout << "첫번째 숫자를 입력하세요 : "; cin >> num[0];
    cout << "첫번째 연산자를 입력하세요 : "; cin >> op[0];
    cout << "두번째 숫자를 입력하세요 : "; cin >> num[1];
    cout << "두번째 연산자를 입력하세요 : "; cin >> op[1];
    cout << "세번째 숫자를 입력하세요 : "; cin >> num[2];
    cout << "세번째 연산자를 입력하세요 : "; cin >> op[2];
    cout << "네번째 숫자를 입력하세요 : "; cin >> num[3];

    long long temp;
    int opCount = 3; // ✅ 추가: 남은 연산자 수 추적

    // ✅ 1단계: *, / 먼저 처리
    for (int i = 0; i < opCount; i++) {
        if (op[i] == '*' || op[i] == '/') {
            if (calculate(num[i], op[i], num[i + 1], temp)) {
                cout << "오버플로우 또는 오류 발생\n";
                return 0;
            }

            num[i] = temp;

            for (int j = i + 1; j < opCount; j++) {
                num[j] = num[j + 1];
                op[j - 1] = op[j];
            }

            opCount--; // ✅ 추가: 연산자 수 감소
            i--;
        }
    }

    // ✅ 2단계: +, - (opCount 사용)
    long long result = num[0];
    for (int i = 0; i < opCount; i++) {  // ✅ 3 → opCount
        if (calculate(result, op[i], num[i + 1], result)) {
            cout << "오버플로우 또는 오류 발생\n";
            return 0;
        }
    }

    // 출력
    cout << "\n[ 결과 ]\n";

    cout << "Bin : ";
    unsigned long long tempBin = result;
    bool started = false;
    for (int i = 63; i >= 0; i--) {
        if ((tempBin >> i) & 1) started = true;
        if (started) cout << ((tempBin >> i) & 1);
    }
    if (!started) cout << "0";
    cout << endl;

    cout << "Dec : " << result << endl;
    cout << "Hex : 0x" << hex << uppercase << result << endl;

    return 0;
}