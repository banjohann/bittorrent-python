import os

class PieceManager:
    def __init__(self, pieces_dir="pieces"):
        self.pieces_dir = os.path.join(os.path.dirname(__file__), pieces_dir)
        os.makedirs(self.pieces_dir, exist_ok=True)

    def list_pieces(self):
        return [
            int(fname[:-4])
            for fname in os.listdir(self.pieces_dir)
            if fname.endswith(".txt") and fname[:-4].isdigit()
        ]

    def has_piece(self, piece_id):
        return os.path.exists(self._piece_path(piece_id))

    def save_piece(self, piece_id, data):
        with open(self._piece_path(piece_id), "wb") as f:
            f.write(data)

    def get_piece(self, piece_id):
        with open(self._piece_path(piece_id), "rb") as f:
            return f.read()

    def _piece_path(self, piece_id):
        return os.path.join(self.pieces_dir, f"{piece_id}.txt")