#!/usr/bin/python3
import sys
import re
import functools as ft

def find_courses(inputfilename):

    evil_characters = [
        "?",
        "++",
        "Ã¼",
        "Ãœ",
        "Ã¤",
        "-Ã–",
        "Â¦",
        "+Â£",
        "+Ã±",
        "+Ã",
        "+Â¦",
        "+Ã‚",
        "+Ã»",
        "â€“", 
        "Ã¶",
        "Ã¡",
        "Ãª",
        "Ã–",
        "Ã©",
        "+Â®",
        "Ã”Ã‡Ã´",
        "+Âº",
        "Ã±",
        "Ã§"

    ]
    def compose(f,g):
        return lambda x: g(f(x))
    def subword(s):
        return lambda x: re.sub(re.sub("[ÄÖÜäöüáéíÁÉßñ]","\?",s),s,x)
    words = [
        "Gebäudelehre",
        "Gramática",
        "Dünnschichten",
        "Festkörper",
        "Föderation",
        "Förster",
        "außerplanmäßiger",
        "Türkisch",
        "español",
        "Español",
        "Fakultät",
        "für",
        "Französisch",
        "Übung",
        "Einführung",
        "Logopädie",
        "Geländeseminar",
        "Grenzräumen",
        "Möbelbau",
        "Lüdenscheid",
        "Ausgewählte",
        "Interdisziplinäre",
        "Multimodalität",
        "Relativität",
        "Öffentlichkeit",
        "Berufspädagogik",
        "Ökonomische",
        "Präsentieren",
        "Europäische",
        "Geländepraktikum",
        "über",
        "Sprachentwicklungsstörungen",
        "Prüfung",
        "Diversität",
        "Ältere",
        "Wärmelehre",
        "Öffentlicher",
        "Höhrere",
        "Pläne",
        "Klärschlammbehandlung",
        "Präparierkurs",
        "Grundzüge",
        "überbrückungskurs",
        "Rechnergestütztes",
        "Prüfsysteme",
        "Äquivalent",
        "Gebäudetechnologie",
        "Ökologie",
        "Seminarvorträge",
        "gestützt",
        "strömung",
        "Hörsaal",
        "rgänzend",
        "ropädeutikum",
        "vaskulär",
        "nsätz",
        "örper",
        "nästhesi",
        "spät",
        "dentität",
        "rüfung",
        "öhere",
        "nthropozän",
        "brückung",
        "trömungsmechanik",
        "Ökochemie",
        "rlösung",
        "außer",
        "tänd",
        "versität",
        "länd",
        "öko",
        "häf",
        "giös",
        "äum",
        "ösung",
        "traße",
        "klär"
        "ädag",
        "ührung",
        "öfe",
        "ärme",
        "tät",
        "kräft",
        "spräch",
        "äure",
        "läche",
        "zösisch",
        "töru",
        "räven",
        "Ähnlich",
        "äont",
        "nfän",
        "ündlich",
        "plän",
        "üler",
        "Stühle",
        "rücken",
        "lügel",
        "äpst",
        "ellulär",
        "ömung",
        "läge",
        "tägig",
        "öchstfre",
        "räsentat"
        "ülich",
        "aläo",
        "ründung",
        "ütewirtschaft",
        "eodät",
        "ärm",
        "ropädeutik",
        "bärdensprache",





    ]
    replaceqm= ft.reduce(compose, [
        lambda s: re.sub(r"\(\?\)","(Ü)",s),
        lambda s: re.sub(r"\(L\?\)","(LÜ)",s),
        lambda s: re.sub(r"\(V\?\)","(VÜ)",s),
        lambda s: re.sub(r"\(\?P\)","(ÜP)",s),
    ] + [subword(w) for w in words])
            
    transformations = ft.reduce(compose,[
            lambda s: re.sub(r"Ã¼","ü",s),
            lambda s: re.sub(r"Ã¤","ä",s),
            lambda s: re.sub(r"\+Ã±","ä",s),
            lambda s: re.sub(r"\+\+","ü",s),
            lambda s: re.sub(r"\+Â£", "Ü",s),
            lambda s: re.sub(r"Ãœ","Ü",s),
            lambda s: re.sub(r"Ã¶","ö",s),
            lambda s: re.sub(r"Ã©","é",s),
            lambda s: re.sub(r"Ã§","ç",s),
            lambda s: re.sub(r"Ã–","Ö",s),
            lambda s: re.sub(r"Ãª","é",s),
            lambda s: re.sub(r"â€“","--",s),
            lambda s: re.sub(r"Ã¡","á",s),
            lambda s: re.sub(r"Ã­ ","í",s),
            lambda s: re.sub(r"\+Ã‚","Ö",s),
            lambda s: re.sub(r"\+Ã»","Ö",s),
            lambda s: re.sub(r"Ã±o","ñ",s),
            replaceqm,
    ])
    def evil_characters_in(s):
        return any([x in s for x in evil_characters]) and not '?,' in s and not s.endswith('?') and not '? ' in s

    courses = list()
    firstline = True
    for line in open(inputfilename,'r'):
        if(firstline):
            firstline = False
            continue
        arr = transformations(line).split(',')
        courses.append({'faculty':arr[0],'institute':arr[1],'semester':arr[2],'lv_number':arr[3],'name':arr[4],'type':arr[5] })

    return courses

