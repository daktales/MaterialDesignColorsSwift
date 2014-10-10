__author__ = 'dak'

import sys
from BeautifulSoup import BeautifulSoup

# Text colors retrieved from css file
text_colors = {
    'color' : '0xFFFFFFDE',
    'color light': '0xFFFFFFDE',
    'color light-strong': '0xFFFFFFFF',
    'color dark': '0x000000DE',
    'color dark-when-small' : '0x000000DE',
    'color dark-strong' : '0x00000000'
    }

# Args check
if len(sys.argv) != 3 :
    print "Syntax: python generator.py <htmlfile> <outputfile>"
    exit(1)

# Go directly to our div
parsed_html = BeautifulSoup(open(sys.argv[1]).read())
div = parsed_html.find('div', attrs={'id':'ui-color-palette-extended-color-palette'})

if not div:
    print "Cannot find color palette section"
    exit(1)

# Every section is a color palette (primary + secondary)
sections = div.findAll('section', attrs={'class':'color-group'})
print "Found %d colors:" % len(sections)

# Intro is index struct
intro = ['struct MaterialColors {\n']
code = []

for section in sections:
    # Get name from first li element
    color = section.find('li', attrs={'class': 'color main-color'})
    colorName = color.find('span').text.replace(' ', '')
    intro.append('\tstatic let %s = _MaterialColor%s.self\n' % (colorName, colorName))

    code.append('struct _MaterialColor%s {\n' % colorName)
    lis = section.findAll('li')[1:]
    for li in lis:
        textColor = text_colors[li['class']]
        spans = li.findAll('span')
        colorHue = spans[0].text
        colorHex = '0x' + spans[1].text[1:].upper() + 'FF'
        constantName = 'P' + colorHue
        if colorHue[0] == 'A':
            constantName = colorHue

        code.append('\tstatic let %s\t: (HUE: UInt, TEXT: UInt)\t= (HUE: %s, TEXT: %s)\n' % (constantName, colorHex, textColor))
    code.append('}\n\n')
    print "\tProcessed %s color" % colorName

intro.append('}\n\n')

# Write results to file
with open(sys.argv[2], 'w') as fout:
    fout.writelines(intro)
    fout.writelines(code)