#/bin/bash

#echo "llama3 same"
#python execution.py llama3 3 theseus_same.json

#echo "mistral same"
#python execution.py mistral 3 theseus_same.json

#echo "llama3 different"
#python execution.py llama3 3 theseus_different.json

#echo "mistral different"
#python execution.py mistral 3 theseus_different.json


python execution.py llama3 3 theseus_same.json
python execution.py mistral 3 theseus_same.json
python execution.py llama3 3 theseus_different.json
python execution.py mistral 3 theseus_different.json