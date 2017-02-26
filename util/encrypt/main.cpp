#include <iostream>
#include <string>
#include "encryption.h"

using namespace std;

int main() {
  Encryption encrypt;
  KeyPair keypair;
  keypair = encrypt.create_key();
  cout << "KeyPair pub: " << keypair.pub << " priv: " << keypair.priv << "\n";
  //encrypt.write_key("public.key", keypair.pub);
  //cout << encrypt.read_key("private.key") << "\n";
}
