# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 20:50:47 2019

@author: zengh
"""

from aip import AipOcr


class Change2Text:
    def __init__(self, filePath):
         self.path = filePath   
    """ 读取图片 """
    def readPicture(self):
        with open(self.path, 'rb') as fp:
            return fp.read()
    """ 返回文本识别结果 """
    def getText(self, jsonFile):
       
        textResult = " "
        print('\n' + 20*'-' + "欢迎使用Screen2Text" + 20*'-' )
        lineCount = jsonFile['words_result_num']
        if(lineCount > 0):
            for i in range(0,lineCount):
                line = jsonFile['words_result'][i]['words']
                textResult += line 
                print(line)
        else:
            print('+'* 5 + '  请重试！  ' + '+'*5)
        print('\n' + 20*'-' + "如有任何建议，请及时反馈" + 20*'-' )
        return textResult
    def doOCR(self):
        """  百度SDK, 开放API. APPID AK SK """
        APP_ID = '15619671'
        API_KEY = 'TE2skjfG9ZP3nWN13gIhwW0r'
        SECRET_KEY = 'dmEyu6VKasE0zMSkRlsxy5n8I52cX500'
        
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        image = self.readPicture()
        """ 调用通用文字识别, 图片参数为本地图片 """
        client.basicGeneral(image);
        """ 如果有可选参数 """
        options = {}
        """
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        options["probability"] = "true"
        """
        
        """ 带参数调用通用文字识别, 图片参数为本地图片 """
        jsonFile = client.basicGeneral(image, options)
        text = self.getText(jsonFile)
        return text


