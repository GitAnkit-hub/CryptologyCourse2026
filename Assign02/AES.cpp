// TAsk to do:
// AES Encryption
// AES Decryption
// Key Scheduling function
// Round Function

#include <iostream>
#include <vector>
using namespace std;
vector<unsigned char>Round_const = { 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36 };
// since hex data is of 1 Byte
// unsigned char and uint8_t are guaranteed to be 1 byte size
