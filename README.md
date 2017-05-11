# Requeridos 

1. El corpus de entrenamiento y el modelo entrenado (son dos archivos grandes).
2. Python3, skalearn, gensim

# Obtener los índices donde aparecen las GUs dentro del corpus de entrenamiento

Sea el corpus en "GUs_literature.txt" y sea una lista de TFs "AraC", "YdeO", "ArgP", "Ada", "AcrR" y "XylR":

```bash
$ nl ../corpus/GUs_literature.txt | grep AraC | head -n1
     15  AraC . arabinose  AraC-arabinose . fucose AraC-fucose . araBAD  araBAD_mRNA AraB  RXN0-5116 ...
$ nl /almac/ignacio/data/GUsDany/corpus/GUs_literature.txt | grep AcrR | head -n1
     5  AcrR . ethidium AcrR-ethidium . proflavin AcrR-proflavin . rhodamine 6G AcrR-rhodamine 6G ...
$ nl /almac/ignacio/data/GUsDany/corpus/GUs_literature.txt | grep Ada | head -n1
     6  Ada . methyl  Ada-methyl . ada-alkB ada-alkB_mRNA Ada Ada-methyl . ada-alkB ada-alkB_mRNA AlkB... 
$ nl /almac/ignacio/data/GUsDany/corpus/GUs_literature.txt | grep ArgP | head -n1
    16  ArgP . arginine ArgP-arginine . lysine  ArgP-lysine . argO  argO_mRNA ArgO  RXN66-448 arginine_Ext...
$ nl /almac/ignacio/data/GUsDany/corpus/GUs_literature.txt | grep XylR | head -n1
   180  XylR . xylose XylR-xylose . xylAB xylAB_mRNA  XylA  XYLISOM-RXN xylopyranose  xylulose . xylAB ...
$ nl /almac/ignacio/data/GUsDany/corpus/GUs_literature.txt | grep YdeO | head -n1
    57  EvgA . phosphate  EvgA-phosphate . acrD acrD_mRNA AcrD  AcrD-AcrA-TolC  TRANS-RXN-92  drug_Ext ...
```

# Give the indexes to the ranking script and run it:
```bash
$ python most_similars.py -h
usage: most_similars.py [-h] [--indexes indexes] [--corpus corpus]
                        [--inlines inlines] [--model model] [--dims dims]
                        [--top top] [--train train] [--save save]

This script gives a ranking for ach sentence of a given list (list of
'indexes') or for each string inside a file ('inlines').

optional arguments:
  -h, --help         show this help message and exit
  --indexes indexes  A list of indexes separed by comma.
  --corpus corpus    A file containing train text a [sentence|document] per
                     line.
  --inlines inlines  A file containing a sentence by row.
  --model model      A file containing the sentence embeddings model (gensim).
  --dims dims        Dimension of word embeddings.
  --top top          number of sentences returned for each ranking.
  --train train      Toggles whether a new model must be trained
                     (unspecified=False).
  --save save        Toggles whether results must be saved into automaticly
                     named files (unspecified=False).

$ python most_similars.py --corpus $DATA/GUsDany/corpus/GUs_literature.txt --indexes 15,5,6,16,180,57 --model $DATA/GUsDany/d2v_raw_GUs-literature-wiki_H300_W5_A1.model
```

This prints out to stdout the ranking:

index|similaity|GU

````bash
# The most similars to this GU: 
# 'AraC . arabinose AraC-arabinose . fucose AraC-fucose . araBAD  araBAD_mRNA AraB  R'

10  0.99226 AllR . glyoxylate AllR-glyoxylate . allA  allA_mRNA AllA  UREIDOGLYCOLATE-LYASE-RX

5 0.99199 Ada . methyl  Ada-methyl . ada-alkB ada-alkB_mRNA Ada Ada-methyl . ada-alkB ada-a

4 0.99137 AcrR . ethidium AcrR-ethidium . proflavin AcrR-proflavin . rhodamine 6G AcrR-rho

6 0.99095 AdiY . adiA adiA_mRNA AdiA  ARGDECARBOX-RXN arginine  agmatine  CO2 . gadAX gadAX_m

7 0.99053 AgaR . agaR agaR_mRNA AgaR . agaS-kbaY-agaBCDI  agaS-kbaY-agaBCDI_mRNA  AgaS . aga

11  0.98684 AllS . allantoin  AllS-allantoin . allDCE allDCE_mRNA AllD  RXN0-7024 ureidoglycol

13  0.98683 AppY . appCBXA  appCBXA_mRNA  AppC  AppC-AppB RXN0-5266 ubiquinol_Ext oxygen_Ext  ub

12  0.98499 AlsR . allose AlsR-allose . rpiB  rpiB_mRNA RpiB  RXN0-303  aldehydo-D-allose-6-P a

3 0.98437 AccB . accBC  accBC_mRNA  AccB  AccD-AccA-AccC-AccB ACETYL-COA-CARBOXYLTRANSFER-RXN

9 0.97129 AlaS . alanine  AlaS-alanine . alaS alaS_mRNA AlaS  AlaS-alanine . 


# The most similars to this GU: 
# 'AcrR . ethidium  AcrR-ethidium . proflavin AcrR-proflavin . rhodamine 6G AcrR-rho'


6 0.99968 AdiY . adiA adiA_mRNA AdiA  ARGDECARBOX-RXN arginine  agmatine  CO2 . gadAX gadAX_m

5 0.99963 Ada . methyl  Ada-methyl . ada-alkB ada-alkB_mRNA Ada Ada-methyl . ada-alkB ada-a

10  0.99963 AllR . glyoxylate AllR-glyoxylate . allA  allA_mRNA AllA  UREIDOGLYCOLATE-LYASE-RX

7 0.99954 AgaR . agaR agaR_mRNA AgaR . agaS-kbaY-agaBCDI  agaS-kbaY-agaBCDI_mRNA  AgaS . aga

13  0.99844 AppY . appCBXA  appCBXA_mRNA  AppC  AppC-AppB RXN0-5266 ubiquinol_Ext oxygen_Ext  ub

12  0.99793 AlsR . allose AlsR-allose . rpiB  rpiB_mRNA RpiB  RXN0-303  aldehydo-D-allose-6-P a

11  0.99738 AllS . allantoin  AllS-allantoin . allDCE allDCE_mRNA AllD  RXN0-7024 ureidoglycol

3 0.99274 AccB . accBC  accBC_mRNA  AccB  AccD-AccA-AccC-AccB ACETYL-COA-CARBOXYLTRANSFER-RXN

14  0.99137 AraC . arabinose  AraC-arabinose . fucose AraC-fucose . araBAD  araBAD_mRNA AraB  R

9 0.98198 AlaS . alanine  AlaS-alanine . alaS alaS_mRNA AlaS  AlaS-alanine . 


# The most similars to this GU: 
# 'Ada . methyl Ada-methyl . ada-alkB ada-alkB_mRNA Ada Ada-methyl . ada-alkB ada-a'


4 0.99963 AcrR . ethidium AcrR-ethidium . proflavin AcrR-proflavin . rhodamine 6G AcrR-rho

10  0.99959 AllR . glyoxylate AllR-glyoxylate . allA  allA_mRNA AllA  UREIDOGLYCOLATE-LYASE-RX

6 0.99957 AdiY . adiA adiA_mRNA AdiA  ARGDECARBOX-RXN arginine  agmatine  CO2 . gadAX gadAX_m

7 0.99940 AgaR . agaR agaR_mRNA AgaR . agaS-kbaY-agaBCDI  agaS-kbaY-agaBCDI_mRNA  AgaS . aga

13  0.99807 AppY . appCBXA  appCBXA_mRNA  AppC  AppC-AppB RXN0-5266 ubiquinol_Ext oxygen_Ext  ub

12  0.99758 AlsR . allose AlsR-allose . rpiB  rpiB_mRNA RpiB  RXN0-303  aldehydo-D-allose-6-P a

11  0.99706 AllS . allantoin  AllS-allantoin . allDCE allDCE_mRNA AllD  RXN0-7024 ureidoglycol

3 0.99286 AccB . accBC  accBC_mRNA  AccB  AccD-AccA-AccC-AccB ACETYL-COA-CARBOXYLTRANSFER-RXN

14  0.99199 AraC . arabinose  AraC-arabinose . fucose AraC-fucose . araBAD  araBAD_mRNA AraB  R

9 0.98166 AlaS . alanine  AlaS-alanine . alaS alaS_mRNA AlaS  AlaS-alanine . 


# The most similars to this GU: 
# 'ArgP . arginine  ArgP-arginine . lysine  ArgP-lysine . argO  argO_mRNA ArgO  RXN66-4'


11  0.96595 AllS . allantoin  AllS-allantoin . allDCE allDCE_mRNA AllD  RXN0-7024 ureidoglycol

7 0.96445 AgaR . agaR agaR_mRNA AgaR . agaS-kbaY-agaBCDI  agaS-kbaY-agaBCDI_mRNA  AgaS . aga

10  0.96392 AllR . glyoxylate AllR-glyoxylate . allA  allA_mRNA AllA  UREIDOGLYCOLATE-LYASE-RX

6 0.96369 AdiY . adiA adiA_mRNA AdiA  ARGDECARBOX-RXN arginine  agmatine  CO2 . gadAX gadAX_m

12  0.96237 AlsR . allose AlsR-allose . rpiB  rpiB_mRNA RpiB  RXN0-303  aldehydo-D-allose-6-P a

14  0.96222 AraC . arabinose  AraC-arabinose . fucose AraC-fucose . araBAD  araBAD_mRNA AraB  R

5 0.96203 Ada . methyl  Ada-methyl . ada-alkB ada-alkB_mRNA Ada Ada-methyl . ada-alkB ada-a

4 0.96194 AcrR . ethidium AcrR-ethidium . proflavin AcrR-proflavin . rhodamine 6G AcrR-rho

13  0.96039 AppY . appCBXA  appCBXA_mRNA  AppC  AppC-AppB RXN0-5266 ubiquinol_Ext oxygen_Ext  ub

3 0.95761 AccB . accBC  accBC_mRNA  AccB  AccD-AccA-AccC-AccB ACETYL-COA-CARBOXYLTRANSFER-RXN

# The most similars to this GU: 
# 'XylR . xylose  XylR-xylose . xylAB xylAB_mRNA  XylA  XYLISOM-RXN xylopyranose  xylul'


172 0.86116 TrpR . tryptophan TrpR-tryptophan . aroH  aroH_mRNA AroH  DAHPSYN-RXN P-enol-pyruv

169 0.82007 TdcR . tdcABCDEFG tdcABCDEFG_mRNA TdcA . tdcABCDEFG tdcABCDEFG_mRNA TdcB . tdcAB

176 0.81844 UlaR . ulaABCDEF  ulaABCDEF_mRNA  UlaA  UlaC-UlaB-UlaA  RXN0-2461 HPr - phosphorylat

173 0.79348 TyrR . tryptophan TyrR-tryptophan . phenylalanine TyrR-phenylalanine . tyrosine 

174 0.78728 UhpA . phosphate  UhpA-phosphate . uhpT uhpT_mRNA UhpT  TRANS-RXN0-534  GAP_Ext GAP

166 0.77735 SoxS . acnA acnA_mRNA AcnA  ACONITATEHYDR-RXN cis-aconitate I-CIT ACONITATEDEHYDR

180 0.76551 YdeO . appCBXA  appCBXA_mRNA  AppC  AppC-AppB RXN0-5266 ubiquinol_Ext oxygen_Ext  ub

167 0.76202 StpA . bglG bglG_mRNA BglG . bglGFB bglGFB_mRNA BglG . bglGFB bglGFB_mRNA BglF .

161 0.75943 RutR . thymine  RutR-thymine . uracil RutR-uracil . carAB carAB_mRNA  CarA  CarB-Ca

170 0.75093 TorR . phosphate  TorR-phosphate . TorI TorR-TorI . gadAX gadAX_mRNA  GadA  GLUTDEC

# The most similars to this GU: 
# 'EvgA . phosphate EvgA-phosphate . acrD acrD_mRNA AcrD  AcrD-AcrA-TolC  TRANS-RXN-9'


64  0.79245 FucR . fuculose-1-P FucR-fuculose-1-P . fucAO fucAO_mRNA  FucA  FUCPALDOL-RXN fucu

43  0.79137 CytR . cytidine CytR-cytidine . cdd cdd_mRNA  Cdd CYTIDEAM2-RXN cytidine  ammonium

46  0.77583 DeoR . 2-deoxy-D-ribose 5-phosphate DeoR-2-deoxy-D-ribose 5-phosphate . deoCABD 

51  0.77244 DpiA . phosphate  DpiA-phosphate . appY appY_mRNA AppY . citCDEFXG  citCDEFXG_mRNA

49  0.76499 DinJ-YafQ . cspE  cspE_mRNA CspE . dinJ-yafQ  dinJ-yafQ_mRNA  DinJ  YafQ-DinJ . dinJ

40  0.76081 CusR . phosphate  CusR-phosphate . cusCFBA  cusCFBA_mRNA  CusC  CusC-CusB-CusF-CusA 

41  0.75702 CynR . cyanate  CynR-cyanate . cynR cynR_mRNA CynR  CynR-cyanate . cynTS  cynTS_mRN

48  0.75559 DicA . dicB-ydfDE-insD-intQ dicB-ydfDE-insD-intQ_mRNA DicB . dicB-ydfDE-insD-int

47  0.75532 DhaR . DhaK DhaR-DhaK . dhaKLM  dhaKLM_mRNA DhaK  DhaR-DhaK . dhaKLM  dhaKLM_mRNA D

80  0.74344 HcaR . hcaEFCBD hcaEFCBD_mRNA HcaE  HcaC-HcaD-HcaF-HcaE RXN-12072 cinnamate oxyge
```

Happy linking
