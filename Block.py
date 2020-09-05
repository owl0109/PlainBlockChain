import hashlib
import datetime
import time

class Block():
    #変数の宣言
    def __init__(self, index, prev_hash, data, timestamp, bits):
        self.index = index
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = 0
        self.elapsed_time = ""
        self.block_hash = ""

    #特殊メソッド。
    def __setitem__(self, key, value):
        setattr(self, key, value)

    #ここでブロックのデータとしてまとめる
    def to_json(self):
        return {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "stored_data": self.data,
            "timestamp": self.timestamp.strftime("%Y/%m/%d %H:%M:%S"),
            "bits": self.bits,
            "nonce": self.nonce,
            #生成した時間
            "elapsed_time": self.elapsed_time,
            "block_hash": self.block_hash
        }

    #ブロックヘッダを構築しそれをSHA256でハッシュ化してそれを返すよ
    def calc_blockhash(self):
        blockhead = str(self.index) + str(self.prev_hash) + str(self.data) + str(self.timestamp) + hex(self.bits)[2:] + str(self.nonce)
        #.encode()によってエンコードする
        #冒頭で定義しているブロックハッシュの変数にこのメソッドで計算したハッシュ値を代入する。
        h = hashlib.sha256(blockhead.encode()).hexdigest()
        self.block_hash = h
        return h

    #bitsからtargetを算出。
    def calc_target(self):
        #右に24ビットシフトさせ、3引いている。
        #leだけが残る。そこから3引いて、exponent_bytesを計算する
        exponent_bytes = (self.bits >> 24) -3
        #1バイト=>8ビットだから計算する
        exponent_bits = exponent_bytes * 8
        coefficient = self.bits & 0xffffff
        #coefficientをexponent_bits分だけ左にシフトする
        return coefficient << exponent_bits

    #計算されたハッシュ値が先ほど計算したターゲットより小さいか計算する。
    def check_valid_hash(self):
        return int(self.calc_blockhash(),16) <= self.calc_target()