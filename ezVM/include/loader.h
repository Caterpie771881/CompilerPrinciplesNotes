#ifndef LOADER_H
#define LOADER_H

#include "ezVM.h"
#include <cstdint>

const uint32_t MAGIC = 0x657a766d;
const uint32_t ENDOFFILE = 0x00656f66;

struct FileHeader
{
    uint32_t magic;
    uint16_t version;
    uint32_t constants;
    uint32_t instructions;
};

class Loader
{
public:
    Loader(char *);
    Bytecode *Load();

private:
    char *path;
};

#endif