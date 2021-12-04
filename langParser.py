c0de = open('extremesession', 'r', encoding='utf-8').readlines()
code = " ".join(each.replace('\n', '').replace("    ", '') for each in c0de)
import re
from packages import *

steps = {
    'func': {

    }, 
    'vars': { 
        "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, 
        "6": 6, "7": 7, "8": 8, "9": 9, "0": 0,
        "endl": "\n"

    },
    'calls': [ 

    ]
}
if '!Ext(func)' in code:
    codes = code.split('!Ext')
    codes.remove('')
    for each in codes:
        if '(func)' in each:
            Type = re.search(r'(.*?)<', each).group(1).replace('(', '').replace(')', '')
            Name = re.search(r'<(.*?)>', each).group(1)
            function = re.search(r'{(.*?)}!', each).group(1)
            todo = function.split(';')
            if '' in todo: todo.remove('')
            if ' ' in todo: todo.remove(' ')
            
            steps['func'][Name] = {}
            for step in todo:
                if step.isspace():
                    step = None
                else:
                    while step[0] == ' ':
                        step = step[1:len(step)]
                    steps['func'][Name][len(steps['func'][Name])+1] = step
                    
if '!Ext(var)' in code:
    codes = re.findall(r'!Ext\(var\)<(.*?)>(.*?)=(.*?)"(.*?)";', code)
    for each in codes:
        steps['vars'][each[0]] = each[3]

if "*" in code:
    falls = re.findall(r'\*(.*?)\*', code)
    for each in falls:
        steps['calls'].append(each.split('<')[1].split('>')[0])

for each in steps['func']:
    for z in steps['func'][each]:
        step = steps['func'][each][z]
        s = [
            step.split('(')[0], step.split('(')[1].split(')')[0]
        ]
        if "," in s[1]:
            stepS = s[1].split(",")
            for stepS0 in stepS:
                stepS1 = stepS0
                while stepS0[0] == ' ':
                    stepS0 = stepS0[1:len(stepS0)]
                while stepS0[len(stepS0)-1] == ' ':
                    stepS0 = stepS0[0:len(stepS0)-1]
                stepS[stepS.index(stepS1)] = stepS0
            s[1] = stepS
        if type(s[1]) in [list, tuple]:
            for t in s[1]:
                if not (t.startswith('"') and t.endswith('"')):
                    if not t.isnumeric():
                        s[1][s[1].index(t)] = steps['vars'][t]
                    else:
                        s[1][s[1].index(t)] = int(t)
                else:
                    l = []
                    for n in s[1]:
                        if isinstance(n, int): l.append(n)
                        else: l.append(n.replace('"', ''))
                    s[1] = l
        else:
            if not (s[1].startswith('"') and s[1].\
                endswith('"')) and s[1].isnumeric():
                    s[1] = int(s[1])
            else:
                if s[1][len(s[1])] == ' ':
                    while s[1][-1] == ' ':
                        print(s[1][-1])
                        s[1] = s[1][0:len(s[1])-1]
                if s[1].startswith('"') and s[1].\
                    endswith('"') and not s[1].isnumeric():
                        s[1] = s[1].replace('"', '')
                
        if s[1] == '': s[1] = None
        steps['func'][each][z] = s 
for e in steps['calls']:
    for each in steps['func'][e]:
        if isinstance(steps['func'][e][each][1], list) or \
            isinstance(steps['func'][e][each][1], tuple):
                exec(f"{steps['func'][e][each][0]}({str(steps['func'][e][each][1])})")
        elif isinstance(steps['func'][e][each][1], str):
            exec(f"{steps['func'][e][each][0]}(\"{steps['func'][e][each][1]}\")")
