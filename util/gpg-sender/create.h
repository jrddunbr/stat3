#ifndef CREATE_H
#define CREATE_H

#include <string>
#include <gcrypt.h>

using namespace std;

size_t get_keypair_size(int nbits);
void init();
int generate_key();

#endif /* CREATE_H */
