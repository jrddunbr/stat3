#ifndef SERVER
#define SERVER

#include <iostream>
#include <map>
#include <stream>
#include <sys/socket.h>
#include <arpa/inet.h>

class Tcp_Srv {
private:
  string std::address;
  short port;
  sockaddr_in host;
  int listen_socket;
public:
  Tcp_Srv(std::string address, int port) {

  };
  ~Tcp_Srv() {
    close(listen_socket);
  }
};

class Udp_Srv {
private:
  std::string address;
  short port;
  sockaddr_in host;
  int listen_socket;
public:
  Udp_Srv(std::string address, int port) {

  };
  ~Udp_Srv() {
    close(listen_socket);
  };
};

class Server_Srv {
private:
  bool udp;
public:
  Server_Srv(int port, bool udp);
};

class Battery_Srv {
private:
  bool udp;
public:
  Battery_Srv(int port, bool udp);
};

class Sensor_Srv {
private:
  bool udp;
public:
  Battery_Srv(int port, bool udp);
};

class Network_Srv {
private:
  bool udp;
public:
  Network_Srv(int port, bool udp);
};

#endif /* SERVER */
