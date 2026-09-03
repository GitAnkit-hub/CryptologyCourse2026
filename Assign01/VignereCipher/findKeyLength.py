ciphertext = '''DVNSJ QRVPC GWBVZ QGVVP VILQJ VTURP BNPZN TGQIG SIGVW MTCIM FQUIA CCKVG CBYKQ
ZNTNB UCIEN UHIVF IWPQC BNKCM IGGGV OEWEV PVGFX APQKM EATDR TBIQG IPRNX JECGQ
NPLMY EDURF IPRXX AVVDZ JKIPN UBQYG PVQGM XYCXV RFIPN VIPRI GMNVT AGVGM NUJZR
KCBUG QCVNS QAILI FPDBN UXVTN TJBQZ JHVIP RMCWJ NTLTG IPNVR WAPTK GGSBU GBIYN
TDRTN ZBQBK BPIIV PTLZC CCFEG QCVHW AFXNS GGMAV HCOLT KGUXV PNJLV PVUNV WMZCI
QPUPA GTDVB ONXUK AWFQE PLOTL VEXVR GCOVP TMEKC ONPSP VUIWE AIPRU RPBNP ZQGRQ
QGSBB UEMAF IPRFP GRZET BTXVT GKMEA RWEPT ZBHIP RNXJE CGGGJ TNVTH BEQDU PQCBN
KCMQD DWXUD VZCIP ROPBV EHBUG HKUQA IETTI QCQWH VCCZD TZFIT WZGIZ VEUQT WGMFC
CLRNT ONPIX EQDNF VWIGJ PLVPH XVTTL TGCME CIQBP HWSVW QAMTZ FQCMZ CCCFE GQCVS
MFEGQ OGSPB YHQZR AMBDH MEXPB VQCAP QJTQN TIQVD LRGEB UGDZR OHEUK AMNPD BUGGM
KRAIV PTLUQ LIOUI ZNEIQ QGPAB HIMAH DCAFE ZNEIQ PCAIC RAQPC IQBPH KRPIC EKTAY
CIMEV WMFEW WYCGZ RCAQF GSBUC IUNVW MZCIQ PULIF PDBZG GMYAP KBNAM PVXWA QUNBT
BCYCH JHVPT NPVCN ITNBT SMFEG QOKCO CCIBR TCANP SZRCH WAKCO NDDCG VWMJQ GTQ'''


filter_ciphertext = "".join(filter(str.isalpha, ciphertext.upper()))
#print(filter_ciphertext)
#print(filter_ciphertext)
# TAsk : FIND the key length
#Algorithm

# Input: Ciphertext C, maximum key length L.
# Output: Estimated key length l.
# 1. For every candidate key length j = 1, 2, . . . , L:
# (a) Split the ciphertext into j slices.
# (b) Compute the IoC of every slice.
# (c) Compute the average IoC.
# 2. Return the smallest key length whose average IoC is closest to English.

ciphertext1 = 'ABCDEFGHIJ'

def split_ciphertext(key_len):
    #return "len" number of slices
    slices = []
    for i in range(key_len):
        slice_i = filter_ciphertext[i::key_len]
        slices.append(slice_i)
    #print(slices)
    return slices


#print(split_ciphertext(3))
from collections import Counter

def IoC_calculate(slice):
    N = len(slice)
    if(N <= 1):
        return 0.0
    
    frequencies = Counter(slice)
    #print("frequencies", frequencies) 

    # numerator
    numerator = sum(count * (count - 1) for count in frequencies.values())
    #print(numerator)

    #denominator
    denominator = N * ( N - 1)
    #print(denominator)

    #print(numerator / denominator)

    return numerator / denominator




def FindKeyLength(filter_ciphertext, max_l = 20):

    avg_iocs = {}
    English_ioc = 0.0667
    for key_len in range(1, max_l + 1):
        #splitting the ciphertext into "j" slices
        slices = split_ciphertext(key_len)
        #print(f"len of the slice is {len(slices)}")

        #compute the ioc of every slide
        ioc_scores = [IoC_calculate(s) for s in slices]

        # 3. AVg. IoC scores 
        avg_ioc = sum(ioc_scores) / len(ioc_scores)
        avg_iocs[key_len] = avg_ioc

        print(f"Key Length {key_len:2d}: Average IoC = {avg_ioc:.4f}")

        # 2. Return the key length closest to English IoC (0.0667)
    estimated_l = min(
            avg_iocs.keys(), 
            key=lambda j: abs(avg_iocs[j] - English_ioc)
        )

    return estimated_l


# best_key_length = FindKeyLength(filter_ciphertext, max_l = 33)
# print(f"\n Estimated Key Length: {best_key_length} ---")  # it comes out to be 8


# Step 02: Plaintext Recovery


# Target English frequency vector (delta)
ENGLISH_FREQ = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}

DELTA_VECTOR = [ENGLISH_FREQ[chr(ord('A') + i)] for i in range(26)]
import math
Delta_Norm = math.sqrt(sum(d ** 2 for d in DELTA_VECTOR))
#print(Delta_Norm) # 0.2559
# print(DELTA_VECTOR)
# print(ord('A')) # 65
# print(chr(ord('A'))) # A


def cosine_similarity(gamma, delta = DELTA_VECTOR, delta_norm = Delta_Norm):
    dot_product = sum(g *d for g, d in zip(gamma, delta))
    gamma_norm = math.sqrt(sum(g ** 2 for g in gamma))
    if gamma_norm == 0 or delta_norm == 0:
        return 0.0
    return dot_product / (gamma_norm * delta_norm)

def Key_Recoverey(ciphertext, key_len = 8):

    recovered_key = []
    #for every slice
    for slice_idx in range(key_len):
        slice_text = ciphertext[slice_idx::key_len]
        slice_len = len(slice_text)

        best_shift = 0
        best_score = -1.0
         #for every shift(0 -26)
        for shift in range(26):
            decrypted_slice = [chr((ord(char) - ord('A') - shift) % 26 + ord('A')) for char in slice_text]
            #print("decrypted_slice", decrypted_slice)
            counts = Counter(decrypted_slice)
            #print("counts", counts)
            gamma_shift = [counts[chr(ord('A') + i)] / slice_len for i in range(26)] # count (A) / len(slice_text)
            #print("slice_len", slice_len)
            #print("gamma_shift", gamma_shift)

            score = cosine_similarity(gamma_shift)
            #print(f"for the {shift}, score is {score} ")
            if score > best_score:
                best_score = score
                best_shift = shift

        # print(f"Best score for {slice_idx} slice is {best_score}")
        # print(f"Best shift for {slice_idx} slice is {best_shift}")
        key_char = chr(ord('A') + best_shift)
        recovered_key.append(key_char)  
    key_str = "".join(recovered_key)

    return key_str

def Plaintext_Recoverey(Key, ciphertext):

    key_len = len(Key)
    plaintext = []
    for i, char in enumerate(ciphertext):
        shift = ord(Key[i % key_len]) - ord('A')
        plaintext.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))

    return "".join(plaintext)

def main():
    key_len = FindKeyLength(filter_ciphertext, max_l = 20)
    Key = Key_Recoverey(filter_ciphertext, key_len = key_len)
    plaintext = Plaintext_Recoverey(Key, filter_ciphertext)
    print(f"Key recovered is {Key}, having length of {key_len} and Plaintext is: \n{plaintext}")
        


if __name__ == '__main__':
    main()


