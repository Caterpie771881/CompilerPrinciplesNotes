#ifndef UTILS_H
#define UTILS_H

#include <cstdint>
#include <vector>

void PutUint16(std::vector<uint8_t> &, size_t, uint16_t);

uint16_t ReadUint16(const std::vector<uint8_t> &, size_t);

bool isLittleEndian();

uint32_t swapEndianness(const uint32_t &);

uint16_t swapEndianness(const uint16_t &);

#endif