#include <fstream>
#include <iostream>
#include <algorithm>
#include "loader.h"
#include "opcode.h"
#include "object.h"
#include "utils.h"

Loader::Loader(char *path) : path(path) {}

Bytecode *Loader::Load()
{
    bool IsLittleEndian = isLittleEndian();
    std::ifstream file(path, std::ios::binary);
    if (!file)
    {
        std::cerr << "faild to open " + (std::string)path << std::endl;
        return nullptr;
    }

    FileHeader header;
    file.read(reinterpret_cast<char *>(&header), sizeof(header));
    if (IsLittleEndian)
    {
        header.magic = swapEndianness(header.magic);
        header.version = swapEndianness(header.version);
        header.constants = swapEndianness(header.constants);
        header.instructions = swapEndianness(header.instructions);
    }

    if (header.magic != MAGIC)
    {
        std::cerr << "invalid file format, wrong magic number: " << header.magic << std::endl;
        return nullptr;
    }
    std::cout << "get header: "
              << header.magic << "_"
              << header.version << "_"
              << header.constants << "_"
              << header.instructions
              << std::endl;
    // load constant pool
    std::vector<obj::Object *> Constants(0);
    if (header.constants > 0)
    {
        obj::ConstsPool pool(header.constants);
        file.read(reinterpret_cast<char *>(&pool[0]), header.constants);
        std::cout << "loading constants..." << std::endl;
        for (size_t i = 0; i < pool.size(); i++)
        {
            auto [newObject, offset] = obj::ReadConst(pool, i);
            if (!newObject)
                return nullptr;
            Constants.push_back(newObject);
            i += offset;
        }
    }
    // load instructions
    std::cout << "loading instructions..." << std::endl;
    code::Instructions Instructions(header.instructions);
    file.read(reinterpret_cast<char *>(&Instructions[0]), header.instructions);

    uint32_t eof;
    file.read(reinterpret_cast<char *>(&eof), sizeof(eof));
    if (IsLittleEndian)
        eof = swapEndianness(eof);
    if (eof != ENDOFFILE)
    {
        std::cerr << "file is corrupt" << std::endl;
        return nullptr;
    }

    return new Bytecode{Instructions, Constants};
}