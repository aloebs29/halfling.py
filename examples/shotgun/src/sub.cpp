#include "sub.hpp"

int sub(int a, int b)
{
#if defined(DEFINED_IN_PY) && defined(ALSO_DEFINED_IN_PY)
    return a - b;
#endif
}
