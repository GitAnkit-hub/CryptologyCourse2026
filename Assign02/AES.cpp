// TAsk to do:
// AES Encryption
// AES Decryption
// Key Scheduling function
// Round Function

#include <iostream>
#include <vector>
using namespace std;
vector<unsigned char> Round_const = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36};
// since hex data is of 1 Byte
// unsigned char and uint8_t are guaranteed to be 1 byte size

// Key Scheduling Concept
// ki = shiftrows(ki-1) ^ RCi

vector<unsigned char> Master_key;

// implement the shift rows also
void shiftRows(unsigned char *state[4][4])
{
}

// SubTasks for key scheduling function
// generate the master key
// implement the shiftrows function
// generate all the round keys
#include <random>
#include <sodium.h> // cryptographically secure random number generator

void generateMasterKey()
{

    // Initialize the master key with random values
    Master_key.resize(16); // AES-128 uses a 16-byte key
    randombytes_buf(Master_key.data(), Master_key.size());
}

cout << "Master Key: ";
for (const auto &byte : Master_key)
{
    cout << hex << static_cast<int>(byte) << " ";
}
cout << endl;