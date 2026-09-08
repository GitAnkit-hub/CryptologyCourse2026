// TAsk to do:
// AES Encryption
// AES Decryption
// Key Scheduling function
// Round Function

#include <iostream>
#include <vector>
using namespace std;
#include <random>
#include <sodium.h> // cryptographically secure random number generator
#include<iomanip>
vector<unsigned char> Round_const = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36};
// since hex data is of 1 Byte
// unsigned char and uint8_t are guaranteed to be 1 byte size

vector<unsigned char> Master_key;

// implement the shift rows also
void shiftRows(unsigned char *state[4][4])
{
    // Shift the rows of the state array
    for (int r = 1; r < 4; ++r)
    {
        unsigned char temp[4];
        for (int c = 0; c < 4; ++c)
        {
            temp[c] = (*state)[r][(c + r) % 4];
        }
        for (int c = 0; c < 4; ++c)
        {
            (*state)[r][c] = temp[c];
        }
    }
}

// SubTasks for key scheduling function
// generate the master key
// implement the shiftrows function
// generate all the round keys


void generateMasterKey()
{   
    if(sodium_init() < 0){
        cerr << "Failed to initialize libsodium\n";
        return;
    }

    // Initialize the master key with random values
    Master_key.resize(16); // AES-128 uses a 16-byte key
     // A fixed 32-byte dummy seed for assignment testing
    const unsigned char assignment_seed[randombytes_SEEDBYTES] = {
        0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
        0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10,
        0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18,
        0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f, 0x20
    };
    randombytes_buf_deterministic(Master_key.data(), Master_key.size(), assignment_seed);
    cout << "Master Key: ";
    for (const auto &byte : Master_key)
    {
        cout << hex << setw(2) << setfill('0') << static_cast<int>(byte) << " ";
    }
    cout << endl;
}



int main(){
    generateMasterKey();
    return 0;
}

