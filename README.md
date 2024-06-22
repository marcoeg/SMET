# SMET: mapping CTI reports and CVEs to ATT&CK SDOs

`SMET` is a tool that maps text, such as a CTI report or a CVE, to ATT&CK techniques as MITRE SDOs (STIX Domain Objects).<br>

## Background
The Common Vulnerabilities and Exposures (CVE) and ATT&CK Matrix are two significant MITRE endeavors. CVE facilitates sharing publicly discovered vulnerabilities while ATT&CK collects and categorizes adversaries' Tactic, Techniques, and Procedures (TTP) and recommends appropriate countermeasures. As CVE yields a low-level description of the vulnerability, ATT&CK can complement CVE by providing more insights into it from an attacking perspective for a deeper analysis. 

This project defines a methodology for using MITRE ATT&CK to characterize the impact of a vulnerability as described in the CVE. ATT&CK techniques provide a standard way of describing the methods adversaries use to exploit a vulnerability and what adversaries may achieve by exploiting the vulnerability. Using ATT&CK techniques to describe a vulnerability makes it easier for defenders to integrate vulnerabilities into their threat modeling.

`SMET` is a tool that automatically maps CVE entries to ATT&CK techniques based on their textual similarity. SMET achieves this mapping by leveraging `ATT&CK BERT`, a model to learn semantic similarity among attack actions. 

In inference, `SMET` utilizes semantic extraction, `ATT&CK BERT`, and a logistic regression model to map CVE entries to ATT&CK techniques. 

>Note: the mapping is to the MITRE SDOs in the Enterprise domain.

## Installation 
Requires Python 3.8.18 or later. <br>
```bash
# The mysqlclient pip install fails otherwise becouse of dependencies
sudo apt install libmysqlclient-dev 

# Install dependencies
pip install -r requirements.txt 

# Disable CUDA because incompatibility with drivers and dependencies
export CUDA_VISIBLE_DEVICES=""  

# Downloads the large English model for spaCy NLP library
python -m spacy download en_core_web_lg
```

## Install MITRE SDOs (STIX Domain Objects)
Install the utility library for SDOs `mitreattack-python`:
```
pip install mitreattack-python
```
Also, the STIX enterprise domain SDOs file must on the local machine to output readable results, and not just the SDO's ID.

The https://github.com/mitre/cti repo contains the `cti/enterprise-attack/enterprise-attack.json` file.

If the repo is not cloned on the local machine, download the file:
```
wget https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json
```

## Use Example
The `mapping-example.py` script is an example of using the `SMET.py` module for mapping CVE text to MITRE SDOs.
```
# disable cuda for likely incompatibily of drivers and dependencies
export CUDA_VISIBLE_DEVICES="" 

./mapping-example.py
```

The example is finding the MITRE SDO most likely to map a CVE description in the `cve_description` variable. The SDOs obtained from the models are ranked and the first one is then fetched and printed using the `mitreattack-python` library.

>Documentation about the `mitreattack-python` library: https://mitreattack-python.readthedocs.io/en/latest/

## Model
`SMET` uses the `ATT&CK BERT` model for semantically meaningful cybersecurity text embedding.

`ATT&CK BERT` is a cybersecurity domain-specific language model based on sentence-transformers. `ATT&CK BERT` maps sentences representing attack actions to a semantically meaningful embedding vector. Embedding vectors of sentences with similar meanings have a high cosine similarity.

 https://huggingface.co/basel/ATTACK-BERT
 
>Since it uses `BERT` it is assumed the license is `apache-2.0`.

 Using this model requires the `sentence-transformers` (in `requirements.txt`):
```
pip install -U sentence-transformers
```
Sample usage to estimate similarity between two sentences:
```
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('basel/ATTACK-BERT')

sentences = ["Attacker takes a screenshot", "Attacker captures the screen"]
embeddings = model.encode(sentences)

print(cosine_similarity([embeddings[0]], [embeddings[1]]))
```

Details on the sentence transformer are in https://www.sbert.net/ and https://huggingface.co/tasks/sentence-similarity

## Paper
Basel, A. , Al-Sheer, E. , Singhal, A. , Khan, L. and Hamlen, K. (2023), SMET: Semantic Mapping of CVE to ATT&CK and its Application to Cyber Security, DBSec 2023: Data and Applications Security and Privacy XXXVII, Sophia Antopolis, FR, https://doi.org/10.1007/978-3-031-37586-6_15, https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=936761.


## Similar Map
A similar mapping is in the `mappings-explorer/src/mapex_convert/mappings/Att&ckToCveMappings.csv` file of the repo in https://github.com/center-for-threat-informed-defense/mappings-explorer.git

Check also: https://center-for-threat-informed-defense.github.io/mappings-explorer/about/methodology/cve-methodology/
 