from enum import Enum

class BitcoinOP(Enum):
    """
    This is a class that inherits from Enum. It contains a list of individual OP_CODEs and their hexadecimal values.
    The methods of this class are used to convert from hexadecimal to OP_CODE names and vice versa.
    
        :cvar OP_0 str: 00
        :cvar OP_PUSHDATA str: 4c
        :cvar OP_PUSHDATA2 str: 4d
        :cvar OP_PUSHDATA4 str: 4e
        :cvar OP_1NEGATE str: 4f
        :cvar OP_1 str: 51
        :cvar OP_2 str: 52
        :cvar OP_3 str: 53
        :cvar OP_4 str: 54
        :cvar OP_5 str: 55
        :cvar OP_6 str: 56
        :cvar OP_7 str: 57
        :cvar OP_8 str: 58
        :cvar OP_9 str: 59
        :cvar OP_10 str: 5a
        :cvar OP_11 str: 5b
        :cvar OP_12 str: 5c
        :cvar OP_13 str: 5d
        :cvar OP_14 str: 5e
        :cvar OP_15 str: 5f
        :cvar OP_16 str: 60
        :cvar OP_NOP str: 61
        :cvar OP_IF str: 63
        :cvar OP_NOTIF str: 64
        :cvar OP_ELSE str: 67
        :cvar OP_ENDIF str: 68
        :cvar OP_VERIFY str: 69
        :cvar OP_RETURN str: 6a
        :cvar OP_TOALTSTACK str: 6b
        :cvar OP_FROMALTSTACK str: 6c
        :cvar OP_2DROP str: 6d
        :cvar OP_2DUP str: 6e
        :cvar OP_3DUP str: 6f
        :cvar OP_2OVER str: 70
        :cvar OP_2ROT str: 71
        :cvar OP_2SWAP str: 72
        :cvar OP_IFDUP str: 73
        :cvar OP_DEPTH str: 74
        :cvar OP_DROP str: 75
        :cvar OP_DUP str: 76
        :cvar OP_NIP str: 77
        :cvar OP_OVER str: 78
        :cvar OP_PICK str: 79
        :cvar OP_ROLL str: 7a
        :cvar OP_ROT str: 7b
        :cvar OP_SWAP str: 7c
        :cvar OP_TUCK str: 7d
        :cvar OP_CAT str: 7e
        :cvar OP_SUBSTR str: 7f
        :cvar OP_LEFT str: 80
        :cvar OP_RIGHT str: 81
        :cvar OP_SIZE str: 82
        :cvar OP_INVERT str: 83
        :cvar OP_AND str: 84
        :cvar OP_OR str: 85
        :cvar OP_XOR str: 86
        :cvar OP_EQUAL str: 87
        :cvar OP_EQUALVERIFY str: 88
        :cvar OP_RESERVED1 str: 89
        :cvar OP_RESERVED2 str: 8a
        :cvar OP_1ADD str: 8b
        :cvar OP_1SUB str: 8c
        :cvar OP_2MUL str: 8d
        :cvar OP_2DIV str: 8e
        :cvar OP_NEGATE str: 8f
        :cvar OP_ABS str: 90
        :cvar OP_NOT str: 91
        :cvar OP_0NOTEQUAL str: 92
        :cvar OP_ADD str: 93
        :cvar OP_SUB str: 94
        :cvar OP_MUL str: 95
        :cvar OP_DIV str: 96
        :cvar OP_MOD str: 97
        :cvar OP_LSHIFT str: 98
        :cvar OP_RSHIFT str: 99
        :cvar OP_BOOLAND str: 9a
        :cvar OP_BOOLOR str: 9b
        :cvar OP_NUMEQUAL str: 9c
        :cvar OP_NUMEQUALVERIFY str: 9d
        :cvar OP_NUMNOTEQUAL str: 9e
        :cvar OP_LESSTHAN str: 9f
        :cvar OP_GREATERTHAN str: a0
        :cvar OP_LESSTHANOREQUAL str: a1
        :cvar OP_GREATERTHANOREQUAL str: a2
        :cvar OP_MIN str: a3
        :cvar OP_MAX str: a4
        :cvar OP_WITHIN str: a5
        :cvar OP_RIPEMD160 str: a6
        :cvar OP_SHA1 str: a7
        :cvar OP_SHA256 str: a8
        :cvar OP_HASH160 str: a9
        :cvar OP_HASH256 str: aa
        :cvar OP_CODESEPARATOR str: ab
        :cvar OP_CHECKSIG str: ac
        :cvar OP_CHECKSIGVERIFY str: ad
        :cvar OP_CHECKMULTISIG str: ae
        :cvar OP_CHECKMULTISIGVERIFY str: af
        :cvar OP_NOP1 str: b0
        :cvar OP_NOP2 str: b1
        :cvar OP_CHECKLOCKTIMEVERIFY str: b1
        :cvar OP_NOP3 str: b2
        :cvar OP_CHECKSEQUENCEVERIFY str: b2
        :cvar OP_NOP4 str: b3
        :cvar OP_NOP5 str: b4
        :cvar OP_NOP6 str: b5
        :cvar OP_NOP7 str: b6
        :cvar OP_NOP8 str: b7
        :cvar OP_NOP9 str: b8
        :cvar OP_NOP10 str: b9
        :cvar OP_INVALIDOPCODE str: ff
    """
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
    def convert_byte_to_op(self: object, hex: str) -> str:
        """
        This is a class method that accepts a hex representation of a byte and returns it in the form of an OP_CODE string            

            :param self object: since this is a class method, there is no need to create an instance for the call. Can be called with -> BitcoinOP.convert_byte_to_op()
            :param hex str: Hex representation of the OP_CODE value for evaluation in string form
            
            :returns: OP_CODE name of input hex byte
            :rtype: str 
        """
        try:
            op_code = BitcoinOP(hex).name
            return op_code
        except ValueError:
            if int(hex) >= 1 and int(hex) <= 75:
                return "OP_PUSHBYTES_" + hex
            else:
                return BitcoinOP.OP_INVALIDOPCODE.name
    
    @classmethod
    def convert_op_to_byte(self: object, op_code: str) -> str:
        """
        This is a class method that accepts the hexadecimal representation of a byte as a string and also returns a string containing the hexadecimal value

            :param self object: since this is a class method, there is no need to create an instance for the call. Can be called with -> BitcoinOP.convert_op_to_byte()
            :param op_code str: OP_CODE name for subsequent evaluation
            
            :returns: hex byte value in string of input OP_CODE name
            :rtype: str 
        """
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
    """
    This is a class that inherits from Enum. Contains a list of individual file suffixes and their hexadecimal representation within the inscription type.
    The methods of this class are used to convert from a simple file suffix to an inscriptions standard type and vice versa    

        :cvar js str: 6170706C69636174696F6E2F6A617661736372697074
        :cvar json str: 6170706C69636174696F6E2F6A736F6E
        :cvar pdf str: 6170706C69636174696F6E2F706466
        :cvar sig str: 6170706C69636174696F6E2F7067702D7369676E6174757265
        :cvar yaml str: 6170706C69636174696F6E2F79616D6C
        :cvar flac str: 617564696F2F666C6163
        :cvar mpg str: 617564696F2F6D706567
        :cvar wav str: 617564696F2F776176
        :cvar apng str: 696D6167652F61706E67
        :cvar avif str: 696D6167652F61766966
        :cvar gif str: 696D6167652F676966
        :cvar jpeg str: 696D6167652F6A706567
        :cvar jpg str: 696D6167652F6A7067
        :cvar png str: 696D6167652F706E67
        :cvar svg str: 696D6167652F7376672B786D6C
        :cvar webp str: 696D6167652F77656270
        :cvar gltf str: 6D6F64656C2F676C74662D62696E617279
        :cvar stl str: 6D6F64656C2F73746C
        :cvar html str: 746578742F68746D6C3B636861727365743D7574662D38
        :cvar txt str: 746578742F706C61696E3B636861727365743D7574662D38
        :cvar mp4 str: 766964656F2F6D7034
        :cvar webm str: 766964656F2F7765626D
    """

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
    def convert_hexType_to_suffix(self: object, hexCode: str) -> str:
        """
        This is a class method that accepts the hexadecimal representation of a inscription type as a string and also returns a string containing the file suffix value

            :param self object: since this is a class method, there is no need to create an instance for the call. Can be called with -> InscriptionFileType.convert_hexType_to_suffix()
            :param hexCode str: hex representation in string format defining the inscription type
            
            :returns: suffix of the file to save the inscription belonging to the given type or value Error
            :rtype: str
        
        """
        try:
            op_code = InscriptionFileType(hexCode)
            return op_code.name
        except ValueError:
            return "Error"
        
    @classmethod
    def convert_suffix_to_hexType(self: object, suffix: str) -> str:
        """
        This is a class method that accepts the suffix of file and return a string contain hex representation of inscription type of the given suffix

            :param self object: since this is a class method, there is no need to create an instance for the call. Can be called with -> InscriptionFileType.convert_suffix_to_hexType()
            :param suffix str: suffix of the given file type with inscription
            
            :returns: hex representation of the given media type according to the inscription standard
            :rtype: str
        """
        try:
            suffix = BitcoinOP[suffix]
            return suffix.value
        except ValueError:
            return "Error"