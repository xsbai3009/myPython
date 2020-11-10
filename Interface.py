# coding:utf-8
import re
import shutil
import unittest
from Config.Config import *
from Src.Common import lprint, readTxt
from Src.Csv import loadParams



def writer(line, arg):
    '''
    根据TestModule.py.tmpl创建新的py文件
    :param DataName:运行接口(文件)的名字 eg: login
    :param arg:接口传入参数  eg:username=local.super&password=35665632616b6978554256345a425a634f50745837413d3d
    '''
    name ="Test" + ''.join(i.capitalize() for i in line['Url'].split('/'))
    if not  os.path.exists(Config.CasesPath):
        os.makedirs(Config.CasesPath)
    PyAbsname = os.path.join(Config.CasesPath, '{}.py'.format(name))
    n=1
    while 1:
        if os.path.exists(PyAbsname):
            PyAbsname = os.path.join(Config.CasesPath, '{}{}.py'.format(name,n))
            name = name+'{}'.format(n)
            n +=1
        else:
            break

    lprint('生成测试文件为:{}'.format(PyAbsname))

    with  open(PyAbsname, 'w+', encoding='utf-8') as fw:
        f = readTxt(os.path.join(basedir, 'Src', 'TestModuleNew.py.tmpl'))
        for l in f:
            l = re.sub("class ([^(]+)", "class {}".format(name), l)
            l = re.sub("test_data = .+", "test_data = {}".format(line), l)
            l = re.sub("(arg = \S+)", 'arg = "{}"'.format(arg), l)
            fw.write(l)
        lprint('测试 目标 Data  is:{}'.format(arg))
    return  name,PyAbsname



def ReadCase(DataName, arg):
    '''
    读取文件内容
    :param txt: Suite文件夹下txt文件名，例如‘CaseList.txt’
    :return:文件内容
    '''
    lprint("调用文件：(r'{}')".format(Config.CaseAbsName))
    test_data = loadParams(Config.CaseAbsName)
    for line in test_data:
        if line['Url'] == DataName:
            lprint('测试 Url  is:{}'.format(line['Url']))
            lprint('测试 Data  is:{}'.format(line['Data']))
            lprint('测试 Method  is:{}'.format(line['Method']))
            lprint('测试 Response  is:{}'.format(line['Response']))
            lprint('测试 Description  is:{}'.format(line['Description']))
            name ,PyAbsname= writer(line, arg)
            return  name,PyAbsname


def Run(DataName, arg):
    name ,PyAbsname= ReadCase(DataName, arg)
    runner = unittest.TextTestRunner()
    case_path = os.path.join(basedir, "Cases")
    discover = unittest.defaultTestLoader.discover(case_path, pattern=name+'.py', top_level_dir=case_path)
    lprint("************************TEST START************************")
    test_result = runner.run(discover)
    lprint("*************************TEST END*************************")
    time.sleep(3)

    # print('All case ntumber:{}'.format(test_result.testsRun))

    # print('errors case number:{}'.format(len(test_result.errors)))
    if len(test_result.errors):
        for case, reason in test_result.errors:
            # print(reason)
            if reason:
                return 'fail',reason

    # print('Failed case number:{}'.format(len(test_result.failures)))
    elif len(test_result.failures):
        for case, reason in test_result.failures:
            # print(reason)
            if reason:
                return 'fail',reason
    else:
        return "pass", "pass"



# def Run(DataName, arg):
#     name ,PyAbsname= ReadCase(DataName, arg)
#     runner = unittest.TextTestRunner()
#     case_path = os.path.join(basedir, "Cases")
#     discover = unittest.defaultTestLoader.discover(case_path, pattern=name+'.py', top_level_dir=case_path)
#     lprint("************************TEST START************************")
#     returnFlag = runner.run(discover)
#     lprint("*************************TEST END*************************")
#     time.sleep(3)
#     return returnFlag

def deleteTmpFile():
    shutil.rmtree(Config.CasesPath)
    lprint("临时文件已清理完成！")

if __name__ == "__main__":
    pass