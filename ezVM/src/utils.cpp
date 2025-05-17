#include "utils.h"


void PutUint16(std::vector<uint8_t> v, int offset, uint16_t u) {
    v[offset] = static_cast<uint8_t>((u >> 8) & 0xFF);
    v[offset + 1] = static_cast<uint8_t>(u & 0xFF);
}
