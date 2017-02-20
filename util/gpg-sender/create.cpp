#include <iostream>
#include <string>
#include <gcrypt.h>
#include "create.h"

using namespace std;

size_t get_keypair_size(int nbits)
{
    size_t aes_blklen = gcry_cipher_get_algo_blklen(GCRY_CIPHER_AES128);

    // format overhead * {pub,priv}key (2 * bits)
    size_t keypair_nbits = 4 * (2 * nbits);

    size_t rem = keypair_nbits % aes_blklen;
    return (keypair_nbits + rem) / 8;
}

void init() {
  if(!gcry_check_version (NULL)) {
    cout << "Error loading libgcrypt\n";
  }
}

int generate_key() {
  gcry_sexp_t prams, keypair;

  gcry_sexp_build(&prams, NULL, "(genkey (rsa (nbits 4:256)))");

  gcry_pk_genkey(&keypair, prams);

  size_t rsa_len = get_keypair_size(256);
  void* rsa_buff = calloc(1, rsa_len);

  gcry_sexp_sprint(keypair, GCRYSEXP_FMT_CANON, rsa_buff, rsa_len);
  gcry_sexp_dump(keypair);

  return -1;
}

int main(int argc, char** argv) {
  init();
  generate_key();
}
