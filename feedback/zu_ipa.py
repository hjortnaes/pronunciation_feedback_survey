import re
import sys
#run using $python3 zu_ipa.py in_file out_file

sent_file = open(sys.argv[1], 'r')
syllables = []
sounds = []
for line in sent_file:
    sentence = line.strip('(\.!?)\s*\n').split(' ')
    for word in sentence:
        word = word.lower()
        syllable = re.sub(r"(a|e|i|o|u)(m(?=[^(a|e|i|o|u|g|y|t|c|x|m)]))?(n(?=[^(a|e|i|o|u|g|y|c|x)]))?",
                           "\g<1>\g<2>\g<3>." , word)
        sound = re.sub(r"(n(gx|gq|gc|g|x|c|y)?|(k|t|p|x|c|q)(h)?|a|e|i|o|u|l(w)?|m|b(h)?|h(l|h)?|dl|sh|mm|[a-z])",
                        "\g<1>.", word)
        syllables.append(syllable)
        sounds.append(sound)
# consonants= {'ngx', 'ngq', 'ngc', 'ny', 'nx', 'nq', 'xh', 'th', 'sh',
#              'hl', 'hh', 'qh', 'ph', 'ng', 'nc', 'z', 'y', 'gx', 'gq', 'gc',
#              'kh', 'dl', 'ch', 'bh', 'x', 'w', 'v',  't',  's', 'r', 'q', 'p',
#              'n', 'm', 'l', 'k', 'j',  'h', 'g', 'f', 'd', 'c', 'b'}