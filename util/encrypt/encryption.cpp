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
    //if (isalpha(input)) {
      str += input;
    //}
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
  gcry_sexp_build(&prams, NULL, "(genkey (rsa (nbits 4:2048)))");
  gcry_pk_genkey(&keypair, prams);
  gcry_sexp_t pubk = gcry_sexp_find_token(keypair, "public-key", 0);
  //use the below line for the key with less surrounding data
  //gcry_sexp_t pubk = gcry_sexp_find_token(pubk1, "n", 0);
  gcry_sexp_t privk = gcry_sexp_find_token(keypair, "private-key", 0);

  if(!pubk || !privk) {
	  cout << "Failed to generate key!\n";
	  exit(1);
  }

  KeyPair key;
  key.pub = to_string(pubk);
  key.priv = to_string(privk);
  return key;
}

gcry_sexp_t Encryption::encrypt(string pubkey, string data) {
  gcry_sexp_t ciphertext;
  gcry_pk_encrypt(&ciphertext, to_gcrypt(data), to_gcrypt(pubkey));
  return ciphertext;
}

string Encryption::decrypt(string privkey, gcry_sexp_t &ciphertext) {
  gcry_sexp_t data;
  gcry_pk_decrypt(&ciphertext, data, to_gcrypt(privkey));
  return to_string(data);
}

size_t Encryption::get_keypair_size(int nbits)
{
    size_t aes_blklen = gcry_cipher_get_algo_blklen(GCRY_CIPHER_AES128);

    // format overhead * {pub,priv}key (2 * bits)
    size_t keypair_nbits = 4 * (2 * nbits);

    size_t rem = keypair_nbits % aes_blklen;
    return (keypair_nbits + rem) / 8;
}

gcry_sexp_t Encryption::to_gcrypt(string key) {
  size_t error = 0;
  gcry_sexp_t raw;
  gcry_sexp_build(&raw, NULL, key.c_str());
  //gcry_sexp_new(&raw, key.c_str(), sizeof(key.c_str()), 0);
  return raw;
}

string Encryption::to_string(gcry_sexp_t key) {
  size_t sz = gcry_sexp_sprint(key, GCRYSEXP_FMT_ADVANCED, NULL, 0);
  char *buffer = (char *) malloc(sz);
  gcry_sexp_sprint(key, GCRYSEXP_FMT_ADVANCED, buffer, sz);
  string str = buffer;
  return str;
}
