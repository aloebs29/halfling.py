#include "sub.hpp"

int sub(int a, int b)
{
#if defined(DEFINED_IN_TOML) && defined(ALSO_DEFINED_IN_TOML)
    return a - b;
#endif
}