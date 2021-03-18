from stopwordFilter import stopwordFilter
from konlpy.tag import Mecab

tagger = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")

class datasetMaker:
    def __init__(self, myDB, stopwordFilter):
        self.myDB = myDB
        self.stopwordFilter = stopwordFilter

    # ['메뉴' '재료' '재료' '재료' '재료' '재료' '재료' '재료' ...] 식으로 dataset을 만듬
    def makeDataset(self):
        wf = open('textFile/recipeList.txt', mode='wt', encoding='utf-8')
        wf2 = open('textFile/dataset.txt', mode='wt', encoding='utf-8')
        menuidList = self.myDB.select_menu_id_url()
        for menuid in menuidList :
            line = list()
            line.append(str(menuid['url']))
            ingredientList = self.myDB.select_ingredient_menuid(menuid['id'])
            for ingredient in ingredientList:
                ingredient = self.stopwordFilter.linePreprocess2(ingredient['iname'])
                ingredient = self.stopwordFilter.typoChanger(ingredient)
                if ingredient != '' and ingredient not in line:
                    line.append(ingredient)
            if len(line) > 2:
                data = " ".join(line)
                wf.write(data + '\n')
                data = " ".join(line[1:])
                wf2.write(data + '\n')
        wf.close()

    def makeWordList(self):
        rf = open('textFile/ingredientList.txt', mode='rt', encoding='utf-8')
        wf = open('textFile/wordList.txt', mode='wt', encoding='utf-8')
        dic = {}
        dic2 = {}
        for line in rf:
            ary = line.split(" ")
            for ing in ary:
                if ing in dic:
                    dic[ing] = dic[ing] + 1
                else:
                    dic.update({ing: 0})
            if not line:
                break

        # rf2 = open('textFile/ingredientList.txt', mode='rt', encoding='utf-8')
        # wf2 = open('textFile/morphemeList.txt', mode='wt', encoding='utf-8')
        # for line in rf2:
        #     line = line.rstrip('\n')
        #     ary = tagger.morphs(line)
        #     for ing in ary:
        #         if ing in dic2:
        #             dic2[ing] = dic2[ing] + 1
        #         else:
        #             dic2.update({ing: 0})
        #     if not line:
        #         break

        res = sorted(dic.items(), key=(lambda x: x[1]), reverse=True)
        for ing in res:
            wf.write(str(ing) + '\n')

        # res = sorted(dic2.items(), key=(lambda x: x[1]), reverse=True)
        # for ing in res:
        #     wf2.write(str(ing) + '\n')

    def makeNounList(self):
        dic2 = {}
        rf2 = open('textFile/ingredientList.txt', mode='rt', encoding='utf-8')
        wf2 = open('textFile/nounList.txt', mode='wt', encoding='utf-8')
        for line in rf2:
            line = line.rstrip('\n')
            ary = tagger.nouns(line)
            for ing in ary:
                if ing in dic2:
                    dic2[ing] = dic2[ing] + 1
                else:
                    dic2.update({ing: 0})
            if not line:
                break

        res = sorted(dic2.items(), key=(lambda x: x[1]), reverse=True)
        for ing in res:
            wf2.write(str(ing) + '\n')

    def makeNonNounList(self):
        dic2 = {}
        rf2 = open('textFile/ingredientList.txt', mode='rt', encoding='utf-8')
        wf2 = open('textFile/nonNounList.txt', mode='wt', encoding='utf-8')
        for line in rf2:
            line = line.rstrip('\n')
            aryMorpheme = tagger.morphs(line)
            aryNouns = tagger.nouns(line)
            for noun in aryNouns:
                aryMorpheme.remove(noun)
            for ing in aryMorpheme:
                if ing in dic2:
                    dic2[ing] = dic2[ing] + 1
                else:
                    dic2.update({ing: 0})
            if not line:
                break

        res = sorted(dic2.items(), key=(lambda x: x[1]), reverse=True)
        for ing in res:
            wf2.write(str(ing) + '\n')






