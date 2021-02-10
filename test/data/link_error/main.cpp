#include <iostream>

extern int not_a_function();

int main()
{
    not_a_function();
    return 0;
}