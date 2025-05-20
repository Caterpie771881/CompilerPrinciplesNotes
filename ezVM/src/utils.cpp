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

bool isLittleEndian()
{
    uint32_t x = 1;
    return *reinterpret_cast<std::byte *>(&x) == std::byte{1};
}

uint32_t swapEndianness(const uint32_t &value)
{
    return (value >> 24) |
           ((value & 0x00FF0000) >> 8) |
           ((value & 0x0000FF00) << 8) |
           (value << 24);
}

uint16_t swapEndianness(const uint16_t &value)
{
    return (value >> 8) | (value << 8);
}