# syr2ipa
Assyrian text to IPA/latin transliterator

Examples:

Latin:
```
./syr2ipa.py -lt 'ܘܟܠܹܐܠܹܗ ܥܲܠ ܣܹܠܵܐ ܕܝܵܡܵܐ. ܘܚܙܹܠܝܼ ܕܐ݇ܣܸܩܠܹܗ ܕܵܒܵܐ ܡ̣ܢ ܝܵܡܵܐ؛' 
wklehleh ʿal sehla dyama. wkhzehli dsiqleh daba min yama; 
```
IPA:
```
./syr2ipa.py -t 'ܘܟܠܹܐܠܹܗ ܥܲܠ ܣܹܠܵܐ ܕܝܵܡܵܐ. ܘܚܙܹܠܝܼ ܕܐ݇ܣܸܩܠܹܗ ܕܵܒܵܐ ܡ̣ܢ ܝܵܡܵܐ؛' 
wklele ʕal selɑ djɑmɑ. wxzelɪ dsɪqle dɑbɑ mɪn jɑmɑ;
```
With a specified Corpus Dictionary, BDOLs can be detected:
```
./syr2ipa.py -ld corpus.json -t 'ܘܟܠܹܐܠܹܗ ܥܲܠ ܣܹܠܵܐ ܕܝܵܡܵܐ. ܘܚܙܹܠܝܼ ܕܐ݇ܣܸܩܠܹܗ ܕܵܒܵܐ ܡ̣ܢ ܝܵܡܵܐ؛'
wklehleh ʿal sehla d'yama. w'khzehlee d'siqleh daba min yama; 
```

Long term goals include:
- A tunable consolidated .json character definition scheme that any of the implementations can look at for parsing
- Transliteration without vowels using the corpus dictionary
