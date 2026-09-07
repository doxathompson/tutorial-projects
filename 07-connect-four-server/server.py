"""Concurrent TCP wrapper around a deterministic Connect Four domain model."""
from __future__ import annotations
import socketserver
ROWS,COLS=6,7
class Game:
    def __init__(self): self.board=[[0]*COLS for _ in range(ROWS)]; self.player=1
    def drop(self,column:int)->bool:
        if column not in range(COLS): raise ValueError("column must be 0..6")
        for row in reversed(range(ROWS)):
            if self.board[row][column]==0:
                self.board[row][column]=self.player; won=self.has_won(row,column); self.player=3-self.player; return won
        raise ValueError("column is full")
    def has_won(self,row:int,col:int)->bool:
        token=self.board[row][col]
        for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
            count=1
            for sign in (-1,1):
                r,c=row+dr*sign,col+dc*sign
                while 0<=r<ROWS and 0<=c<COLS and self.board[r][c]==token: count+=1; r+=dr*sign; c+=dc*sign
            if count>=4:return True
        return False
class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        game=Game(); self.wfile.write(b"Connect Four: enter columns 0-6\n")
        for line in self.rfile:
            try: won=game.drop(int(line)); self.wfile.write((render(game)+("Winner!\n" if won else "")).encode())
            except ValueError as exc: self.wfile.write(f"error: {exc}\n".encode())
            if won:return
def render(game): return "\n".join(" ".join(".XO"[cell] for cell in row) for row in game.board)+"\n"
if __name__=="__main__":
    # ThreadingMixIn isolates clients; daemon threads let Ctrl-C shut down cleanly.
    class Server(socketserver.ThreadingMixIn,socketserver.TCPServer): daemon_threads=True; allow_reuse_address=True
    with Server(("127.0.0.1",9999),Handler) as server: server.serve_forever()

