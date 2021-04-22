


build:
	make clean 
	make engine

clean:
	-rm *.o


engine: main.o
	g++ -o engine main.o -lsfml-graphics -lsfml-window -lsfml-system

main.o:
	g++ -c main.cpp -I/home/james/SFML-2.5.1/SFML-2.5.1/include



.PHONY: clean, build
