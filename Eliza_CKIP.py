import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#? turn off ttensorflow information( which is so annoying)

from ckiptagger import WS, POS, NER
#? import mandarin word segmentation

def eliza(str):

    text = str
    ws = WS("./data")
    pos = POS("./data")
    ner = NER("./data")
    #? get word data

    ws_results = ws([text])
    pos_results = pos(ws_results)
    ner_results = ner(ws_results, pos_results)

    result_2darr = [ [ws_results[0][index],pos_results[0][index]] for index in range(len(ws_results[0])) ]
    #print(ws_results)
    #print(pos_results)
    #print(result_2darr)

    Noun = set(('Na','Nb','Nd','Nh'))
    Location = set(('Nc','Ncd'))
    Condition = set(('VH','VI','VJ','VK','VL','D'))
    Verb = set(('VA','VAC','VB','VC','VCL','VD','VE','VF','VG','P'))

    Ndict, Locdict, Cdict, Vdict, Cbb_dict = [], [], [], [], []

    for index in range(len(ws_results[0])):
        word, tag = result_2darr[index][0], result_2darr[index][1]
        if tag in Noun:
            Ndict.append(word)
            #? if noun
        elif tag in Location:
            Locdict.append(word)
            #? if location noun
        elif tag in Condition:
            Cdict.append(word)
            #? if Conditional Verb
        elif tag in Verb:
            Vdict.append(word)
            #? if Verb
        print(result_2darr[index])
    #for name in ner_results[0]:
    #    print(name)

    print('N: {}, Loc: {}, C: {}, V:{}'.format(Ndict, Locdict, Cdict, Vdict))
    NounCount, CCount, VerbCount = len(Ndict), len(Cdict), len(Vdict)
    if NounCount>0:
        #? if string contains at least one noun
        if len(Cdict)>0:
            print('{}{}是為甚麼呢?'.format('你' if Ndict[0]=='我' else ( '我' if Ndict[0]=='你' else Ndict[0]),''.join(Cdict)))
        elif len(Locdict)>0:
            print('你提到{}這個地方，{}{}{}讓你感覺如何呢?'.format(Locdict[0],'我' if Ndict[0]=='你' else ( '你' if Ndict[0]=='我' else Ndict[0]),Vdict[0],Locdict[0]))
        elif len(Vdict)>0:
            print('{}為甚麼要{}呢?'.format('你' if Ndict[0]=='我' else ( '我' if Ndict[0]=='你' else Ndict[0]),Vdict[0]))
        else:
            print('{}怎麼了?'.format('你' if Ndict[0]=='我' else ( '我' if Ndict[0]=='你' else Ndict[0])))
    elif CCount >0:
        #? if string contains no noun while there is at least one condidtional verb exist
        if '不好' in ''.join(Cdict):
            print('為你感到抱歉，但是為甚麼{}{}呢?'.format(''.join(Cdict),''.join(Vdict)))
        else:
            print('原來如此，那為甚麼{}呢?'.format(''.join(Cdict)))
    elif VerbCount >0:
        #? if string contains no noun and conditional verb, while there is at least one verb exist
        print('為甚麼{}呢?'.format(''.join(Vdict)))
    else:
        if '謝謝' in Cdict:
            print('不客氣!')
        print('我聽不懂你在說甚麼，換個說法試試?')

def command_interface():
  print('你好，我是人工痣鐬。我會瘋狂問你為甚麼直到你退出程式\n---------')
  print('當要結束程式時，輸入 "quit" 。')
  print('='*72)
  print('你好呀。說說你的心情?')

  s = ''
  while s != 'quit':
    try:
      s = input('> ')
    except EOFError:
      s = 'quit'
    eliza(s)

if __name__ == "__main__":
  command_interface()