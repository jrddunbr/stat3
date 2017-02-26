#include <iostream>
#include <string>
#include "encryption.h"
#include "gcrypt.h"

using namespace std;

int main() {
  Encryption encrypt;
  KeyPair keypair;
  keypair = encrypt.create_key();
  encrypt.write_key("public.key", keypair.pub);
  cout << keypair.pub << "\n";
  cout << encrypt.read_key("public.key") << "\n";
  cout << encrypt.read_key("public.key").compare(keypair.pub) << "\n";
  gcry_sexp_t out = encrypt.encrypt(keypair.pub, "hello");
  cout << encrypt.decrypt(keypair.priv, out) << "\n";
}
