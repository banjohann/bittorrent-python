import os
import random

def generate_pieces(num_pieces=20, min_piece=1):
    max_piece = num_pieces * 5
    pieces_dir = os.path.join(os.path.dirname(__file__), "client/pieces")
    os.makedirs(pieces_dir, exist_ok=True)
    all_ids = list(range(min_piece, max_piece))
    selected_ids = random.sample(all_ids, num_pieces)

    for piece_id in selected_ids:
        filename = os.path.join(pieces_dir, f"{piece_id}.txt")
        with open(filename, "w") as f:
            f.write(str(piece_id))

    print(f"{num_pieces} pedaços gerados em {pieces_dir}: {selected_ids}")

if __name__ == "__main__":
    try:
        num_pieces = int(input("Quantas peças deseja gerar? "))
    except ValueError:
        print("Entrada inválida. Usando valor padrão de 20 peças.")
        num_pieces = 20
    generate_pieces(num_pieces)