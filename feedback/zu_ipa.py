import re
import sys
# run using $python3 zu_ipa.py in_file out_file


def syllablize(sent):
    # consonants= {'ngx', 'ngq', 'ngc', 'ny', 'nx', 'nq', 'xh', 'th', 'sh',
    #              'hl', 'hh', 'qh', 'ph', 'ng', 'nc', 'z', 'y', 'gx', 'gq', 'gc',
    #              'kh', 'dl', 'ch', 'bh', 'x', 'w', 'v',  't',  's', 'r', 'q', 'p',
    #              'n', 'm', 'l', 'k', 'j',  'h', 'g', 'f', 'd', 'c', 'b'}
    sentence = sent.strip('(\.!?)\s*\n').split(' ')
    syllables = []
    sounds = []
    for word in sentence:
        word = word.lower()
        syllable = re.sub(r"(a|e|i|o|u)(m(?=[^(a|e|i|o|u|g|y|t|c|x|m)]))?(n(?=[^(a|e|i|o|u|g|y|c|x)]))?",
                          "\g<1>\g<2>\g<3>.", word)
        sound = re.sub(r"(n(gx|gq|gc|g|x|c|y)?|(k|t|p|x|c|q)(h)?|a|e|i|o|u|l(w)?|m|b(h)?|h(l|h)?|dl|sh|mm|[a-z])",
                       "\g<1>.", word) + ' '
        syllables.append(syllable)
        sounds.extend(sound.split('.'))
    return syllables, sounds[:-1]


# sent_file = open(sys.argv[1], 'r')
#
#
# with open(sys.argv[2], 'w') as out_file:
#     for line in sent_file:
#         syl_line, sound_line = syllablize(line)
#         print(line.strip(), file=out_file)
#         print(syl_line, file=out_file)
#         print(sound_line, file=out_file)
#         print('-'*64, file=out_file)
