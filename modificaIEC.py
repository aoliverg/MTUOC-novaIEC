#    modificaIEC.py   
#    Copyright (C) 2020  Antoni Oliver
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

import codecs
import sys
from MTUOC_tokenizer_cat import tokenize
from MTUOC_tokenizer_cat import detokenize

fcanvis=codecs.open("canvisDIECnova.txt","r",encoding="utf-8")

canvis={}
for linia in fcanvis:
    linia=linia.rstrip()
    if not linia.startswith("#"):
        camps=linia.split("\t")
        canvis[camps[0]]=camps[1]

entrada=codecs.open(sys.argv[1],"r",encoding="utf-8")
sortida=codecs.open(sys.argv[2],"w",encoding="utf-8")

claus=set(canvis.keys())
for linia in entrada:
    cat=linia.rstrip()
    cat=cat.replace("’","'").strip()
    cattok=tokenize(cat)
    tokens=set(cattok.split(" "))
    cattok=" "+cattok+" "
    commonclaus=tokens.intersection(claus)
    print(commonclaus)
    if len(commonclaus)>0:
        cattok2=cattok
        for cc in commonclaus:
            cattok2=cattok2.replace(" "+cc+" "," "+canvis[cc]+" ")
            cattok2=cattok2.replace(" "+cc.upper()+" "," "+canvis[cc].upper()+" ")
            cattok2=cattok2.replace(" "+cc.capitalize()+" "," "+canvis[cc].capitalize()+" ")
        cat2=detokenize(cattok2).strip()
    else:
        cat2=cat
    
    sortida.write(cat2+"\n")
    
