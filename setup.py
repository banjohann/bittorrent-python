import os
import random

def generate_random_pieces(num_pieces=20, min_piece=1, max_piece=None):
    if max_piece is None:
        max_piece = num_pieces * 5

    pieces_dir = os.path.join(os.path.dirname(__file__), "client/pieces")
    os.makedirs(pieces_dir, exist_ok=True)
    all_ids = list(range(min_piece, max_piece + 1))

    if num_pieces > len(all_ids):
        print(f"Aviso: Solicitadas {num_pieces} peças, mas o range permite apenas {len(all_ids)}.")
        num_pieces = len(all_ids)

    selected_ids = random.sample(all_ids, num_pieces)

    for file in os.listdir(pieces_dir):
        if file.endswith('.txt') and file[:-4].isdigit():
            os.remove(os.path.join(pieces_dir, file))

    for piece_id in selected_ids:
        filename = os.path.join(pieces_dir, f"{piece_id}.txt")
        with open(filename, "w") as f:
            f.write(str(piece_id))

    print(f"{num_pieces} pedaços aleatórios gerados em {pieces_dir}: {sorted(selected_ids)}")
    return selected_ids

def generate_sequential_pieces(start_piece, num_pieces=20):
    pieces_dir = os.path.join(os.path.dirname(__file__), "client/pieces")
    os.makedirs(pieces_dir, exist_ok=True)
    
    selected_ids = list(range(start_piece, start_piece + num_pieces))
    
    for file in os.listdir(pieces_dir):
        if file.endswith('.txt') and file[:-4].isdigit():
            os.remove(os.path.join(pieces_dir, file))
            
    for piece_id in selected_ids:
        filename = os.path.join(pieces_dir, f"{piece_id}.txt")
        with open(filename, "w") as f:
            f.write(str(piece_id))

    print(f"{num_pieces} pedaços sequenciais gerados em {pieces_dir}: {selected_ids}")
    return selected_ids

if __name__ == "__main__":
    print("Gerador de pedaços para BitTorrent")
    print("1. Gerar peças aleatórias")
    print("2. Gerar peças sequenciais")

    try:
        option = int(input("Escolha uma opção (1 ou 2): "))
        num_pieces = int(input("Quantas peças deseja gerar? "))

        if option == 1:
            generate_random_pieces(num_pieces)
        elif option == 2:
            start_piece = int(input("A partir de qual número? "))
            generate_sequential_pieces(start_piece, num_pieces)
        else:
            print("Opção inválida. Saindo.")
    except ValueError:
        print("Entrada inválida. Saindo.")