#include <iostream>
#include <string>
#include "encryption.h"

using namespace std;

int main() {
  Encryption encrypt;
  KeyPair keypair;
  keypair = encrypt.create_key();
  cout << "kp: " << endl;
cout << "KeyPair pub: " << keypair.pub << " priv: " << keypair.priv;
  //encrypt.write_key("public.key", keypair.pub);
  //cout << encrypt.read_key("private.key") << "\n";
}
