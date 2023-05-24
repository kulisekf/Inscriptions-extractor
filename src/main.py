import argparse
from modules import WorkWithBlock
from modules import WorkWithTransaction
from modules import WorkWithInscription


def what_to_find()->list:
    """
    This function, using argparse, loads the necessary data entered into the terminal when the application is started and returns for their subsequent use

        :returns: A list containing 4 values. In this order - the block hash of the block that contains the inscription, the hash of the transaction that contains the inscription, the path to the folder that contains the blkXXXX.dat files and the path to the folder where the inscription is to be stored

        :rtype: list of strings
    """
    parser = argparse.ArgumentParser(description='Extract inscription from block')

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
    """
    The main function, which sequentially calls individual sub-parts while the program is running. At the same time, exception catching is performed at this level

        :returns: None

    """
    try:
        coordinates = what_to_find() ##list blockhash, transaction hash
        whereIsBlock = WorkWithBlock.find_block(coordinates[0], coordinates[2]) ## list nazev souboru .blk ve kterem je hlevany blok, pozice kde blok zacina (pred magicnumber a size)
        whereIsTransactionWitness = WorkWithTransaction.find_transaction(whereIsBlock[0], whereIsBlock[1], coordinates[1], coordinates[2]) ##najde zacatek transakce
        finalInscription = WorkWithInscription.find_inscription(whereIsBlock[0], whereIsTransactionWitness[0], whereIsTransactionWitness[1], coordinates[2])
        WorkWithInscription.save_inscription(finalInscription[0], finalInscription[1], coordinates[3])
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()