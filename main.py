##https://github.com/ragestack/blockchain-parser

import os
import hashlib
import sys
dir = './.bitcoin/blocks/'

##přečte určitý počet bajtů, změní little-endian notaci na notmální
def read_bytes(file,n,byte_order = 'L'):
    data = file.read(n)
    if byte_order == 'L':
        data = data[::-1]
    data = data.hex().upper()
    return data

##bajt může značit více věcí - zde se rozhoduje, zda samotný bajt je výsledná hodnota, či zda značí kolik následujících bajtů hodnotu obsahuje
def read_varint(file):
    b = file.read(1)
    bInt = int(b.hex(),16)
    c = 0
    data = ''
    if bInt < 253:
        c = 1
        data = b.hex().upper()
    if bInt == 253: c = 3
    if bInt == 254: c = 5
    if bInt == 255: c = 9
    ##jelikož se jde od 1 do c, výslednou hodnotu obsahuje c-1 bajtu
    for j in range(1,c):
        b = file.read(1)
        b = b.hex().upper()
        data = b + data
    return data

##z little-endian stringu udělá big-endian
def reverse(input):
    L = len(input)
    if (L % 2) != 0:
        return None
    else:
        Res = ''
        L = L // 2
        for i in range(L):
            T = input[i*2] + input[i*2+1]
            Res = T + Res
            T = ''
        return (Res)

def find_block(blockHash:str):
    ##nacte slozku a nasledne vsechny soubory do listu
    fList = os.listdir(dir)
    fList = [x for x in fList if (x.endswith('.dat') and x.startswith('blk'))]
    ##seřadí list sestupně - inscriptions budou spíše v novějších blocích
    fList.sort(reverse=True)
    ## postupně projde všechny soubory
    for i in fList:
        ##otevře daný soubor
        nameSrc = i
        t = dir + nameSrc
        f = open(t,'rb')
        #prochází, dokud nenarazí na konec souboru
        fSize = os.path.getsize(t)
        zacatekBloku = 0
        velikostBloku = 1
        while f.tell() != fSize and velikostBloku != 0:
            ##zacatek bloku
            zacatekBloku = f.tell()
            f.seek(zacatekBloku + 4) ##přeskočí magic number
            
            ##načte velikost bloku - konvertovaná do bajtů
            velikostBloku = int(read_bytes(f,4), base=16)

            ##vypocita hash bloku (jeho hlavicky - veliká 80 bajtů)
            hlavickaBloku = read_bytes(f,80,'B')
            hlavickaBloku = bytes.fromhex(hlavickaBloku)
            hlavickaBloku = hashlib.new('sha256', hlavickaBloku).digest()
            hlavickaBloku = hashlib.new('sha256', hlavickaBloku).digest()
            hlavickaBloku = hlavickaBloku[::-1]        
            hlavickaBloku = hlavickaBloku.hex().upper()
            if hlavickaBloku.__eq__(blockHash):
                return [i, str(zacatekBloku)]
            if hlavickaBloku == '0000000000000000000687BCA986194DC2C1F949318629B44BB54EC0A94D8244':
                print("Block 709,632 (Taproot activated block), continue search? (Y/N)")
                stop = str(input())
                while stop != "N" and stop != "Y":
                    print("Wrong value was entered! continue search? (Y/N)\n ->")
                    stop = str(input())
                if stop == "Y":
                    sys.exit("Search stopped")
            ##přesun na konec bloku + 1 
            # (není to přímo začátek dalšího bloku, před ním je ještě magic number a velikost bloku)
            f.seek(velikostBloku + zacatekBloku + 8,0)
        f.close()
    ##pokud prošel všechny soubory a požadovaný blockhash nenalezl - neexistuje
    raise Exception(f"Error: Non-exist block hash")

##pokusí se najít zadanou transakci. Pokus ji nenajde, vrátí text chyby, pokud ji najde a transakce obsahuje
#witness, vrátí lokaci witness a počet vstupů, pokud witness nebosahuje vrátí text chyby
def find_transaction(fileName, zacatekBloku, txHash):
    f = open(dir + fileName,'rb') ##otevře správný soubor
    f.seek(int(zacatekBloku) + 8 + 80) ##přeskočí na začátek bloku, následně za magicnumber a size a nakonec za celou hlavičku - následuje pro čtení hodnota tx count
    txCount = int(read_varint(f),16)##zjisti mnozstvi transakci v bloku - převede z hexadecimal na decimal

    for k in range(txCount):
        RawTX = reverse(read_bytes(f,4)) ## obsahuje TX version number

        ##segwit marker
        Witness = False
        b = f.read(1)
        tmpB = b.hex().upper()
        bInt = int(b.hex(),16)
        if bInt == 0:
            tmpB = ''
            f.seek(1,1)
            c = f.read(1)
            bInt = int(c.hex(),16)
            tmpB = c.hex().upper()
            Witness = True
        if bInt < 253:
            c = 1
            tmpHex = hex(bInt)[2:].upper().zfill(2)
            tmpB = ''
        if bInt == 253: c = 3
        if bInt == 254: c = 5
        if bInt == 255: c = 9
        for j in range(1,c):
            b = f.read(1)
            b = b.hex().upper()
            tmpHex = b + tmpHex
            
        inCount = int(tmpHex,16)## obsahuje počet vstupů do transakce
        
        tmpHex = tmpHex + tmpB
        RawTX = RawTX + reverse(tmpHex)

        ## projdou se všechny vstupy
        for m in range(inCount):
            ## txid (hash) předchozí tx
            tmpHex = read_bytes(f,32) 
            RawTX = RawTX + reverse(tmpHex)
            ## index výstupu předchozí tx
            tmpHex = read_bytes(f,4)                
            RawTX = RawTX + reverse(tmpHex)
            ##v předsegwitových tx je na tomto místě podpisový skript, zde prázdné - je ve witness
            tmpHex = ''
            b = f.read(1)
            tmpB = b.hex().upper()
            bInt = int(b.hex(),16)
            c = 0
            if bInt < 253:
                c = 1
                tmpHex = b.hex().upper()
                tmpB = ''
            if bInt == 253: c = 3
            if bInt == 254: c = 5
            if bInt == 255: c = 9
            for j in range(1,c):
                b = f.read(1)
                b = b.hex().upper()
                tmpHex = b + tmpHex
            scriptLength = int(tmpHex,16)
            tmpHex = tmpHex + tmpB
            RawTX = RawTX + reverse(tmpHex)
            tmpHex = read_bytes(f,scriptLength,'B')
            RawTX = RawTX + tmpHex
            ## sequence - časový zámek/RBF
            tmpHex = read_bytes(f,4,'B')
            RawTX = RawTX + tmpHex
            tmpHex = ''
        ## zde se zjišťuje počet outputů
        b = f.read(1)
        tmpB = b.hex().upper()
        bInt = int(b.hex(),16)
        c = 0
        if bInt < 253:
            c = 1
            tmpHex = b.hex().upper()
            tmpB = ''
        if bInt == 253: c = 3
        if bInt == 254: c = 5
        if bInt == 255: c = 9
        for j in range(1,c):
            b = f.read(1)
            b = b.hex().upper()
            tmpHex = b + tmpHex
        outputCount = int(tmpHex,16)
        tmpHex = tmpHex + tmpB
        RawTX = RawTX + reverse(tmpHex)
        ## projdou se všechny výstupy transakce
        for m in range(outputCount):
            ## value v sat
            tmpHex = read_bytes(f,8)
            ## následující část čte scriptPubKey
            RawTX = RawTX + reverse(tmpHex)
            tmpHex = ''
            b = f.read(1)
            tmpB = b.hex().upper()
            bInt = int(b.hex(),16)
            c = 0
            if bInt < 253:
                c = 1
                tmpHex = b.hex().upper()
                tmpB = ''
            if bInt == 253: c = 3
            if bInt == 254: c = 5
            if bInt == 255: c = 9
            for j in range(1,c):
                b = f.read(1)
                b = b.hex().upper()
                tmpHex = b + tmpHex
            scriptLength = int(tmpHex,16)
            tmpHex = tmpHex + tmpB
            RawTX = RawTX + reverse(tmpHex)
            tmpHex = read_bytes(f,scriptLength,'B')
            RawTX = RawTX + tmpHex
            tmpHex = ''
        zacatekWitness = f.tell()
        ##postupně přeskočí celou witness část transakce
        if Witness == True:
            for m in range(inCount): ##pro každý vstup
                WitnessLength = int(read_varint(f),16) ##zjistí počet prvků ve witness
                for j in range(WitnessLength): #pro každý prvek ve witness
                    WitnessItemLength = int(read_varint(f),16) ##zjistí délku prvku
                    f.seek(WitnessItemLength, 1) ##přeskočí celý witness prvek

        RawTX = RawTX + reverse(read_bytes(f,4)) ##hodnota Lock time, reversnutá a přidaná
        ## z Raw tx udělá její hash
        RawTX = bytes.fromhex(RawTX)
        RawTX = hashlib.new('sha256', RawTX).digest()
        RawTX = hashlib.new('sha256', RawTX).digest()
        RawTX = RawTX[::-1]
        RawTX = RawTX.hex().upper()

        ## zjistí, zda nalezl správnou transakci
        if txHash == RawTX:
            if Witness == True:
                f.close()
                return [zacatekWitness, inCount] ##RawTX 
            else:
                raise Exception(f"Error: The entered transaction does not contain the witness part")
    f.close()
    raise Exception(f"Error: Non-exist TX hash in this block")

def extract_inscriptions(fileName, zacatekWitness, inCount):
    f = open(dir + fileName,'rb')
    f.seek(zacatekWitness)
    inscription = ""
    ## pro každý ze vstupů - bude nejspíše 1, ale sichr je sichr
    for m in range(inCount):
        tmpHex = read_varint(f)

        #přeskočí první část witness - nepotřebuji, myslím že pubkey
        WitnessItemLength = int(read_varint(f),16)
        f.seek(WitnessItemLength, 1)

        ##načtu 2. část witness
        tmpHex = read_varint(f)
        WitnessItemLength = int(tmpHex,16)
        tmpHex = reverse(read_bytes(f,WitnessItemLength))
        inscription += tmpHex
        tmpHex = ''

        inscription = inscription[68:] ##smažu část witness - signature a OP_CHECKSIG
        ## zjistí, zda se jedná o inscriptions - shodný prefix
        if inscription[0:16] == "0063036F72640101":
            inscription = inscription[16:] ##odstraním prefix
            typeLength = int(inscription[0:2], base=16)*2+2 ##zjistim si délku popisu typu obsahu
            type = inscription[2:typeLength]  ##nactu typ obsahu
            inscription = inscription[typeLength+2:] ##ostranim typ obsahu
            inscription_final = ""
            ##dokud nebude string obsahující inscriptions data prázdný - kromě OP_ENDIF na konci, to tam nechávám
            while len(inscription) != 2:
                ##zjistí kolik bajtů obsahuje data, bajty s hodnotou odstraní a bajty s daty přesune
                segmentLength, byteOut = length_reader(inscription)
                inscription = inscription[byteOut:]
                inscription_final += inscription[0:segmentLength*2]
                inscription = inscription[segmentLength*2:]

            f.close()
            return [type, inscription_final]
        raise Exception(f"Error: Transaction does not contain inscription")

##zjistí, kolik bajtů obsahuje data + kolik bajtů nese tuto informaci
def length_reader(inscription):
    b = inscription[0:2]
    if b.__eq__('4C'):
        return int(reverse(inscription[2:4]), 16), 4
    elif b.__eq__('4D'):
        return int(reverse(inscription[2:6]), 16), 6
    else:
        return int(reverse(inscription[0:2]), 16), 2

##zjistí typ inscriptions a uloží ho do správného souboru
def save_inscription(type, inscription):
    if type.__eq__('6170706C69636174696F6E2F6A617661736372697074'): #application/javascript
        data = bytes.fromhex(inscription)
        with open('./result/inscription.js', 'wb') as file:
            file.write(data)
    if type.__eq__('6170706C69636174696F6E2F6A736F6E'): #application/json
        data = bytes.fromhex(inscription)
        with open('./result/inscription.json', 'wb') as file:
            file.write(data)
    elif type.__eq__('6170706C69636174696F6E2F706466'): #application/pdf
        data = bytes.fromhex(inscription)
        with open('./result/inscription.pdf', 'wb') as file:
            file.write(data)
    elif type.__eq__('6170706C69636174696F6E2F7067702D7369676E6174757265'): #application/pgp-signature
        data = bytes.fromhex(inscription)
        with open('./result/inscription.sig', 'wb') as file:
            file.write(data)
    elif type.__eq__('6170706C69636174696F6E2F79616D6C'): #application/yaml
        data = bytes.fromhex(inscription)
        with open('./result/inscription.yaml', 'wb') as file:
            file.write(data)
    elif type.__eq__('617564696F2F666C6163'): #audio/flac
        data = bytes.fromhex(inscription)
        with open('./result/inscription.flac', 'wb') as file:
            file.write(data)
    elif type.__eq__('617564696F2F6D706567'): #audio/mpeg
        data = bytes.fromhex(inscription)
        with open('./result/inscription.mpg', 'wb') as file:
            file.write(data)
    elif type.__eq__('617564696F2F776176'): #audio/wav
        data = bytes.fromhex(inscription)
        with open('./result/inscription.wav', 'wb') as file:
            file.write(data)
    elif type.__eq__('696D6167652F61706E67'): #image/apng
        data = bytes.fromhex(inscription)
        with open('./result/inscription.apng', 'wb') as file:
            file.write(data)
    elif type.__eq__('696D6167652F61766966'): #image/avif
        data = bytes.fromhex(inscription)
        with open('./result/inscription.avif', 'wb') as file:
            file.write(data)
    elif type.__eq__('696D6167652F676966'): #image/gif
        data = bytes.fromhex(inscription)
        with open('./result/inscription.gif', 'wb') as file:
            file.write(data)
    elif type.__eq__('696D6167652F6A706567'): #image/jpeg
        data = bytes.fromhex(inscription)
        with open('./result/inscription.jpeg', 'wb') as file:
            file.write(data)
    elif type.__eq__('696D6167652F6A7067'): #image/jpg
        data = bytes.fromhex(inscription)
        with open('./result/inscription.jpeg', 'wb') as file:
            file.write(data)
    elif type.__eq__('696D6167652F706E67'): #image/png
        data = bytes.fromhex(inscription)
        with open('./result/inscription.png', 'wb') as file:
            file.write(data)
    elif type.__eq__('696D6167652F7376672B786D6C'): #image/svg+xml
        data = bytes.fromhex(inscription)
        with open('./result/inscription.svg', 'wb') as file:
            file.write(data)
    elif type.__eq__('696D6167652F77656270'): #image/webp
        data = bytes.fromhex(inscription)
        with open('./result/inscription.webp', 'wb') as file:
            file.write(data)
    elif type.__eq__('6D6F64656C2F676C74662D62696E617279'): #model/gltf-binary
        data = bytes.fromhex(inscription)
        with open('./result/inscription.gltf', 'wb') as file:
            file.write(data)
    elif type.__eq__('6D6F64656C2F73746C'): #model/stl
        data = bytes.fromhex(inscription)
        with open('./result/inscription.stl', 'wb') as file:
            file.write(data)
    elif type.__eq__('746578742F68746D6C3B636861727365743D7574662D38'): #text/html;charset=utf-8
        f = open('./result/inscription.html','w')
        f.write(bytes.fromhex(inscription).decode('utf-8'))
        f.close()
    elif type.__eq__('746578742F706C61696E3B636861727365743D7574662D38'): #text/plain;charset=utf-8
        f = open('./result/inscription.txt','w')
        f.write(bytes.fromhex(inscription).decode('utf-8'))
        f.close()  
    elif type.__eq__('766964656F2F6D7034'): #video/mp4
        data = bytes.fromhex(inscription)
        with open('./result/inscription.mp4', 'wb') as file:
            file.write(data)
    elif type.__eq__('766964656F2F7765626D'): #video/webm
        data = bytes.fromhex(inscription)
        with open('./result/inscription.webm', 'wb') as file:
            file.write(data)
    else:
        f = open('./result/vysledek.txt','w')
        f.write("!!!unknown type of content!!!\n\n")
        f.write("type: " + bytes.fromhex(type).decode('utf-8'))
        f.write("\n\ninscription data: " + inscription)
        f.close()

def what_to_find():
    print("Enter the hash block of transaction with inscription:")
    blockHash = str(input())
    ##blockHash = "00000000000000000000b1bdfdb4a667d57b5e5890eebaea608f7bcc0fe9bd63"
    while len(blockHash) != 64:
        print("\tWrong value was entered! the hash length does not conform to the standard\nEnter the hash block of transaction with inscription:")
        blockHash = str(input())
    print("Enter the transaction hash of transaction with inscription")
    transactionHash = str(input())
    ##transactionHash = "52ed0a201a5b3bde92fe485e8550a78dd03dac71e7488eb61c1e8b5b4a779deb"
    while len(transactionHash) != 64:
        print("\tWrong value was entered! the hash length does not conform to the standard\nEnter the transaction hash of transaction with inscription")
        transactionHash = str(input())
    return [blockHash.upper(), transactionHash.upper()]


def main():
    try:
        coordinates = what_to_find() ##list blockhash, transaction hash
        whereIsBlock = find_block(coordinates[0]) ## list nazev souboru .blk ve kterem je hlevany blok, pozice kde blok zacina (pred magicnumber a size)
        whereIsTransactionWitness = find_transaction(whereIsBlock[0], whereIsBlock[1], coordinates[1]) ##najde zacatek transakce
        finalInscription = extract_inscriptions(whereIsBlock[0], whereIsTransactionWitness[0], whereIsTransactionWitness[1])
        save_inscription(finalInscription[0], finalInscription[1])
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()