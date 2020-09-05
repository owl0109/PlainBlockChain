import hashlib
import datetime
import time
import json

from BlockChain import Blockchain

#ここを0x1d777777に変更する
INITIAL_BITS = 0x1e777777

if __name__ == "__main__":
    bc = Blockchain(INITIAL_BITS)
    print("ジェネシスブロックを作成中・・・")
    bc.create_genesis()
    for i in range(30):
        print(str(i + 2) + "番目のブロックを生成中・・・")
        bc.add_newblock(i)