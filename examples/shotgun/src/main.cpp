#include <iostream>

#include "add.hpp"
#include "sub.hpp"
#include "mul.hpp"

int main()
{
    std::cout << "Calculating 2 + 3 with function in another file.." << std::endl;
    std::cout << "Result: " << add(2, 3) << std::endl
              << std::endl;

    std::cout << "Calculating 16 - 9 with a function depending on defines in the TOML.. "
              << std::endl;
    std::cout << "Result: " << sub(16, 9) << std::endl
              << std::endl;

    std::cout << "Calculating 6 x 7 with a function in a static library.. "
              << std::endl;
    std::cout << "Result: " << mul(6, 7) << std::endl
              << std::endl;
    return 0;
}