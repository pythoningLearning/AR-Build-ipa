# -*- coding: utf-8 -*-

__author__ = 'Arms'

'''
编译xcode工程并生成ipa文件
'''

import commands
import sys
import os
import datetime
from config import xcodeBuildConfigs
from common import ShellError, Dict, toDict
from uploadsvn import uploadipa

buildConfig = toDict(xcodeBuildConfigs)

if __name__ == '__main__':
    mode = sys.argv[1]
    params = None
    cleanCommand = None
    buildCommand = None
    createIPACommand = None
    ipaPath = None
    if mode == 'debug':
        params = buildConfig.debug
        ipaPath = '~/Desktop/%s_%s_test_%s.ipa' % (
            params.project, params.version, datetime.datetime.now().strftime("%m%d%H%M"))
        buildCommand = 'xcodebuild -project %s.xcodeproj -target %s -configuration %s -sdk %s build CODE_SIGN_IDENTITY="%s" PROVISIONING_PROFILE="%s"' % (
            params.project, params.target, params.configuration, params.sdk, params.code_sign_identity, params.provisioning_profile)
        createIPACommand = 'xcrun -sdk %s PackageApplication -v build/%s-iphoneos/%s.app -o %s' % (
            params.sdk, params.configuration, params.project, ipaPath)
    elif mode == 'release':
        params = buildConfig.release
        ipaPath = '~/Desktop/%s_%s_pro_%s.ipa' % (
            params.project, params.version, datetime.datetime.now().strftime("%m%d%H%M"))
        buildCommand = 'xcodebuild -project %s.xcodeproj -target %s -configuration %s -sdk %s build CODE_SIGN_IDENTITY="%s" PROVISIONING_PROFILE="%s"' % (
            params.project, params.target, params.configuration, params.sdk, params.code_sign_identity, params.provisioning_profile)
        createIPACommand = 'xcrun -sdk %s PackageApplication -v build/%s-iphoneos/%s.app -o %s' % (
            params.sdk, params.configuration, params.project, ipaPath)
    projectPath = params.path
    currentPath = os.getcwd()

    os.chdir(projectPath)
    print 'switchToPath %s' % os.getcwd()

    print 'clean project'
    cleanCommand = 'xcodebuild -target %s clean' % params.target
    result, message = commands.getstatusoutput(cleanCommand)
    if result != 0:
        print message
        raise ShellError('shell error occur command is %s' % cleanCommand)
    else:
        print "clean success"

    print 'build project'
    result, message = commands.getstatusoutput(buildCommand)
    if result != 0:
        print message
        raise ShellError('shell error occur command is %s' % buildCommand)
    else:
        print "build success"

    print 'create ipa'
    result, message = commands.getstatusoutput(createIPACommand)
    if result != 0:
        print message
        raise ShellError('shell error occur command is %s' % buildCommand)
    else:
        print "create success"
        print 'ipa path : %s' % ipaPath

    print 'clear intermediate files generated during the build'
    clearCommand = 'rm -R ./build'
    result, message = commands.getstatusoutput(clearCommand)
    if result != 0:
        print message
        raise ShellError('shell error occur command is %s' % clearCommand)
    else:
        print "clear success"

    print 'Upload ipa file to svn?'
    print '1. upload ipa to svn test ipa path'
    print '2. upload ipa to svn pro ipa path'
    print '3. done'
    num = raw_input('please enter num: ')
    if num == '1':
        uploadipa('test', ipaPath)
    elif num == '2':
        uploadipa('pro', ipaPath)
    else:
        pass
