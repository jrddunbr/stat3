#include <iostream>
#include <fstream>
#include <string>
#include <gcrypt.h>
#include "encryption.h"

using namespace std;

string Encryption::read_key(string filename) {
  ifstream in = ifstream(filename);
  string str = "";
  while(in) {
    char input = in.get();
    if (isalpha(input)) {
      str += input;
    }
  }
  in.close();
  return str;
}

int Encryption::write_key(string filename, string key) {
  ofstream out = ofstream(filename);
  out << key;
  out.close();
  return 0;
}

KeyPair Encryption::create_key() {
  gcry_sexp_t prams, keypair;
  gcry_sexp_build(&prams, NULL, "(genkey (rsa (nbits 4:256)))");
  gcry_pk_genkey(&keypair, prams);
  gcry_sexp_t pubk = gcry_sexp_find_token(keypair, "public-key", 0);
  gcry_sexp_t privk = gcry_sexp_find_token(keypair, "private-key", 0);

  cout << "raw: "<< keypair << "\n";
  //cout << "both: " << to_string(keypair) << "\n";
  cout << "priv: " << to_string(privk) << "\n";
  cout << "pub: " << to_string(pubk) << "\n";

  KeyPair key;
  key.pub = "pub";
  key.priv = "priv";
  return key;
}

string Encryption::encrypt(string pubkey, string data) {
  /*
  gcry_sexp_t data;
  data = to_gcrypt(data);
  gcry_pk_encrypt(<cipher>, data, to_gcrypt(pubkey));
  */
  return "encrypted";
}

string Encryption::decrypt(string privkey, string data) {
  /*
  gcry_sexp_t data;
  data = to_gcrypt(data);
  gcry_pk_decrypt(<cipher>, data, to_gcrypt(privkey));
  */
  return "decrypted";
}

size_t Encryption::get_keypair_size(int nbits)
{
    size_t aes_blklen = gcry_cipher_get_algo_blklen(GCRY_CIPHER_AES128);

    // format overhead * {pub,priv}key (2 * bits)
    size_t keypair_nbits = 4 * (2 * nbits);

    size_t rem = keypair_nbits % aes_blklen;
    return (keypair_nbits + rem) / 8;
}

/*

gcry_sexp_t Encryption::to_gcrypt(string key) {
  size_t error = 0;
  gcry_sexp_t raw;
  return gcry_sexp_new(raw, key.c_str(), sizeof(key.c_str()), 0);
}

*/

string Encryption::to_string(gcry_sexp_t key) {
  char* charstr = gcry_sexp_nth_string(key, 0);
  string str = charstr;
  gcry_free(charstr);
  return str;
}
