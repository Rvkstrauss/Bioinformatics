import sys
import itertools

dna = 'ACCTGATATAGCTATTATTATCTGGATTACA'
start = 0
end = 8

#def flank_region(length,start_m, end_m):

def find_reps(seq, dna, start_idx):
    s = dna.find(seq,start_idx)
    if s != -1:
        start=s+len(seq)
        while seq == dna[start: start + len(seq)]:
            start = start + len(seq)
        end = start
        return (s, end)
    return (-1,-1)

def find_all_ms(seq, dna, num_reps):
    s = 0
    ms_dict = {}
    while (s > -1):
        s,e = find_reps(seq, dna, s)
        if s>-1 and num_reps<=((e-s)/len(seq)):
            ms_dict[seq] = ms_dict.get(seq,[])
            ms_dict[seq].append((s,e))
        s=e
    return ms_dict
def combinations(seq, dna, num_reps):
    comb = {}
    find_all_ms(seq,dna,num_reps)

def main(dna,seq,reps):
    d = (find_all_ms(seq, dna,reps))
    return d

if __name__=="__main__":
    seq = sys.argv[1]
    reps = int(sys.argv[2])
    if len(sys.argv)>3:
        dna = open(sys.argv[3]).read()
        print ( dna)
    print(main(dna,seq,reps))



