all: main

main: encrypt.o
	g++ main.cpp encryption.o -o main -lgcrypt

encrypt.o:
	g++ -c encryption.cpp

clean:
	rm -f *.o main
