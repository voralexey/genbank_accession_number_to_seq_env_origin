#################
# Pierre GARCIA #
# AV            #
# Feb 2022      #
#################

# ! usr/bin/python3.8
# -*- coding: utf-8 -*-
import urllib.request
import sys
import time

# from tqdm import tqdm # progress bar

# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=nucleotide&id=AB905779.1&version=2.0

# try:
#     sys.argv[1]
# except:
#     sys.exit("fasta file")


# def readfile(filex):
#     f = open(filex, "r")
#     cont = f.readlines()
#     f.close()
#     return cont


def mafftread(fasta):
    f = open(fasta, "r")
    l = f.readline()
    count = int(0)
    temp = ""
    while l:
        count += 1
        if l.find(">") != -1:  # if true?
            if count == 1:
                temp += l
            else:
                temp += "\n" + l
            l = f.readline()
            continue
        else:
            l = l.rstrip()
            temp += l
            l = f.readline()
    tabtemp = temp.split("\n")
    dicofasta = {}
    liste = []
    nom = ""
    seq = ""
    for l in tabtemp:
        if l.find(">") != -1:
            nom = l
        else:
            seq = l
            dicofasta[nom] = seq
            liste.append(nom)
    return dicofasta, liste


#fasta = mafftread(sys.argv[1])
fasta = mafftread("genbank_script_test.fasta") # WHAT DATA TYPE IS THIS?
#print(fasta)
liste2 = {}

# for i in tqdm(fasta[1]): # shows a % progress bar
for i in fasta[1]:
    accession = i.replace(">", "").split(".")[0]
    url2 = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=nucleotide&id={accession}&version=2.0"

    hdr = {'User-agent': 'your bot 0.1'}
    try:
        req = urllib.request.Request(url2, headers=hdr)
        time.sleep(0.2)
        response = urllib.request.urlopen(req)

        # req = urllib.request.urlopen(url2)
        # req.add_header('User-Agent', 'abc-bot')
        tab_tax = response.readlines() # list
        print(tab_tax)
        # requests.get(link, headers = {'User-agent': 'your bot 0.1'})
        spec = ""
        # strain = ""
        org_name = ""
        source = ""
        for j in tab_tax: # j=strings, one of them is a string with the WHOLE org's description
            j = str(j)
            if j.find("<Organism>") != -1:
                # <SubType>strain|serovar|sub_species|country|isolation_source|collection_date|collected_by</SubType>
                description = j.split("<") # a list with the WHOLE org's description with no "<"
                print(description)
                for k in description: # each element is a string
                    if k.find("Organism>") != -1 and k.find("/Organism>") == -1:
                        # <Organism>Salmonella enterica subsp. enterica serovar Paratyphi B</Organism>
                        org_name = k.split(">")[1]
                        #print(org_name)
                    if k.find("SubType>") != -1 and k.find("/SubType>") == -1:
                        isolation_source_index = k.split(">")[1].split("|").index("isolation_source")
                        #print(isolation_source_index)
                    if k.find("SubName>") != -1 and k.find("/SubName>") == -1:
                        source = k.split("|")[isolation_source_index]
                        #print(source)

                # isolation_source_index = description.split("|").index("isolation_source")
                # print(isolation_source_index)
            # if j.find("<SubName>") != -1:
            #     isolation_source = j.split("|")[isolation_source_index]
            #     print(isolation_source)
            #     for k in isolation_source:
            #         if k.find("<Organism>") != -1 and k.find("</Organism>") != -1:
            #             # <Organism>Salmonella enterica subsp. enterica serovar Paratyphi B</Organism>
            #             spec = k.split("<")[0].split(">")[1]
            #             # print(spec)
            #         if k.find("<SubName>") != -1 and k.find("</SubName>") != -1:
            #             source = isolation_source

            # if j.find("<SubName>") != -1:
            #     spec_str_ori = j.split("<")
            #     print(spec_str_ori) #[1].split("<")[0]
            #     for k in spec_str_ori:
            #         if k.find("Organism>") != -1 and k.find("/Organism>") == -1: # line with an Organism's name
            #       #<Organism>Salmonella enterica subsp. enterica serovar Paratyphi B</Organism>
            #             spec = k.split(">")[1]
            #             print(spec)
            #         if k.find("SubName>") != -1 and k.find("/SubName>") == -1: # line with the WHOLE description line
            #             strain = k.split(">")[1]
            #             #print(strain)
            # print strain
            # print spec
            # print spec
        # print spec
        # break
        # print strain,spec
        # liste2[i] = spec+" "+strain
        liste2[i] = "@"+org_name+"@"+source # a dict
        for k, v in liste2.items():
            liste2[k] = v.rstrip("@") # remove trailing @ if source isn't found

        #print(liste2)
    except:
        print("ERROR, trying again")
        time.sleep(0.2)
# print liste2
#out1 = open(sys.argv[1].replace(".fasta", "_origin.fasta"), "w")
out1 = open("genbank_script_test.fasta".replace(".fasta", "_origin.fasta"), "w")

for i in fasta[1]:
    try:
        out1.write(i.split(".")[0] + " " + liste2[i] + "\n" + fasta[0][i] + "\n")
    except:
        out1.write(i + "\n" + fasta[0][i] + "\n")
out1.close()

#out2 = open(sys.argv[1].replace(".fasta", "_origin.txt"), "w")
out2 = open("genbank_script_test.fasta".replace(".fasta", "_origin.txt"), "w")
for i in fasta[1]:
    try:
        out2.write(i + "\t" + liste2[i] + "\n")
    except:
        out2.write(i + "\tNA\n")
