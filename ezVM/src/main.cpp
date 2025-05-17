#include <iostream>
#include "ezVM.h"

int main()
{
    std::cout << "Hello VM" << std::endl;
    VM vm = VM(Bytecode{});
    vm.Run();
    return 0;
}
