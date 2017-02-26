#include <iostream>
#include <string>
#include "encryption.h"
#include "gcrypt.h"

using namespace std;

int main() {
  Encryption encrypt;
  KeyPair keypair;
  keypair = encrypt.create_key();
  cout << "KeyPair pub: " << keypair.pub << " priv: " << keypair.priv << "\n";
  //encrypt.write_key("public.key", keypair.pub);
  //cout << encrypt.read_key("private.key") << "\n";
  gcry_sexp_t test = encrypt.to_gcrypt(keypair.pub);
  string test2 = encrypt.to_string(test);
  //we want these to be the exact same string. This confirms that the keys are reloaded properly
  cout << "pub-before: " << keypair.pub << " pub-afer: " << test2 << "\n";
  cout << "compare " << keypair.pub.compare(test2) << "\n";
}
