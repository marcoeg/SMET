"""
    Example of using the SMET module to map text from a CVE to MITRE SDO objects.
"""
import nltk
import funs

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("----------- Downloading model, SDOs and stopwords. Ignore warnings.")
from SMET import map_text,map_attack_vector
from mitreattack.stix20 import MitreAttackData

nltk.download('stopwords')

SDOs_filepath = "./enterprise-attack.json"
mitre_attack_data = MitreAttackData(SDOs_filepath) 
print("----------- Ready\n")

# ID to MITRE entities mapping objects. Example: {"T1055.011": "Process Injection: Extra Window Memory Injection"}
id2mitre = funs.read_json_as_dict('./id2mitre.json')

# Inverted dictionary to map entities to IDs as needed to fetch and print the highest score SDO
mitre2id = {value: key for key, value in id2mitre.items()}

# CVE 2020-0601 - a significant vulnerability in MS Windows Crypto API also named "ChainOfFools" or "CurveBall"
cve_description = "A spoofing vulnerability exists in the way Windows CryptoAPI (Crypt32.dll) validates Elliptic Curve Cryptography (ECC) certificates.An attacker could exploit the vulnerability by using a spoofed code-signing certificate to sign a malicious executable, making it appear the file was from a trusted, legitimate source, aka 'Windows CryptoAPI Spoofing Vulnerability'."

# Use the map_text function of SMET to map CVE to ATT&CK. 
# It returns a list of pairs. The first element of a pair is the SDO entity name and the second the ranking.
mapping = map_text(cve_description, CVE = True)

print(f"CVE description:\n{cve_description}")
print("\nThe top 5 SDOs are:")
for m in mapping[0:5]:
    print(m)

# Use mitre2id[] to map the SDO entity name to its ATT&CK ID needed to fetch the full SDO 
print(f"\nPrinting full STIX object for attack pattern {mitre2id[mapping[0][0]]} - {mapping[0][0]}:")
input("Press enter to continue...")

# get full attack-pattern SDO from the enterprise attack domain
SDO = mitre_attack_data.get_object_by_attack_id(mitre2id[mapping[0][0]], 'attack-pattern')

# print full SDO object
mitre_attack_data.print_stix_object(SDO)
