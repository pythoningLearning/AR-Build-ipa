# -*- coding: utf-8 -*-

__author__ = 'Arms'

'''
上传ipa文件到SVN
'''

import commands
import os
import urllib
from config import qdSvnConfigs
from common import ShellError, Dict, toDict, showMessage

svnConfigs = toDict(qdSvnConfigs)

def uploadipa(mode='test', ipapath=None):
    if not ipapath:
        raise StandardError('error! ipapath is empty')
    moveCommand = None
    svn_path = None
    svn_local_Path = None
    if mode == 'test':
        moveCommand = 'mv %s %s' % (ipapath, svnConfigs.test_local_path)
        svn_local_Path = svnConfigs.test_local_path
        svn_path = svnConfigs.test_svn_path
    elif mode == 'pro':
        moveCommand = 'mv %s %s' % (ipapath, svnConfigs.pro_local_path)
        svn_local_Path = svnConfigs.pro_local_path
        svn_path = svnConfigs.pro_svn_path
    os.chdir(svn_local_Path)
    print 'switchToPath %s' % os.getcwd()

    print 'move ipa file to svn path'
    result, message = commands.getstatusoutput(moveCommand)
    if result != 0:
        print message
        raise ShellError('shell error occur command is %s' % moveCommand)
    else:
        print "move success"

    ipaName = os.path.basename(ipapath)
    svnAddCommand = 'svn add %s' % ipaName
    print 'add ipa file to svn'
    result, message = commands.getstatusoutput(svnAddCommand)
    if result != 0:
        print message
        raise ShellError('shell error occur command is %s' % svnAddCommand)
    else:
        print "add success"

    svnCommitCommand = 'svn commit -m "upload %s" %s' % (ipaName, ipaName)
    print 'commit ipa file to svn'
    result, message = commands.getstatusoutput(svnCommitCommand)
    if result != 0:
        print message
        raise ShellError('shell error occur command is %s' % svnCommitCommand)
    else:
        print "commit success"
        print 'svn Path:'
        print '%s/%s' % (urllib.unquote(svn_path), ipaName)
        showMessage('Commit finished', 'svn upload ipa file success!')
