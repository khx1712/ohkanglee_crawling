import re
from konlpy.tag import Mecab

patternBlank = r"\([^)]*\)|(\(|\{|\[).*"
patternOR = r"\s*(혹은|혹|또는|아니면|이나|or|OR|Or|oR).*"
patternSymbol = '[^\w\s]'


class stopwordFilter:
    def __init__(self, myDB):
        self.stopword = set()
        self.myDB = myDB
        self.tagger = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")
        # self.typoList = list()
        # self.initTypoChanger()

    # 불용어가 잘 처리되는지 확인하기 위해 DB의 재료를 ingredient.txt 로 받은 뒤
    # 불용어 처리한 재료를 ingredientListElimStopword.txt 에 다시 써서 제대로 가공됬는지 확인한다
    # (이 처리가 잘됨을 확인하면 그때 DB의 자료를 실제로 update 할것)
    def eliminateStopwordFromIngredient(self):
        self.initStopword()
        # self.makeIngredientToText()

        rf = open('textFile/ingredientList.txt', mode='rt', encoding='utf-8')
        wf = open('textFile/ingredientListElimStopword.txt', mode='wt', encoding='utf-8')
        for line in rf:
            writeStr = self.linePreprocess2(line)
            if writeStr != str():
                writeStr = writeStr.lstrip(' ') + '\n'
                wf.write(writeStr)
            if not line:
                break

    def initStopword(self):
        self.deDuplicationStopword()
        f = open('textFile/stopwordList.txt', mode='rt', encoding='utf-8')
        for line in f:
            self.stopword.add(line.rstrip('\n'))
            if not line:
                break
        f.close()

    def linePreprocess(self, line):
        line = re.sub(pattern=patternBlank, repl='', string=line)
        line = re.sub(pattern=patternSymbol, repl='', string=line)

        line = line.rstrip('\n')
        ingredientArr = line.split(' ')
        writeStr = str()
        for ingredient in ingredientArr:
            if ingredient not in self.stopword:
                # writeStr += (' ' + ingredient)
                writeStr += (ingredient)
        return writeStr

    def linePreprocess2(self, line):
        line = re.sub(pattern=patternBlank, repl='', string=line)
        line = re.sub(pattern=patternOR, repl='', string=line)

        nouns = self.tagger.nouns(line)
        writeStr = str()
        for noun in nouns:
            if noun not in self.stopword:
                # writeStr += (' ' + ingredient)
                writeStr += noun
        return writeStr


    def makeIngredientToText(self):
        ingredientList = self.myDB.select_ingredient_iname()
        f = open('textFile/ingredientList.txt', mode='wt', encoding='utf-8')
        for ingredient in ingredientList:
            f.write(ingredient['iname'] + '\n')
        f.close()

    def deDuplicationStopword(self):
        f = open('textFile/stopwordList.txt', mode='rt', encoding='utf-8')
        mySet = set()
        for line in f:
            mySet.add(line.rstrip('\n'))
            if not line:
                break
        f.close()

        f = open('textFile/stopwordList.txt', mode='wt', encoding='utf-8')
        for ingredient in mySet:
            f.write(ingredient+'\n')
        f.close()

    def morphemeAnalysis(self, line):
        return list(self.tagger.morphs(line))
        # print(self.tagger.nouns(line))
        # print(self.tagger.pos(line))

    def initTypoChanger(self):
        self.typoList.append({'typos' : ["머스타드", "머스터드", '허니머스트', '머스타트'],
                              'except' : [],
                              'wrong' : '머스타드'})
        self.typoList.append({'typos' : ["양파"],
                              'except': [],
                              'wrong' : '양파'})
        self.typoList.append({'typos' : ["카레"],
                              'except': [],
                              'wrong' : '카레'})
        self.typoList.append({'typos' : ["쌀국수"],
                              'except': ['소스', '스톡'],
                              'wrong' : '쌀국수'})
        self.typoList.append({'typos' : ["파프리카"],
                              'except': [],
                              'wrong' : '파프리카'})
        self.typoList.append({'typos' : ["베이컨"],
                              'except': [],
                              'wrong' : '베이컨'})
        self.typoList.append({'typos' : ["베이컨"],
                              'except': [],
                              'wrong' : '베이컨'})
        self.typoList.append({'typos' : ["우동면"],
                              'except': [],
                              'wrong' : '우동면'})
        self.typoList.append({'typos': ["오트밀"],
                              'except': [],
                              'wrong': '오트밀'})
        self.typoList.append({'typos': ["케찹", '케첩', '캐찹', '캐첩'],
                              'except': [],
                              'wrong': '케첩'})
        self.typoList.append({'typos': ["소시지", "소세지"],
                              'except': [],
                              'wrong': '소세지'})
        self.typoList.append({'typos': ["경기미"],
                              'except': [],
                              'wrong': '백미'})
        self.typoList.append({'typos': ["액젓"],
                              'except': [],
                              'wrong': '액젓'})
        self.typoList.append({'typos': ["후추", "후춧"],
                              'except': [],
                              'wrong': '후추'})
        self.typoList.append({'typos': ["식초"],
                              'except': [],
                              'wrong': '식초'})
        self.typoList.append({'typos': ["칼국수"],
                              'except': ['스프'],
                              'wrong': '칼국수'})
        self.typoList.append({'typos': ["지단"],
                              'except': [],
                              'wrong': '지단'})
        self.typoList.append({'typos': ["어묵", '오뎅'],
                              'except': ['어묵'],
                              'wrong': '어묵'})
        self.typoList.append({'typos': ['와사비'],
                              'except': ['마요'],
                              'wrong': '와사비'})
        self.typoList.append({'typos': ['후리카케','후리가깨','후리가캐','후리가께','후리가'],
                              'except': [],
                              'wrong': '후리카케'})
        self.typoList.append({'typos': ['파슬리','파아슬리'],
                              'except': [],
                              'wrong': '파슬리'})

    def typoChanger(self, line):
        for typo in self.typoList:
            aFlag = False
            tFlag = False
            for e in typo['except']:
                if line.find(e) != -1:
                    aFlag = True
            for t in typo['typos']:
                if line.find(t) != -1:
                    tFlag = True
            if aFlag is False and tFlag is True:
                return typo['wrong']
        return line