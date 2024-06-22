# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 04:03:07 2023

@author: basel
"""

# export CUDA_VISIBLE_DEVICES=""

import nltk
nltk.download('stopwords')


from SMET import map_text,map_attack_vector

#Mapping tips:
#When the input is short (e.g., one sentence or attack action) use map_attack_vector()
#For inputs that consist of a few lines, such as a CVE entry of a paragraph from a CTI report use map_text() 
#In cases where the input is long, like a full CTI report, segmented the text into multiple paragraphs or sentences and processed each separately


#map attack vectors to ATT&CK
AV1 = 'take screenshot'
mapping1 = map_attack_vector(AV1)

AV2 = 'delete logs'
mapping2 = map_attack_vector(AV2)

AV3 = 'exfiltrate data to C2 server'
mapping3 = map_attack_vector(AV3)



#map CVE to ATT&CK
cve = "A remote code execution vulnerability was found in Shim. The Shim boot support trusts attacker-controlled values when parsing an HTTP response. This flaw allows an attacker to craft a specific malicious HTTP request, leading to a completely controlled out-of-bounds write primitive and complete system compromise. This flaw is only exploitable during the early boot phase, an attacker needs to perform a Man-in-the-Middle or compromise the boot server to be able to exploit this vulnerability successfully. "
mapping = map_text(cve,CVE = True)


#map any text to ATT&CK
cve = ""
mapping = map_text(cve,CVE = False)


#get embedding using ATT&CK 
from sentence_transformers import SentenceTransformer

text = ""

emb_model = SentenceTransformer("basel/ATTACK-BERT")
embedding = emb_model.encode(text)


######
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('basel/ATTACK-BERT')

sentences = ["the account has weak password", "attacker gain an initial access to the machine"]

embeddings = model.encode(sentences)

from sklearn.metrics.pairwise import cosine_similarity
print(cosine_similarity([embeddings[0]], [embeddings[1]]))


#### MEG 

import funs
id2mitre = funs.read_json_as_dict('id2mitre.json')

# Inverted dictionary
mitre2id = {value: key for key, value in id2mitre.items()}

#map CVE to ATT&CK
cve = "A remote code execution vulnerability was found in Shim. The Shim boot support trusts attacker-controlled values when parsing an HTTP response. This flaw allows an attacker to craft a specific malicious HTTP request, leading to a completely controlled out-of-bounds write primitive and complete system compromise. This flaw is only exploitable during the early boot phase, an attacker needs to perform a Man-in-the-Middle or compromise the boot server to be able to exploit this vulnerability successfully. "
mapping = map_text(cve,CVE = True)

print(mitre2id[mapping[0][0]])
print(mitre2id[mapping[1][0]])

print(mapping[0][0], mitre2id[mapping[0][0]])
cve = "A spoofing vulnerability exists in the way Windows CryptoAPI (Crypt32.dll) validates Elliptic Curve Cryptography (ECC) certificates.An attacker could exploit the vulnerability by using a spoofed code-signing certificate to sign a malicious executable, making it appear the file was from a trusted, legitimate source, aka 'Windows CryptoAPI Spoofing Vulnerability'."

