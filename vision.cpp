#include <iostream>
#include <string>
#include <windows.h>
using namespace std;

int main()
{

    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);

    string name;
    int age;
    string vision;
    int obj;
    int process;
    bool activation;




    cout << "이름을 입력하세요 : ";
    cin >> name;
    cout << "나이를 입력하세요 : ";
    cin >> age;
    cout << "나의 비전(한 단어)을 입력하세요: ";
    cin >> vision;
    cout << "목표 수치를 입력하세요(0~100): ";
    cin >> obj;
    cout << "현재 진행 수치를 입력하세요(0~100): ";
    cin >> process;
    cout << "비전 활성화 여부 (1: 시작, 0: 대기): ";
    cin >> activation;


    cout << "-- 나의 성장 비전 리포트 --"<< endl;
    cout << "성함" << name << " (" << age << "세)"<< endl;
    cout << "목표 비전" << vision << endl;
    cout << "진행도 :" << obj << "/100"<< endl;
    cout << "현재 달성률 : " << process << "%"<< endl;
    cout << "운영 상태:" << (activation ? "진행" : "대기")<< endl ;
    cout << "----------------------------";





    return 0;
    

}