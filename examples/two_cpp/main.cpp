#include <iostream>

extern int calculate_something(int a, int b);

int main()
{
    std::cout << "I calculated.. " << calculate_something(0x015, 0x237) << std::endl;
    return 0;
}