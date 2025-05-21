#include <iostream>
#include "loader.h"
#include "ezVM.h"
#include <string>

void checkStackTop(VM &vm, size_t deep = 1)
{
    for (size_t i = 0; i < deep; i++)
    {
        obj::Object *o = vm.Pop();
        if (!o)
            break;
    }
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        std::cerr << "need a path" << std::endl;
        return -1;
    }
    std::cout << "========== Hello VM ==========" << std::endl;
    Loader loader = Loader(argv[1]);
    Bytecode *bytecode = loader.Load();
    if (bytecode)
    {
        VM vm = VM(*bytecode);
        std::cout << "============ RUN =============" << std::endl;
        vm.Run();
        std::cout << "============ END =============" << std::endl;
        checkStackTop(vm, 5);
        delete bytecode;
    }
    return 0;
}
