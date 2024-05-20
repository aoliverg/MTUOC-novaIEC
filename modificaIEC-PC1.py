#    modificaIEC-PC1.py   
#    Copyright (C) 2024  Antoni Oliver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import codecs
import sys
from MTUOC_tokenizer_cat import Tokenizer
import unicodedata
import argparse


parser = argparse.ArgumentParser(description='A script to convert a parallel corpus Catalan-L2 into the new Catalan orthographic rules.')
parser.add_argument("--infile", type=str, help="The input file", required=True)
parser.add_argument("--outfile", type=str, help="The output file.", required=True)

args = parser.parse_args()


fcanvis=codecs.open("canvisDIECnova.txt","r",encoding="utf-8")

tokenizer=Tokenizer()

canvis={}
for linia in fcanvis:
    linia=linia.rstrip()
    if not linia.startswith("#"):
        camps=linia.split("\t")
        canvis[camps[0]]=camps[1]

entrada=codecs.open(args.infile,"r",encoding="utf-8")
sortida=codecs.open(args.outfile,"w",encoding="utf-8")

tokenizer=Tokenizer()

claus=set(canvis.keys())
for linia in entrada:
    linia=linia.rstrip()
    camps=linia.split("\t")
    if len(camps)>=2:
        cat=camps[0]
        L2=camps[1]

        cat=cat.strip()
        cat=cat.replace("’","'") #normalitzacio apòstrof
        cat=cat.replace("l.l","l·l") #normalitzacio l geminada
        cat=cat.replace("L.L","L·L") #normalitzacio l geminada
        cat=unicodedata.normalize('NFC',cat)                    
        cattok=tokenizer.tokenize(cat)
        tokens=set(cattok.split(" "))
        cattok=" "+cattok+" "
        commonclaus=tokens.intersection(claus)
        if len(commonclaus)>0:
            cattok2=cattok
            for cc in commonclaus:
                cattok2=cattok2.replace(" "+cc+" "," "+canvis[cc]+" ")
                cattok2=cattok2.replace(" "+cc.upper()+" "," "+canvis[cc].upper()+" ")
                cattok2=cattok2.replace(" "+cc.capitalize()+" "," "+canvis[cc].capitalize()+" ")
            cat2=tokenizer.detokenize(cattok2).strip()
        else:
            cat2=cat
        cadena=cat2+"\t".join(camps[1:])
        sortida.write(cadena+"\n")
    
