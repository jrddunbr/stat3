all: main

main: encrypt.o
	g++ --std=c++14 main.cpp encryption.o -o main -lgcrypt

encrypt.o:
	g++ --std=c++14 -c encryption.cpp

clean:
	rm -f *.o main
