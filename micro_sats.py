import sys
import itertools
from pprint import pprint
import re


def dna_combo(n):
    nt = ['A', 'C', 'G', 'T']
    temp = itertools.product(nt, repeat=n)
    return ["".join(x) for x in temp]
#def flank_region(length,start_m, end_m):


def find_reps(seq, dna, start_idx):
    start = dna.find(seq, start_idx)
    if start != -1:
        end = start + len(seq)
        reps = 1
        while seq[0] == dna[end]:
            end += len(seq)
            reps+=1
        return start, end,reps
    return -1, -1,-1


def find_all_ms(seq, dna, num_reps,lflank=40):
    s = 0
    ms_dict = {}
    while s > -1:
        #print "Finding reps from",s
        s,e,reps = find_reps(seq, dna, s)
        #print s,e,reps
        if s > -1 and num_reps <= reps:
            ms_dict[seq] = ms_dict.get(seq, [])
            sa=s-40 if s>lflank else 0
            ep=e+40 if e<len(dna)-lflank else len(dna)
            cga=cg_content(dna[sa:s])
            cgp=cg_content(dna[e:ep])
            ms_dict[seq].append((s, e,reps,cga,cgp))
        s = e
    return ms_dict

def find_all_ms_re(seq,dna,num_reps,lflank=40):
    pat = re.compile(r'('+seq+'){'+str(num_reps)+',}')
    ms_dict={}
    for m in pat.finditer(dna):
        s,e,gr= (m.start(),m.end(),m.group())
        reps = (s-e)/len(seq)
        ms_dict[seq] = ms_dict.get(seq, [])
        sa=s-40 if s>lflank else 0
        ep=e+40 if e<len(dna)-lflank else len(dna)
        cga=cg_content(dna[sa:s])
        cgp=cg_content(dna[e:ep])
        ms_dict[seq].append((s, e,reps,cga,cgp))
    return ms_dict


def find_combinations(n, dna, num_reps):
    result = {}
    com = dna_combo(n)
    for n_nuc in com:
        print "Looking for ",n_nuc
        result.update(find_all_ms_re(n_nuc, dna, num_reps))
    return result


def cg_content(region_string):
    cg = region_string.count('C') + region_string.count('G')
    #print "CG Content of",region_string,"is",cg,float(cg)/len(region_string)
    return float(cg)/len(region_string)
#where to report this value?


def file_save(l_dict,ofile):
    f = open(ofile, 'w')
    f.write("microsat\tstart\tend\treps\tcg_ant\tcg_post")
    for key,val in l_dict.items():
        for start,end,reps,cga,cgp in val:
            f.write("\n%s\t%d\t%d\t%d\t%f\t%f"%(key,start,end,reps,cga,cgp))
    f.close()


def main(dna, n, reps,ofile):
    d = find_combinations(2, dna, reps)
    #pprint(d)
    file_save(d,ofile)

if __name__== "__main__":
    trash,n,reps,dnafile,ofile = sys.argv
    n=int(n)
    reps = int(reps)
    if len(sys.argv) > 3:
        dna = open(dnafile).read()
        main(dna, n, reps,ofile)


