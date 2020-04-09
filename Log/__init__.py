#!/usr/bin/python3

import sys
import os

log_opts = { 'log': False,
             'err': True,
             'warn': True,
             'dbg': True
}

def _add_suffix2line(msg, prefix=None):
    ret = ''
    if '\n' in str(msg):
        line_cnt = 0
        for line in str(msg).split(os.linesep):
            if line_cnt == 0:
                ret += line + '\n'
            else:
                ret += str(prefix) + ' ' + line + '\n'
            line_cnt += 1
    else:
        ret = msg + ' '
    return ret


def _conc(*msg, prefix = None):
    ret = ''
    if prefix:
        ret = str(prefix) + ' '
    for t in msg:
        ret += _add_suffix2line(t, prefix=prefix)
    # stripping last space
    ret = ret[:-1]
    return ret


def dbg(*msg, prefix = 'DBG:'):
    '''
    Output *msg to stdout if dbg is set to True
    '''
    if log_opts['dbg']:
        sys.stdout.write('%s%s' % (_conc(*msg, prefix = prefix),
                                   os.linesep))


def err(*msg, prefix = 'ERR:'):
    if log_opts['err']:
        sys.stderr.write('%s%s' % (_conc(*msg, prefix = prefix),
                                   os.linesep))
        
def warn(*msg, prefix = 'WARN:'):
    if log_opts['warn']:
        sys.stdout.write('%s%s' % (_conc(*msg, prefix = prefix),
                                   os.linesep))

        
def log(*msg, prefix = 'LOG:'):
    if log_opts['log']:
        sys.stdout.write('%s%s' % (_conc(*msg, prefix = prefix),
                                   os.linesep))

    
def _set_lvl(key, bool):
    if not key in log_opts:
        raise KeyError('key not in log_opts (given: %s)' % str(key))
    if bool == True or bool == False:
        log_opts[key] = bool
    else:
        raise SyntaxError('bool should be either True or False (given: %s)'
                          % str(bool))


def set_log_lvl(bool):
    _set_lvl('log', bool)
    

def set_dbg_lvl(bool):
    _set_lvl('dbg', bool)

    
def set_err_lvl(bool):
    _set_lvl('err', bool)


def set_warn_lvl(bool):
    _set_lvl('warn', bool)

