#ifndef ENCRYPTION_H
#define ENCRYPTION_H

#include <string>
#include <gcrypt.h>

using std::string;
using std::cout;

typedef struct KeyPair {
  string pub;
  string priv;
};

class Encryption {
private:
  gcry_sexp_t keypair, pubkey, privkey;
  size_t get_keypair_size(int nbits);
  size_t keysize;
  gcry_sexp_t to_gcrypt(string key);
  string to_string(gcry_sexp_t);
public:
  Encryption() {
    if(!gcry_check_version (NULL)) {
      cout << "Error loading libgcrypt\n";
      exit(1);
    }
  }
  string read_key(string filename);
  int write_key(string filename, string key);
  KeyPair create_key();
  string encrypt(string pubkey, string data);
  string decrypt(string privkey, string data);
};

#endif /* ENCRYPTION_H */
