#include "utils.h"

void PutUint16(std::vector<uint8_t> &v, size_t offset, uint16_t u16)
{
    v[offset] = static_cast<uint8_t>((u16 >> 8) & 0xFF);
    v[offset + 1] = static_cast<uint8_t>(u16 & 0xFF);
}

uint16_t ReadUint16(const std::vector<uint8_t> &v, size_t offset)
{
    uint8_t a = v[offset];
    uint8_t b = v[offset + 1];
    return (static_cast<uint16_t>(a) << 8) + static_cast<uint16_t>(b);
}
