#ifndef SEND_H
#define SEND_H

#include <string>
#include <gcrypt.h>

using namespace std;

size_t get_keypair_size(int nbits);
void init();
string encrypt_message(string message);
int send_message(string message);
#endif /* SEND_H */
