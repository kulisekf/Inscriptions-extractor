from enum import Enum

class BitcoinOP(Enum):
    OP_0 = "00"
    OP_PUSHDATA1 = "4c"
    OP_PUSHDATA2 = "4d"
    OP_PUSHDATA4 = "4e"
    OP_1NEGATE = "4f"
    OP_1 = "51"
    OP_2 = "52"
    OP_3 = "53"
    OP_4 = "54"
    OP_5 = "55"
    OP_6 = "56"
    OP_7 = "57"
    OP_8 = "58"
    OP_9 = "59"
    OP_10 = "5a"
    OP_11 = "5b"
    OP_12 = "5c"
    OP_13 = "5d"
    OP_14 = "5e"
    OP_15 = "5f"
    OP_16 = "60"
    OP_NOP = "61"
    OP_IF = "63"
    OP_NOTIF = "64"
    OP_ELSE = "67"
    OP_ENDIF = "68"
    OP_VERIFY = "69"
    OP_RETURN = "6a"
    OP_TOALTSTACK = "6b"
    OP_FROMALTSTACK = "6c"
    OP_2DROP = "6d"
    OP_2DUP = "6e"
    OP_3DUP = "6f"
    OP_2OVER = "70"
    OP_2ROT = "71"
    OP_2SWAP = "72"
    OP_IFDUP = "73"
    OP_DEPTH = "74"
    OP_DROP = "75"
    OP_DUP = "76"
    OP_NIP = "77"
    OP_OVER = "78"
    OP_PICK = "79"
    OP_ROLL = "7a"
    OP_ROT = "7b"
    OP_SWAP = "7c"
    OP_TUCK = "7d"
    OP_CAT = "7e"
    OP_SUBSTR = "7f"
    OP_LEFT = "80"
    OP_RIGHT = "81"
    OP_SIZE = "82"
    OP_INVERT = "83"
    OP_AND = "84"
    OP_OR = "85"
    OP_XOR = "86"
    OP_EQUAL = "87"
    OP_EQUALVERIFY = "88"
    OP_RESERVED1 = "89"
    OP_RESERVED2 = "8a"
    OP_1ADD = "8b"
    OP_1SUB = "8c"
    OP_2MUL = "8d"
    OP_2DIV = "8e"
    OP_NEGATE = "8f"
    OP_ABS = "90"
    OP_NOT = "91"
    OP_0NOTEQUAL = "92"
    OP_ADD = "93"
    OP_SUB = "94"
    OP_MUL = "95"
    OP_DIV = "96"
    OP_MOD = "97"
    OP_LSHIFT = "98"
    OP_RSHIFT = "99"
    OP_BOOLAND = "9a"
    OP_BOOLOR = "9b"
    OP_NUMEQUAL = "9c"
    OP_NUMEQUALVERIFY = "9d"
    OP_NUMNOTEQUAL = "9e"
    OP_LESSTHAN = "9f"
    OP_GREATERTHAN = "a0"
    OP_LESSTHANOREQUAL = "a1"
    OP_GREATERTHANOREQUAL = "a2"
    OP_MIN = "a3"
    OP_MAX = "a4"
    OP_WITHIN = "a5"
    OP_RIPEMD160 = "a6"
    OP_SHA1 = "a7"
    OP_SHA256 = "a8"
    OP_HASH160 = "a9"
    OP_HASH256 = "aa"
    OP_CODESEPARATOR = "ab"
    OP_CHECKSIG = "ac"
    OP_CHECKSIGVERIFY = "ad"
    OP_CHECKMULTISIG = "ae"
    OP_CHECKMULTISIGVERIFY = "af"
    OP_NOP1 = "b0"
    OP_NOP2 = "b1"
    OP_CHECKLOCKTIMEVERIFY = "b1"
    OP_NOP3 = "b2"
    OP_CHECKSEQUENCEVERIFY = "b2"
    OP_NOP4 = "b3"
    OP_NOP5 = "b4"
    OP_NOP6 = "b5"
    OP_NOP7 = "b6"
    OP_NOP8 = "b7"
    OP_NOP9 = "b8"
    OP_NOP10 = "b9"
    OP_INVALIDOPCODE = "ff"

    @classmethod
    def convert_byte_to_op(self, byte) -> str:
        try:
            op_code = BitcoinOP(byte).name
            return op_code
        except ValueError:
            if int(byte) >= 1 and int(byte) <= 75:
                return "OP_PUSHBYTES_" + byte
            else:
                return BitcoinOP.OP_INVALIDOPCODE.name
    
    @classmethod
    def convert_op_to_byte(self, op_code) -> str:
        try:
            byte = BitcoinOP[op_code]
            return byte.value
        except:
            if len(op_code) > 1:
                last_char = op_code[len(op_code) - 2:]
                if int(last_char) >= 1 and int(last_char) <= 75:
                    last_char_str = str(hex(int(last_char)))[2:]
                    return last_char_str
            return BitcoinOP.OP_INVALIDOPCODE.value

class InscriptionFileType(Enum):
    js = "6170706C69636174696F6E2F6A617661736372697074"
    json = "6170706C69636174696F6E2F6A736F6E"
    pdf = "6170706C69636174696F6E2F706466"
    sig = "6170706C69636174696F6E2F7067702D7369676E6174757265"
    yaml = "6170706C69636174696F6E2F79616D6C"
    flac = "617564696F2F666C6163"
    mpg = "617564696F2F6D706567"
    wav = "617564696F2F776176"
    apng = "696D6167652F61706E67"
    avif = "696D6167652F61766966"
    gif = "696D6167652F676966"
    jpeg = "696D6167652F6A706567"
    jpg = "696D6167652F6A7067"
    png = "696D6167652F706E67"
    svg = "696D6167652F7376672B786D6C"
    webp = "696D6167652F77656270"
    gltf = "6D6F64656C2F676C74662D62696E617279"
    stl = "6D6F64656C2F73746C"
    html = "746578742F68746D6C3B636861727365743D7574662D38"
    txt = "746578742F706C61696E3B636861727365743D7574662D38"
    mp4 = "766964656F2F6D7034"
    webm = "766964656F2F7765626D"

    @classmethod
    def convert_hexType_to_suffix(self, hexCode) -> str:
        try:
            op_code = InscriptionFileType(hexCode)
            return op_code.name
        except ValueError:
            return "Error"