import sys

class SyrChar:
    ##
    # name:       str - the name of the of character
    # character:  str - a unicode string represnting the character
    # is_letter:  bool - a flag denoting if this is a base letter
    # is_modifer: bool - a flag denoting if this is a modifier (majleana, rukakha, qushaya, khwasa, rwakha, qanuna)
    # modifier_function: func - a function with a str parameter that each modifier should have
    # is_vowel:   bool - a flag denoting if this is a vowel
    def __init__(self, name, character, 
                is_letter = False, 
                is_matres = False, 
                is_modifer = False, 
                modifier_function = None, 
                is_vowel = False, 
                is_punctuation = False,
                is_talqana = False,
                punctuation_override = '',
                latin = '', ipa = ''):
        self.name = name
        self.character = character
        self.is_letter = is_letter
        self.is_matres = is_matres
        self.is_modifer = is_modifer
        self.modifier_function = modifier_function
        self.is_punctuation = is_punctuation
        self.punctuation_override = punctuation_override
        self.is_vowel = is_vowel
        self.is_talqana = is_talqana
        self.latin = latin
        self.ipa = ipa

        if (self.is_modifer or self.is_matres or self.is_talqana) and self.modifier_function is None:
            print(f'Error: defining a modifier: {n}, but not modifier function was definined - exiting'.format(n=self.name))
            exit(1)

    def Modify(self, letter, previous_token, this_token, next_token):
        ipa   = ''
        latin = ''

        if self.modifier_function is None:
            return '',''
        return self.modifier_function(letter, previous_token, this_token, next_token)

    def GetPunctuation(self):
        ipa = ''
        latin = ''
        if self.is_punctuation:
            if self.punctuation_override != '':
                ipa = self.punctuation_override
                latin = self.punctuation_override
            else:
                ipa = self.character
                latin = self.character
        return ipa, latin

class SyrToken:
    def __init__(self, token):
        self.base = None
        self.modifier = None
        self.punctuation = None
        self.talqana = None
        self.vowel = None

        n_letter  = 0
        n_modifer = 0
        n_vowel   = 0

        for t in token:
            if t.is_letter:
                if n_letter == 0:
                    self.base = t
                n_letter += 1
            elif t.is_punctuation:
                self.punctuation = t
            elif t.is_modifer:
                if n_modifer == 0:
                    self.modifier = t
                n_modifer += 1
            elif t.is_talqana:
                self.talqana = t
            elif t.is_vowel:
                if n_vowel == 0:
                    self.vowel = t
                n_vowel += 1

def SyrCharTokensToIPA(tokens):
    n_tokens = len(tokens)
    if n_tokens == 0:
        return '',''

    ipa = ''
    latin = ''

    previous_token = None
    next_token = None
    for t_itor in range(0, n_tokens):
        t = tokens[t_itor]
        
        if t.base is None:
            if t.punctuation:
                return t.punctuation.GetPunctuation()
        
        next_token = None
        if t_itor + 1 <= n_tokens - 1:
            next_token = tokens[t_itor + 1]

        i = ''
        l = ''
        if t.talqana:
            i, l = t.modifier.Modify(t.base, previous_token, t, next_token)
        else:
            if t.modifier:
                i, l = t.modifier.Modify(t.base, previous_token, t, next_token)
            elif t.base.is_matres:
                i, l = t.base.Modify(t.base, previous_token, t, next_token)
            else:
                i += t.base.ipa
                l += t.base.latin
            ipa += i
            latin += l

            if t.vowel:
                ipa   += t.vowel.ipa
                latin += t.vowel.latin

        if t.punctuation:
            i, l = t.punctuation.GetPunctuation()
            ipa += i
            latin += l

        previous_token = t

    return ipa, latin

def ModifierKhwasa(letter, previous_token, t, next_token):
    ipa   = ''
    latin = ''

    # shorten the khwasa if constrained by two shleekheh atwateh
    shorten = False
    if not previous_token is None and not next_token is None:
        if not previous_token.vowel and not next_token.vowel:
            shorten = True

    if letter.character == 'ܝ':
        if shorten:
            ipa = 'ɪ'
            latin = 'i'
        else:
            ipa = 'i'
            latin = 'ee'

    elif letter.character == 'ܘ':
        ipa = 'u'
        latin = 'u'
    
    return ipa, latin

def ModifierRwakha(letter, previous_token, t, next_token):
    ipa   = ''
    latin = ''

    if letter.character == 'ܘ':
        ipa = 'o'
        latin = 'o'
    
    return ipa, latin

def ModifierMajliana(letter, previous_token, t, next_token):
    ipa   = ''
    latin = ''

    if letter.character == 'ܓ':
        ipa = 'dʒ'
        latin = 'j'
    elif letter.character == 'ܙ':
        ipa = 'ʒ'
        latin = 'zh'
    elif letter.character == 'ܟ':
        ipa = 'tʃ'
        latin = 'ch'
    elif letter.character == 'ܫ':
        ipa = 'ʒ'
        latin = 'zh'
    
    return ipa, latin

def ModifierSiyameh(letter, previous_token, t, next_token):
    ipa   = ''
    latin = ''

    if letter.character == 'ܖ':
        ipa = 'r'
        latin = 'r'
    else:
        ipa = letter.ipa
        latin = letter.latin

def ModifierMatres(letter, previous_token, t, next_token):
    ipa   = ''
    latin = ''

    if letter.character == 'ܐ':
        if t.vowel:
            ipa = ''
            latin = ''
        elif previous_token is None:
            if next_token and next_token.vowel and (next_token.vowel.name == 'KHWASA' or next_token.vowel.name == 'RWAKHA'):
                    ipa = ''
                    latin = ''
            else:
                if letter.name == 'ALAP_WEST':
                    ipa = 'o'
                    latin = 'o'
                else:    
                    ipa = 'ɑ'
                    latin = 'a'
        elif next_token is None or next_token.is_punctuation:
            if previous_token and previous_token.vowel and (previous_token.vowel.name == 'ZQAPPA' or previous_token.vowel.name == 'PTAKHA' or previous_token.vowel.name == 'ZLAMA_KIRYA' or previous_token.vowel.name == 'ZLAMA_YARIKHA'):
                ipa = ''
                latin = ''
        else:
            ipa = letter.ipa
            latin = letter.latin

    elif letter.character == 'ܗ':
        if next_token is None and previous_token.vowel and (previous_token.vowel.name == 'ZQAPPA' or previous_token.vowel.name == 'PTAKHA' or previous_token.vowel.name == 'ZLAMA_KIRYA' or previous_token.vowel.name == 'ZLAMA_YARIKHA'):
            ipa = ''
            latin = ''
        else:
            ipa = letter.ipa
            latin = letter.latin

    return ipa, latin

def ModifierRukakha(letter, previous_token, t, next_token):
    ipa   = ''
    latin = ''

    if letter.character == 'ܒ':
        ipa = 'w'
        latin = 'w'
    elif letter.character == 'ܓ':
        ipa = 'ɣ'
        latin = 'gh'
    elif letter.character == 'ܕ':
        ipa = 'ð'
        latin = 'dh'
    elif letter.character == 'ܟ':
        ipa = 'x'
        latin = 'kh'
    elif letter.character == 'ܦ':
        ipa = 'f'
        latin = 'f'
    elif letter.character == 'ܬ':
        ipa = 'θ'
        latin = 'th'
    
    return ipa, latin

def ModifierRukakhaSemiCircle(letter, previous_token, t, next_token):
    ipa   = ''
    latin = ''

    if letter.character == 'ܦ':
        ipa = 'f'
        latin = 'f'
    
    return ipa, latin

def ModifierTalqana(letter, previous_token, t, next_token):
    return '', ''

alap = SyrChar('ALAP', 'ܐ', is_letter = True, is_matres = True, modifier_function=ModifierMatres, latin = 'a', ipa = 'ʔ')
alap_west = SyrChar('ALAP_WEST', 'ܐ', is_letter = True, latin = 'o', ipa = 'ʔ')
beth = SyrChar('BETH', 'ܒ', is_letter = True, latin = 'b', ipa = 'b')
gammal = SyrChar('GAMMAL', 'ܓ', is_letter = True, latin = 'g', ipa = 'g')
gammal_garshuni = SyrChar('GAMMAL_GARSHUNI', 'ܔ', is_letter = True, latin = 'j', ipa = 'dʒ')
dalath = SyrChar('DALATH', 'ܕ', is_letter = True, latin = 'd', ipa = 'd')
heh = SyrChar('HEH', 'ܗ', is_letter = True, is_matres = True, modifier_function=ModifierMatres, latin = 'h', ipa = 'h')
waw = SyrChar('WAW', 'ܘ', is_letter = True, latin = 'w', ipa = 'w')
zain = SyrChar('ZAIN', 'ܙ', is_letter = True, latin = 'z', ipa = 'z')
kheth = SyrChar('KHETH', 'ܚ', is_letter = True, latin = 'kh', ipa = 'x')
theth = SyrChar('THETH', 'ܛ', is_letter = True, latin = 'ṭ', ipa = 'tˤ')
yodh = SyrChar('YODH', 'ܝ', is_letter = True, latin = 'y', ipa = 'j')
kap = SyrChar('KAP', 'ܟ', is_letter = True, latin = 'k', ipa = 'k')
lammad = SyrChar('LAMMAD', 'ܠ', is_letter = True, latin = 'l', ipa = 'l')
meem = SyrChar('MEEM', 'ܡ', is_letter = True, latin = 'm', ipa = 'm')
nun = SyrChar('NUN', 'ܢ', is_letter = True, latin = 'n', ipa = 'n')
simkat = SyrChar('SIMKAT', 'ܣ', is_letter = True, latin = 's', ipa = 's')
simkat_final = SyrChar('SIMKAT_FINAL', 'ܤ', is_letter = True, latin = 's', ipa = 's')
ain = SyrChar('AIN', 'ܥ', is_letter = True, latin = 'ʿ', ipa = 'ʕ')
peh = SyrChar('PEH', 'ܦ', is_letter = True, latin = 'p', ipa = 'p')
sadeh = SyrChar('PEH', 'ܨ', is_letter = True, latin = 'ṣ', ipa = 'sˤ')
qop = SyrChar('QOP', 'ܩ', is_letter = True, latin = 'q', ipa = 'q')
resh = SyrChar('RESH', 'ܪ', is_letter = True, latin = 'r', ipa = 'r')
dotless_resh = SyrChar('DOTLESS_RESH', 'ܖ', is_letter = True, latin = '', ipa = '')
shin = SyrChar('SHIN', 'ܫ', is_letter = True, latin = 'š', ipa = 'ʃ')
taw = SyrChar('TAW', 'ܬ', is_letter = True, latin = 't', ipa = 't')

zqappa = SyrChar('ZQAPPA', 'ܵ', is_vowel = True, latin = 'a', ipa = 'ɑ')
ptakha = SyrChar('PTAKHA', 'ܲ', is_vowel = True, latin = 'a', ipa = 'a')
zlama_kirya = SyrChar('ZLAMA_KIRYA', 'ܸ', is_vowel = True, latin = 'i', ipa = 'ɪ')
zlama_yarikha = SyrChar('ZLAMA_YARIKHA', 'ܹ', is_vowel = True, latin = 'eh', ipa = 'e')
pthaha_top = SyrChar('PTHAHA_TOP', 'ܰ', is_vowel = True, latin = 'a', ipa = 'a')
pthaha_bottom = SyrChar('PTHAHA_BOTTOM', 'ܱ', is_vowel = True, latin = 'a', ipa = 'a')
zqapha_top = SyrChar('ZQAPHA_TOP', 'ܳ', is_vowel = True, latin = 'o', ipa = 'o')
zqapha_bottom = SyrChar('ZQAPHA_BOTTOM', 'ܴ', is_vowel = True, latin = 'o', ipa = 'o')
rwasa_top = SyrChar('RWASA_TOP', 'ܶ', is_vowel = True, latin = 'e', ipa = 'e')
hwasa_bottom = SyrChar('HWASA_BOTTOM', 'ܷ', is_vowel = True, latin = 'e', ipa = 'e')
hwasa_top = SyrChar('HWASA_TOP', 'ܶ', is_vowel = True, latin = 'i', ipa = 'ɪ')
esasa_bottom = SyrChar('ESASA_BOTTOM', 'ܷ', is_vowel = True, latin = 'u', ipa = 'u')
esasa_top = SyrChar('ESASA_TOP', 'ܶ', is_vowel = True, latin = 'u', ipa = 'u')
khwasa = SyrChar('KHWASA', 'ܼ', is_modifer = True, modifier_function = ModifierKhwasa)
rwakha = SyrChar('RWAKHA', 'ܿ', is_modifer = True, modifier_function = ModifierRwakha)

rukakha = SyrChar('RUKAKHA', '݂', is_modifer = True, modifier_function = ModifierRukakha)
rukakha_semicircle  = SyrChar('RUKAKHA_SEMICIRCLE', '̮', is_modifer = True, modifier_function = ModifierRukakhaSemiCircle)
majliana = SyrChar('MAJLIANA_BOTTOM', '̰', is_modifer = True, modifier_function = ModifierMajliana)
majliana_top = SyrChar('MAJLIANA_TOP', '̃', is_modifer = True, modifier_function = ModifierMajliana)

siyameh = SyrChar('SIYAMEH', '̈', is_modifer = True, modifier_function = ModifierSiyameh)
talqana = SyrChar('TALQANA', '݇', is_talqana = True, modifier_function = ModifierTalqana)
talqana_bottom = SyrChar('TALQANA_BOTTOM', '݈', is_talqana = True, modifier_function = ModifierTalqana)

comma = SyrChar('COMMA', ',', is_punctuation = True)
syrcomma = SyrChar('SYRCOMMA', '،', is_punctuation = True, punctuation_override=',')
semicolon = SyrChar('SEMICOMMA', ';', is_punctuation = True)
syrsemicolon = SyrChar('SYRSEMICOMMA', '؛', is_punctuation = True, punctuation_override=';')
question = SyrChar('QUESTION', '?', is_punctuation = True)
syrquestion = SyrChar('SYRQUESTION', '؟', is_punctuation = True, punctuation_override='?')
space = SyrChar('SPACE', ' ', is_punctuation = True)

EastSyrChars = [alap, beth, gammal, gammal_garshuni, dalath, heh, waw, zain, kheth, theth, yodh, kap, lammad, meem, nun, simkat, simkat_final, ain, peh, sadeh, qop, resh, dotless_resh, shin, taw, zqappa, ptakha, zlama_kirya, zlama_yarikha, pthaha_top, pthaha_bottom, zqapha_top, zqapha_bottom, rwasa_top, hwasa_bottom, hwasa_top, esasa_bottom, esasa_top, khwasa, rwakha, rukakha, rukakha_semicircle, majliana, majliana_top, siyameh, talqana, talqana_bottom, comma, syrcomma, semicolon, syrsemicolon, question, syrquestion, space]
WestSyrChars = [alap_west, beth, gammal, gammal_garshuni, dalath, heh, waw, zain, kheth, theth, yodh, kap, lammad, meem, nun, simkat, simkat_final, ain, peh, sadeh, qop, resh, dotless_resh, shin, taw, zqappa, ptakha, zlama_kirya, zlama_yarikha, pthaha_top, pthaha_bottom, zqapha_top, zqapha_bottom, rwasa_top, hwasa_bottom, hwasa_top, esasa_bottom, esasa_top, khwasa, rwakha, rukakha, rukakha_semicircle, majliana, majliana_top, siyameh, talqana, talqana_bottom, comma, syrcomma, semicolon, syrsemicolon, question, syrquestion, space]
SyrChars = EastSyrChars

def PrintSyrCharArray(syrChars):
    for char in syrChars:
        print(char.name)

def TokenizeLettersWithModifiers(SyrChars):
    tokens = []

    tok = []
    for char in SyrChars:
        if char.is_letter:
            if len(tok) > 0:
                tokens.append(SyrToken(tok))
                tok = []
        tok.append(char)
    
    if len(tok) > 0:
        tokens.append(SyrToken(tok))

    return tokens

def StrToSyrChars(word):
    syrChars = []
    for char in word:
        for syrChar in SyrChars:
            if char == syrChar.character:
                syrChars.append(syrChar)
    return syrChars

def SyrWordStrToIPA(syrWord):
    syrCharArray = StrToSyrChars(syrWord)
    # PrintSyrCharArray(syrCharArray)
    tokens = TokenizeLettersWithModifiers(syrCharArray)
    return SyrCharTokensToIPA(tokens)

def ProcessSyrText(syrStr):
    space_split_text = syrStr.split(' ')
    ipa = ''
    latin = ''
    for word in space_split_text:
        i,l = SyrWordStrToIPA(word)
        ipa += i + ' '
        latin += l + ' '

    return ipa, latin

if __name__ == "__main__":
    text = ''
    for word in sys.argv[1:]:
        text += word + ' '

    print(ProcessSyrText(text)[1])


