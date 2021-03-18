from database import MysqlController
from crawling import CrawlingBetweenRanges
from stopwordFilter import stopwordFilter
from dataset import datasetMaker
import re
from konlpy.tag import Mecab
mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")


patternBlank = r"\([^)]*\)|(\(|\{|\[).*"
patternOR = r"\s*(혹은|혹|또는|아니면|이나|or|OR|Or|oR).*"
stringList = ["식용유또는 올리브유", "얼음 혹 아이스", "강호균아니면이은혁", "다진마늘(마늘", "다진마늘(마늘)", "(마늘)다진마늘", "(마늘)다진마늘(마늘", "{마늘}다진마늘{마늘" ]

def main():

    myDB = MysqlController('127.0.0.1', 'root', '!5dhtmdcks', 'recipe')

    # test1 = re.sub(pattern=patternOR, repl='', string="새송이버섯")
    # test = mecab.nouns("새송이버섯")
    # print(test)
    #
    # for a in stringList:
    #     test3 = re.sub(pattern=patternBlank, repl='', string=a)
    #     print(test3)
    #
    # print(mecab.morphs("다진마늘"))
    # print(mecab.morphs("다진파"))
    # print(mecab.morphs("갈은깨"))
    # print(mecab.morphs("전분가루"))
    # print(mecab.morphs("뷰코닉코코넛오일"))
    # print(mecab.morphs("굵은소금"))
    # print(mecab.morphs("신안섬보배꽃소금"))
    print(mecab.pos("거피들깨가루"))

    # CrawlingBetweenRanges(myDB)
    swFilter = stopwordFilter(myDB)
    swFilter.deDuplicationStopword()
    # swFilter.makeIngredientToText()
    swFilter.eliminateStopwordFromIngredient()
    dsMaker = datasetMaker(myDB, swFilter)

    temp = swFilter.typoChanger("카레가루")
    print(temp)
    temp = swFilter.typoChanger("쌀국수소스")
    print(temp)
    temp = swFilter.typoChanger("쌀국수사리")
    print(temp)
    temp = swFilter.typoChanger("허니머스터드")
    print(temp)
    dsMaker.makeDataset()
    # swFilter.morphemeAnalysis("다진마늘 볶음고추장 로메인 상추 설탕또는슈가 볶음밥 샬롯5g 햄버거스테이크5장")
    # dsMaker.makeNounList()


if __name__ == '__main__':
    main()
