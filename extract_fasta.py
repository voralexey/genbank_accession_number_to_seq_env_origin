with open('acc_nums.txt', 'r') as data:
    acc_numbs = data.readlines() # list
    print(acc_numbs)

with open('test2_origin.fasta', 'r') as origin_fasta:
    input_fasta = origin_fasta.readlines()

parsed_fasta = open('fasta_parsed.txt', 'w')

ACCNUM_DICT = {}
for number in acc_numbs:
    ACCNUM_DICT[number[:-1]] = 1  # set value to 1 (can be anything)
print(ACCNUM_DICT)

skip = 0
for line in input_fasta:
    if line[0] == '>':  # should I use "^>"?
        _splitline = line.split(' ')  # split by space (CHECK HEADER FORMAT)
        accessionNumWithArrow = _splitline[0] # select >AccessionNumber
        long_acc_num_line = accessionNumWithArrow.split(".")
        long_acc_num = long_acc_num_line[0]
        accessionNum = long_acc_num[1:] # skip ">"
        print(accessionNum)
        if accessionNum in ACCNUM_DICT:
            parsed_fasta.write(line)
            skip = 0
        else:
            skip = 1
    else:
        if not skip:
            parsed_fasta.write(line)

parsed_fasta.close()