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
        #難易度設定をする
        new_bits = self.get_retarget_bits()

        #難易度設定をしないとき、-1を返す。
        if new_bits < 0 :
            bits = last_block.bits
        else:
            #難易度設定をする
            bits = new_bits

        block = Block(i+1,last_block.block_hash,"ブロック" + str(i+1),datetime.datetime.now(),bits)
        self.mining(block)

    def get_retarget_bits(self):
        #ブロックを5個生成するたびに難易度変更する
        if len(self.chain) == 0 or len(self.chain) % 5 !=0:
            return -1
        #時間の取得
        expected_time = 140*5

        #最初のブロックを取得
        if len(self.chain) != 5:
            first_block = self.chain[-(1+5)]
        else:
            first_block = self.chain[0]

        last_block = self.chain[-1]

        #最初のブロック生成の時間を取得
        first_time = first_block.timestamp.timestamp()
        #最後のブロック生成時間を取得
        last_time = last_block.timestamp.timestamp()

        #時間がどの程度かかったか計算する処理
        total_time = last_time - first_time

        #ターゲットの生成
        target = last_block.calc_target()
        #マイニングにかかる時間の比を計算する
        delta = total_time / expected_time

        if delta < 0.25:
            delta = 0.25
        if delta > 4:
            delta = 4

        new_target = int(target * delta)

        exponent_bytes = (last_block.bits >> 24)-3
        exponent_bits = exponent_bytes * 8
        temp_bits = new_target >> exponent_bits
        #難易度が高すぎるときの処理
        if temp_bits != temp_bits & 0xffffff:
            exponent_bytes += 1
            exponent_bits += 8

        #難易度が低いときの処理
        elif temp_bits == temp_bits & 0xffff:
            exponent_bytes -=1
            exponent_bits -= 8
        #ビット計算をして返す。
        return ((exponent_bytes + 3)<<24) | (new_target >> exponent_bits)
