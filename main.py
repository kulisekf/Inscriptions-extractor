import os
import hashlib
import sys
from io import BufferedReader
import argparse

##přečte určitý počet bajtů, změní little-endian notaci na notmální
def read_bytes(file:BufferedReader,n:int,byte_order:str = 'L')->str:
    data = file.read(n)
    if byte_order == 'L':
        data = data[::-1]
    data = data.hex().upper()
    return data

##bajt může značit více věcí - zde se rozhoduje, zda samotný bajt je výsledná hodnota, či zda značí kolik následujících bajtů hodnotu obsahuje
def read_varint(file:BufferedReader)->str:
    b = file.read(1)
    bInt = int(b.hex(),16)
    data = ''
    if bInt < 253:
        c = 0
        data = b.hex().upper()
    if bInt == 253: c = 2
    if bInt == 254: c = 4
    if bInt == 255: c = 8
    for j in range(0,c):
        b = file.read(1)
        b = b.hex().upper()
        data = b + data
    return data

##funguje stejně, jako předchozí. S tím rozdílem, že je třeba uchovat a returnnout všechna data - použita pro výpočet transaction hashe
def read_varint_transaction(file:BufferedReader)->str:
    b = file.read(1)
    tmpB = b.hex().upper()
    bInt = int(b.hex(),16)
    tmpHex = ''
    if bInt < 253:
        c = 0
        tmpHex = b.hex().upper()
        tmpB = ''
    if bInt == 253: c = 2
    if bInt == 254: c = 4
    if bInt == 255: c = 8
    for j in range(0,c):
        b = file.read(1)
        b = b.hex().upper()
        tmpHex = b + tmpHex
    return tmpHex, tmpB

##z little-endian stringu udělá big-endian
def reverse(input:str)->str:
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
        return Res

def find_block(blockHash:str, DIR:str)->list:
    ##nacte slozku a nasledne vsechny soubory do listu
    fList = os.listdir(DIR)
    fList = [x for x in fList if (x.endswith('.dat') and x.startswith('blk'))]
    fList.sort(reverse=True) ##seřadí list sestupně - inscriptions budou spíše v novějších blocích
    ## postupně projde všechny soubory
    for i in fList:
        ##otevře daný soubor
        nameSrc = i
        f = open(DIR + nameSrc,'rb')
        fSize = os.path.getsize(DIR + nameSrc)
        zacatekBloku = 0
        velikostBloku = 1
        #prochází soubor (každý blok), dokud nenarazí na konec souboru, nebo dokud nenajde hledaný blok - pokud najde, vrátí název souboru a pozici v něm, kde začíná hledaný blok
        while f.tell() != fSize and velikostBloku != 0: #velikost bloku pro to, že poslední soubor (ten do kterého se aktuálně zapisují nové bloky) mi to bez tohoto pravidla procházelo i po přečtení nejaktuálnějšího bloku - jednoduše to skákalo po 8 bajtech
            zacatekBloku = f.tell()
            f.seek(zacatekBloku + 4) ##přeskočí magic number            
            velikostBloku = int(read_bytes(f,4), base=16)##načte velikost bloku - konvertovaná do bajtů
            hlavickaBloku = read_bytes(f,80,'B')
            hlavickaBlokuHash = hash_of_data(hlavickaBloku) #vypočítá hash nalezeného bloku
            if hlavickaBlokuHash.__eq__(blockHash):
                f.close()
                return [i, str(zacatekBloku)]
            taproot_activated_block(hlavickaBlokuHash) #ověří, zda nebyl dosažen aktivační Taproot blok - pokud ano zastaví program
            f.seek(velikostBloku + zacatekBloku + 8,0)#přesun na (konec bloku + 1) - není to přímo začátek dalšího bloku, před ním je ještě magic number a velikost bloku
        f.close()          
    raise Exception(f"Error: Non-exist block hash") ##pokud prošel všechny soubory a požadovaný blockhash nenalezl - neexistuje

#přečte hlavičku bloku a vypočítá block hash
def hash_of_data(data:str)->str:
    ##vypocita hash bloku (jeho hlavicky - veliká 80 bajtů)
    data = bytes.fromhex(data)
    data = hashlib.new('sha256', data).digest()
    data = hashlib.new('sha256', data).digest()
    data = data[::-1]        
    data = data.hex().upper()
    return data

#kontroluje, zda nalezený blok neodpovídá prvnímu taproot bloku - díky taprootu jsou možné inscriptions
def taproot_activated_block(blockHash:str)->None:
    if blockHash == '0000000000000000000687BCA986194DC2C1F949318629B44BB54EC0A94D8244':
        print("Block 709,632 reached (Taproot activated block), continue search? (Y/N)")
        stop = str(input())
        while stop != "N" and stop != "Y":
            print("Wrong value was entered! continue search? (Y/N)\n ->")
            stop = str(input())
        if stop == "Y":
            sys.exit("Search stopped")

##pokusí se najít zadanou transakci. Pokus ji nenajde, vrátí text chyby, pokud ji najde a transakce obsahuje
#witness, vrátí lokaci witness a počet vstupů, pokud witness nebosahuje vrátí text chyby
def find_transaction(fileName:str, zacatekBloku:str, txHash:str, DIR:str)->list:
    f = open(DIR + fileName,'rb') ##otevře správný soubor
    f.seek(int(zacatekBloku) + 8 + 80) ##přeskočí na začátek bloku, následně za magicnumber a size a nakonec za celou hlavičku - následuje pro čtení hodnota tx count
    txCount = int(read_varint(f),16)##zjisti mnozstvi transakci v bloku - převede z hexadecimal na decimal
    for k in range(txCount):
        RawTX = reverse(read_bytes(f,4)) ## obsahuje TX version number
        Witness, inCount, tmpHex = tx_in_count(f) ##zjistí počet vstupů do transakce, vyhodnotí případný segwit flag a zároveň vrátí i hodnotu pro RawTX
        RawTX += reverse(tmpHex)

        ## projdou se všechny vstupy a přidají se do RawTX
        for m in range(inCount):
            RawTX += read_tx_in(f)

        ## zde se zjišťuje počet outputů
        tmpHex, tmpB = read_varint_transaction(f)
        outputCount = int(tmpHex,16)
        RawTX += reverse(tmpHex + tmpB)

        ## projdou se všechny výstupy transakce
        for m in range(outputCount):
            RawTX += read_tx_out(f)

        zacatekWitness = f.tell()
        ##postupně přeskočí celou witness část transakce
        if Witness == True:
            skip_witness(f, inCount)

        RawTX += reverse(read_bytes(f,4)) ##hodnota Lock time, reversnutá a přidaná
        RawTXHash = hash_of_data(RawTX)        ## z Rawtx udělá její hash

        ## zjistí, zda nalezl správnou transakci
        if txHash == RawTXHash:
            if Witness == True:
                f.close()
                return [zacatekWitness, inCount] 
            else:
                raise Exception(f"Error: The entered transaction does not contain the witness part")
    f.close()
    raise Exception(f"Error: Non-exist TX hash in this block")

##zjistí počet vstupů do transakce, vyhodnotí případný segwit flag a zároveň vrátí i hodnotu pro RawTX
def tx_in_count(f:BufferedReader)->bool|int|str:
    Witness = False
    b = f.read(1)
    tmpB = b.hex().upper()
    bInt = int(b.hex(),16)
    tmpHex = ''
    if bInt == 0:
        tmpB = ''
        f.seek(1,1)
        c = f.read(1)
        bInt = int(c.hex(),16)
        tmpB = c.hex().upper()
        Witness = True
    if bInt < 253:
        c = 0
        tmpHex = hex(bInt)[2:].upper().zfill(2)
        tmpB = ''
    if bInt == 253: c = 2
    if bInt == 254: c = 4
    if bInt == 255: c = 8
    for j in range(0,c):
        b = f.read(1)
        b = b.hex().upper()
        tmpHex = b + tmpHex
        
    inCount = int(tmpHex,16)## obsahuje počet vstupů do transakce
    
    tmpHex = tmpHex + tmpB
    return Witness, inCount, tmpHex

#přeskočí celou witness část dat při průchodu transakcí
def skip_witness(f:BufferedReader, inCount:int)->None:
    for m in range(inCount): ##pro každý vstup
        WitnessLength = int(read_varint(f),16) ##zjistí počet prvků ve witness
        for j in range(WitnessLength): #pro každý prvek ve witness
            WitnessItemLength = int(read_varint(f),16) ##zjistí délku prvku
            f.seek(WitnessItemLength, 1) ##přeskočí celý witness prvek

#projde celý vstup transakce a vrátí jeho data pro použití v RawTX
def read_tx_in(f:BufferedReader)->str:
    tmpHex = read_bytes(f,32) ## txid (hash) předchozí tx
    RawTX = reverse(tmpHex)
    
    tmpHex = read_bytes(f,4) ## index výstupu předchozí tx            
    RawTX += reverse(tmpHex)
    ##v předsegwitových tx je na tomto místě podpisový skript, zde prázdné - je ve witness -> načte tuto část
    tmpHex, tmpB = read_varint_transaction(f)
        
    scriptLength = int(tmpHex,16)
    tmpHex = tmpHex + tmpB
    RawTX += reverse(tmpHex)
    tmpHex = read_bytes(f,scriptLength,'B')
    RawTX += tmpHex
    ## sequence - časový zámek/RBF
    tmpHex = read_bytes(f,4,'B')
    RawTX += tmpHex
    return RawTX

def read_tx_out(f:BufferedReader)->str:
    ## value v sat
    tmpHex = read_bytes(f,8)
    ## následující část čte scriptPubKey
    RawTX = reverse(tmpHex)
    tmpHex = ''
    tmpHex, tmpB = read_varint_transaction(f)

    scriptLength = int(tmpHex,16)
    tmpHex = tmpHex + tmpB
    RawTX = RawTX + reverse(tmpHex)
    tmpHex = read_bytes(f,scriptLength,'B')
    RawTX = RawTX + tmpHex
    tmpHex = ''
    return RawTX

##projde všechna witness transakce, pokusí se najít správné - rozhoduje dle prefixu odpovídajícímu inscription
def find_inscription(fileName:str, zacatekWitness:str, inCount:str, DIR:str)->list:
    f = open(DIR + fileName,'rb')
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
        f.close()
        inscription += tmpHex
        tmpHex = ''

        inscription = inscription[68:] ##smažu část witness - signature a OP_CHECKSIG
        
        ## z ničeho nic se to objevilo, zatím jsem nenašel co to má být, tak prostě přeskakuji
        if inscription[0:2] == "06":
            inscription = inscription[16:]
        ## zjistí, zda se jedná o inscriptions - shodný prefix
        if inscription[0:16] == "0063036F72640101":
            return extract_inscription(inscription)
    raise Exception(f"Error: Transaction does not contain inscription")

##pokud se ve witness datech podařilo najít část s inscriptions, projde zbytek a vyextrahuje čistě inscription data zde uložená
def extract_inscription(inscription:str)->list:
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
    return [type, inscription_final]

##zjistí, kolik bajtů obsahuje data + kolik bajtů nese tuto informaci
def length_reader(inscription:str)->int:
    b = inscription[0:2]
    if b.__eq__('4C'):
        return int(reverse(inscription[2:4]), 16), 4
    elif b.__eq__('4D'):
        return int(reverse(inscription[2:6]), 16), 6
    else:
        return int(reverse(inscription[0:2]), 16), 2

##zjistí typ inscriptions a uloží ho do správného souboru
def save_inscription(type:str, inscription:str, result_dir:str)->None:
    if type.__eq__('6170706C69636174696F6E2F6A617661736372697074'): #application/javascript
        save_file("js", bytes.fromhex(inscription), result_dir) 
    if type.__eq__('6170706C69636174696F6E2F6A736F6E'): #application/json
        save_file("json", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('6170706C69636174696F6E2F706466'): #application/pdf
        save_file("pdf", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('6170706C69636174696F6E2F7067702D7369676E6174757265'): #application/pgp-signature
        save_file("sig", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('6170706C69636174696F6E2F79616D6C'): #application/yaml
        save_file("yaml", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('617564696F2F666C6163'): #audio/flac
        save_file("flac", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('617564696F2F6D706567'): #audio/mpeg
        save_file("mpg", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('617564696F2F776176'): #audio/wav
        save_file("wav", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('696D6167652F61706E67'): #image/apng
        save_file("apng", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('696D6167652F61766966'): #image/avif
        save_file("avif", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('696D6167652F676966'): #image/gif
        save_file("gif", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('696D6167652F6A706567'): #image/jpeg
        save_file("jpeg", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('696D6167652F6A7067'): #image/jpg
        save_file("jpg", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('696D6167652F706E67'): #image/png
        save_file("png", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('696D6167652F7376672B786D6C'): #image/svg+xml
        save_file("svg", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('696D6167652F77656270'): #image/webp
        save_file("webp", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('6D6F64656C2F676C74662D62696E617279'): #model/gltf-binary
        save_file("gltf", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('6D6F64656C2F73746C'): #model/stl
        save_file("stl", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('746578742F68746D6C3B636861727365743D7574662D38'): #text/html;charset=utf-8
        save_file("html", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('746578742F706C61696E3B636861727365743D7574662D38'): #text/plain;charset=utf-8
        save_file("txt", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('766964656F2F6D7034'): #video/mp4
        save_file("mp4", bytes.fromhex(inscription), result_dir) 
    elif type.__eq__('766964656F2F7765626D'): #video/webm
        save_file("webm", bytes.fromhex(inscription), result_dir) 
    else:
        data = bytes("!!!unknown type of content!!!\n\ntype: ",'UTF-8') + bytes.fromhex(type) + bytes("\n\ninscription data: " + inscription,'UTF-8')
        save_file("txt", data, result_dir) 
    
def save_file(suffix:str, data:bytes, result_dir:str)->None:
    with open(result_dir + '/inscription.' + suffix, 'wb') as file:
            file.write(data)

def what_to_find()->list:
    parser = argparse.ArgumentParser(description='Extract inxcription from block')

    parser.add_argument('-blkHash', required=True, help="hash of block with inscription transaction (required)")
    parser.add_argument('-txHash', required=True, help="transaction hash of transaction with inscription (required)")
    parser.add_argument('-blkDir', default='./.bitcoin/blocks', help="path to the block folder (default: './.bitcoin/blocks')")
    parser.add_argument('-resDir', default='./', help="path to the folder for file save (default: './')")
    args = parser.parse_args()
    DIR = args.blkDir + "/"

    if len(args.blkHash) != 64:
        raise Exception(f"Error: Wrong blkHash value was entered! The hash length does not conform to the standard")
    if len(args.txHash) != 64:
        raise Exception(f"Error: Wrong txHash value was entered! The hash length does not conform to the standard")
    return [args.blkHash.upper(), args.txHash.upper(), DIR, args.resDir]
 
def main():
    try:
        coordinates = what_to_find() ##list blockhash, transaction hash
        whereIsBlock = find_block(coordinates[0], coordinates[2]) ## list nazev souboru .blk ve kterem je hlevany blok, pozice kde blok zacina (pred magicnumber a size)
        whereIsTransactionWitness = find_transaction(whereIsBlock[0], whereIsBlock[1], coordinates[1], coordinates[2]) ##najde zacatek transakce
        finalInscription = find_inscription(whereIsBlock[0], whereIsTransactionWitness[0], whereIsTransactionWitness[1], coordinates[2])
        save_inscription(finalInscription[0], finalInscription[1], coordinates[3])
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()