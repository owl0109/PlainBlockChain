import json
import time
import datetime
from Block import Block

MAX_32BIT = 0xffffffff

class Blockchain():
    #初期値設定
    def __init__(self, inital_bits):
        self.chain = []
        self.initial_bits = inital_bits

    #配列の一番後ろに要素を追加(append)する
    def add_block(self, block):
        self.chain.append(block)

    def getblockinfo(self, index=-1):
        #JSON形式で出力する処理
        return print(json.dumps(self.chain[index].to_json(), indent=2, sort_keys=True, ensure_ascii=False))

    def mining(self, block):
        #ブロックをつなげるための処理を定義
        start_time = int(time.time() * 1000)
        while True:
            #range関数が0からカウントを始めるための処理
            for n in range(MAX_32BIT + 1):
                #ナンスの値を次々更新
                block.nonce = n
                #ナンスの値がターゲットより小さいとき
                if block.check_valid_hash():
                    #時間を取得
                    end_time = int(time.time() * 1000)
                    block.elapsed_time = str((end_time - start_time)/1000.0)+"秒"
                    #ブロックを追加
                    self.add_block(block)
                    #ブロックの中身を表示
                    self.getblockinfo()
                    return
            new_time = datetime.datetime.now()
            if new_time == block.timestamp:
                #時間がかぶってた時の処理
                block.timestamp += datetime.timedelta(seconds=1)
            else:
                block.timestamp = new_time

    #ジェネシスブロックの作成
    def create_genesis(self):
        genesis_block = Block(0,"0000000000000000000000000000000000000000000000000000000000000000","ジェネシスブロック",datetime.datetime.now(),self.initial_bits)
        self.mining(genesis_block)

    def add_newblock(self,i):
        #新しいブロックを作成する
        last_block = self.chain[-1]
        block = Block(i+1,last_block.block_hash,"ブロック" + str(i+1),datetime.datetime.now(),last_block.bits)
        self.mining(block)

