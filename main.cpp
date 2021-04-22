
#include <SFML/Graphics.hpp>
#include <string>
#include <vector>


const int WIN_WIDTH = 600;
const int WIN_HEIGHT = 600;
const int TILES_IN_ROW = 8;
const int TILES_IN_COL = 8;
const int TILE_WIDTH = WIN_WIDTH / TILES_IN_ROW;
const int TILE_HEIGHT = WIN_HEIGHT / TILES_IN_COL;


enum P_TYPE {
	KING=9,
	QUEEN=1,
	ROOK=2,
	BISHOP=3,
	KNIGHT=4,
	PAWN=5,
	EMPTY=0
};


enum P_COLOR {
	WHITE=1,
	BLACK=2,
};



struct Piece {
	int type, color;

	std::string getTextureFile() {
		std::string fname;

		if (color == P_COLOR::WHITE) {
			fname = "white_";
		} else {
			fname = "black_";
		}

		switch (type) {
			case P_TYPE::KING:
				fname += "king.png";
				break;

			case P_TYPE::QUEEN:
				fname += "queen.png";
				break;

			case P_TYPE::ROOK:
				fname += "rook.png";
				break;

			case P_TYPE::BISHOP:
				fname += "bishop.png";
				break;

			case P_TYPE::KNIGHT:
				fname += "knight.png";
				break;

			case P_TYPE::PAWN:
				fname += "pawn.png";
				break;
		}

		return fname;
	}
};



void drawBoard(sf::RenderWindow &win) {
	for (int i = 0; i < TILES_IN_ROW * TILES_IN_COL; i++) {
		sf::RectangleShape tile(sf::Vector2f(TILE_WIDTH, TILE_HEIGHT));

		if ((i + i / TILES_IN_ROW) % 2 == 0) {
			tile.setFillColor(sf::Color(255, 255, 255));
		} else {
			tile.setFillColor(sf::Color(50, 50, 50));
		}

		tile.setPosition(sf::Vector2f((i % TILES_IN_ROW) * TILE_WIDTH, (i / TILES_IN_ROW) * TILE_HEIGHT));
		win.draw(tile);
	}
}


void drawPieces(sf::RenderWindow &win, const std::vector<std::vector<Piece>> &pieces) {
	for (int y = 0; y < pieces.size(); y++) {
		for (int x = 0; x < pieces[y].size(); x++) {
			Piece p = pieces[y][x];
		
			if (p.type != P_TYPE::EMPTY) {
				std::string textureFile = p.getTextureFile();
				
				sf::Texture texture;
				if (!texture.loadFromFile("assets/" + textureFile)) {

				} else {
					texture.setSmooth(true);
					texture.setRepeated(false);
		
					sf::Sprite sprite;
					sprite.setTexture(texture);
					
					sprite.setPosition(sf::Vector2f(x * TILE_WIDTH, y * TILE_HEIGHT));
				
					win.draw(sprite);
				}
			}
		}
	}
}	


int main() {
	const std::string WIN_TITLE = "Frost Chess Engine 1.0"; 

	std::vector<std::vector<Piece>> pieces;
	
	const std::vector<std::vector<Piece>> DEFAULT_BOARD = {
		{{2, 2}, {4, 2}, {3, 2}, {1, 2}, {9, 2}, {3, 2}, {4, 2}, {2, 2}},
		{{5, 2}, {5, 2}, {5, 2}, {5, 2}, {5, 2}, {5, 2}, {5, 2}, {5, 2}},
		{{0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}},
		{{0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}},
		{{0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}},
		{{0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}},
		{{5, 1}, {5, 1}, {5, 1}, {5, 1}, {5, 1}, {5, 1}, {5, 1}, {5, 1}},
		{{2, 1}, {4, 1}, {3, 1}, {1, 1}, {9, 1}, {3, 1}, {4, 1}, {2, 1}}
	};
	
	pieces = DEFAULT_BOARD;
    sf::RenderWindow window(sf::VideoMode(WIN_WIDTH, WIN_HEIGHT), WIN_TITLE, sf::Style::Close);
	window.setVerticalSyncEnabled(true);
	
    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear();
		drawBoard(window);
		drawPieces(window, pieces);
        window.display();
    }

    return 0;
}


