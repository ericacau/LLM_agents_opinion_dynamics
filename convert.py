import codecs

import magic

blob = open('results/old/theseus_different_mistral_1.jsonl', 'rb').read()
m = magic.Magic(mime_encoding=True)
encoding = m.from_buffer(blob)

print(encoding)

BLOCKSIZE = 1048576 # or some other, desired size in bytes
with codecs.open('results/old/theseus_different_mistral_1.jsonl', "r", encoding) as sourceFile:
    with codecs.open('results/theseus_different_mistral_1_new.jsonl', "w", "utf-8") as targetFile:
        while True:
            try:
                contents = sourceFile.read(BLOCKSIZE)
                if not contents:
                    break
                targetFile.write(contents)
            except:
                pass