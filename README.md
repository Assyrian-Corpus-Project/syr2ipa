# syr2ipa
Assyrian text to IPA/latin transliterator

Examples:
```
./syr2ipa.py ܘܟܠܹܐܠܹܗ ܥܲܠ ܣܹܠܵܐ ܕܝܵܡܵܐ. ܘܚܙܹܠܝܼ ܕܐَܣܸܩܠܹܗ ܕܵܒܵܐ ܡ̣ܢ ܝܵܡܵܐ؛
IPA: wklele ʕal selɑ djɑmɑ wxzeli dsɪqle dɑbɑ mn jɑmɑ;  
latin: wklehleh ʿal sehla dyama wkhzehlee dsiqleh daba mn yama;  
```

```
/syr2ipa.py ܓܵܘ ܠܸܠܝܼܵܐ ܓܵܘ ܐܝܼܡܵܡܵܐ                            
IPA: gɑw lɪlɪɑ gɑw imɑmɑ  
latin: gaw lilia gaw eemama
```

This repository serves as a hosting site for various implementations of Syriac text to IPA/Latin transliterators in various programming languages.

Long term goals include:
- A tunable consolidated .json character definition scheme that any of the implementations can look at for parsing
- Python version (done)
- C++ version
- Javascript version (done)
- Transliteration without vowels
