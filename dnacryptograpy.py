from distutils.log import error
from msilib.schema import Binary
from operator import index
from collections import deque
from datetime import datetime


def indexTable(key):
    key = key - 1
    defaultTable = ["AAAA", "AAAC", "AAAG", "AAAT", "AACA", "AACC", "AACG", "AACT", "AAGA", "AAGC", "AAGG", "AAGT", "AATA", "AATC", "AATG", "AATT", "ACAA", "ACAC", "ACAG", "ACAT", "ACCA", "ACCC", "ACCG", "ACCT", "ACGA", "ACGC", "ACGG", "ACGT", "ACTA", "ACTC", "ACTG", "ACTT",
                    "CAAA", "CAAC", "CAAG", "CAAT", "CACA", "CACC", "CACG", "CACT", "CAGA", "CAGC", "CAGG", "CAGT", "CATA", "CATC", "CATG", "CATT", "CCAA", "CCAC", "CCAG", "CCAT", "CCCA", "CCCC", "CCCG", "CCCT", "CCGA", "CCGC", "CCGG", "CCGT", "CCTA", "CCTC", "CCTG", "CCTT",
                    "GAAA", "GAAC", "GAAG", "GAAT", "GACA", "GACC", "GACG", "GACT", "GAGA", "GAGC", "GAGG", "GAGT", "GATA", "GATC", "GATG", "GATT", "GCAA", "GCAC", "GCAG", "GCAT", "GCCA", "GCCC", "GCCG", "GCCT", "GCGA", "GCGC", "GCGG", "GCGT", "GCTA", "GCTC", "GCTG", "GCTT",
                    "TAAA", "TAAC", "TAAG", "TAAT", "TACA", "TACC", "TACG", "TACT", "TAGA", "TAGC", "TAGG", "TAGT", "TATA", "TATC", "TATG", "TATT", "TCAA", "TCAC", "TCAG", "TCAT", "TCCA", "TCCC", "TCCG", "TCCT", "TCGA", "TCGC", "TCGG", "TCGT", "TCTA", "TCTC", "TCTG", "TCTT",
                    "AGAA", "AGAC", "AGAG", "AGAT", "AGCA", "AGCC", "AGCG", "AGCT", "AGGA", "AGGC", "AGGG", "AGGT", "AGTA", "AGTC", "AGTG", "AGTT", "ATAA", "ATAC", "ATAG", "ATAT", "ATCA", "ATCC", "ATCG", "ATCT", "ATGA", "ATGC", "ATGG", "ATGT", "ATTA", "ATTC", "ATTG", "ATTT",
                    "CGAA", "CGAC", "CGAG", "CGAT", "CGCA", "CGCC", "CGCG", "CGCT", "CGGA", "CGGC", "CGGG", "CGGT", "CGTA", "CGTC", "CGTG", "CGTT", "CTAA", "CTAC", "CTAG", "CTAT", "CTCA", "CTCC", "CTCG", "CTCT", "CTGA", "CTGC", "CTGG", "CTGT", "CTTA", "CTTC", "CTTG", "CTTT",
                    "GGAA", "GGAC", "GGAG", "GGAT", "GGCA", "GGCC", "GGCG", "GGCT", "GGGA", "GGGC", "GGGG", "GGGT", "GGTA", "GGTC", "GGTG", "GGTT", "GTAA", "GTAC", "GTAG", "GTAT", "GTCA", "GTCC", "GTCG", "GTCT", "GTGA", "GTGC", "GTGG", "GTGT", "GTTA", "GTTC", "GTTG", "GTTT",
                    "TGAA", "TGAC", "TGAG", "TGAT", "TGCA", "TGCC", "TGCG", "TGCT", "TGGA", "TGGC", "TGGG", "TGGT", "TGTA", "TGTC", "TGTG", "TGTT", "TTAA", "TTAC", "TTAG", "TTAT", "TTCA", "TTCC", "TTCG", "TTCT", "TTGA", "TTGC", "TTGG", "TTGT", "TTTA", "TTTC", "TTTG", "TTTT"]
    if key > 255:
        return error("Key is too large (> 256)") 
    if key > 0:
        table = deque(defaultTable)
        table.rotate(-key)
        return table
    else:
        return defaultTable

# def DNAtoEncodedBinary(dna, table):
#     i = 0
#     output = ""
#     while i < len(dna):
#         dnasequence = dna[i:i+4]
#         if len(dnasequence) == 4:
#             output += '{0:08b}'.format(table.index(dnasequence))
#         i += 4
#     return output

def encryption(binary, table):
    i = 0
    j = 0
    dnaoutput = ""
    output = ""
    while i < len(binary):
        bitpair = binary[i:i+2]
        if bitpair == "00":
            dnaoutput += "A"
        elif bitpair == "01":
            dnaoutput += "T"
        elif bitpair == "10":
            dnaoutput += "G"
        elif bitpair == "11":
            dnaoutput += "C"
        j += 1
        i += 2
        if j == 4:
            output += '{0:08b}'.format(table.index(dnaoutput))
            j = 0
            dnaoutput = ""
    return output

def DNAencrypt(key, data):
    table = indexTable(key)
    overflow = ""
    if len(data)%8 != 0:
        overflow = data[-(len(data)%8):] 
        data = data[:(len(data)-(len(data)%8))] 
    start = datetime.now()
    encrypted = encryption(data, table)
    # print("done binary to DNA "  + str(datetime.now() - start))
    encrypted = encrypted + overflow
    return encrypted


def EncodedBinarytoDNA(cipher, table):
    i = 0
    output = ""
    while i < len(cipher):
        binarysequence = cipher[i:i+8]
        index = int(binarysequence, 2)
        output += table[index]
        i += 8
    return output

def dnaToBinary(binary):
    i = 0
    output = ""
    while i < len(binary):
        letter = binary[i]
        if letter == "A":
            output += "00"
        elif letter == "T":
            output += "01"
        elif letter == "G":
            output += "10"
        elif letter == "C":
            output += "11"
        i += 1
    return output

def DNAdecrypt(key, cipher):
    
    table = indexTable(key)
    overflow = ""
    if len(cipher)%8 != 0:
        overflow = cipher[-(len(cipher)%8):]
        cipher = cipher[:(len(cipher)-(len(cipher)%8))]
    start = datetime.now()
    dna = EncodedBinarytoDNA(cipher, table)
    # print("done binary to DNA "  + str(datetime.now() - start))
    start2 = datetime.now()
    decrypted = dnaToBinary(dna) + overflow
    # print("done dna to binary " + str(datetime.now() - start2))
    return decrypted