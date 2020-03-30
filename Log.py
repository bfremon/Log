#!/usr/bin/python3

import sys
import os

log_opts = { 'log': False,
             'err': True,
             'warn': True,
             'dbg': True
}


def _conc(*msg, suffix = None):
    ret = ''
    if suffix:
        ret = str(suffix) + ' '
    if len(msg) == 1:
        ret += str(msg[0])
    else:
        idx = 0
        for t in msg:
            if idx < len(msg) - 1:
                ret += str(t) + ' '
            else:
                ret += str(t)
            idx += 1
    return ret


def dbg(*msg, suffix = 'DBG:'):
    if log_opts['dbg']:
        sys.stdout.write('%s%s' % (_conc(*msg, suffix = suffix),
                                   os.linesep))


def err(*msg, suffix = 'ERR:'):
    if log_opts['err']:
        sys.stderr.write('%s%s' % (_conc(*msg, suffix = suffix),
                                   os.linesep))

        
def warn(*msg, suffix = 'WARN:'):
    if log_opts['warn']:
        sys.stdout.write('%s%s' % (_conc(*msg, suffix = suffix),
                                   os.linesep))

        
def log(*msg, suffix = 'LOG:'):
    if log_opts['log']:
        sys.stdout.write('%s%s' % (_conc(*msg, suffix = suffix),
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


if __name__ == '__main__':
    import unittest
    import os
    import stat
    import Cmd
    
    class test_Log(unittest.TestCase):

        test_dir = os.path.join(os.getcwd())
        
        def _write_script(self, fname, string):
            full_p = os.path.join(self.test_dir, fname)
            if os.path.exists(full_p):
                try:
                    os.unlink(full_p)
                except IOError:
                    print('impossible to remove ' + full_p)
            try: 
                f_w = open(full_p, 'w')
            except IOError: 
                print('error in creating script ' + str(full_p))
                f_w.close()
            f_w.write('%s' % string)
            f_w.close()
            os.chmod(full_p, stat.S_IXUSR|stat.S_IRUSR)

            
        def _get_script_output(self, pyfile, f=None):
            script_path = os.path.join(self.test_dir, pyfile)
            assert os.path.exists(script_path), 'file ' + script_path + \
                " doesn't exist"
            cmd = '/usr/bin/env python3 ' + script_path
            out = Cmd.run_cmd(cmd, ret=False)
            return out


        def test__conc(self):
            s = _conc('prt', suffix=None)
            self.assertTrue(s == 'prt')
            s = _conc('prt', suffix='PRT:')
            self.assertTrue(s == 'PRT: prt')
            s = _conc('prt', suffix=True)
            self.assertTrue(s == 'True prt')
            s = _conc('prt', 'per', 'pr', suffix=True)
            self.assertTrue(s == 'True prt per pr')


        def _test_func(self, func):
            test_f = os.path.join(self.test_dir, 'test_'+ func + '.py')
            s = '#!/usr/bin/python3' + os.linesep \
            + 'from Log import *' + os.linesep \
            + 'set_' + func + '_lvl(True)' + os.linesep \
            + func + '(\"prat\") ' + os.linesep
            self._write_script(test_f, s)
            out = self._get_script_output(test_f)
            self.assertTrue(out[0] == func.upper() + ': prat')
            os.unlink(test_f)
            test_f = os.path.join(self.test_dir, 'test_' + func+ '.py')
            s = '#!/usr/bin/python3' + os.linesep \
                + 'from Log import *' + os.linesep \
                + 'set_' + func + '_lvl(False)' + os.linesep \
                + func + '(\"prat\")' + os.linesep
            self._write_script(test_f, s)
            out = self._get_script_output(test_f)
            self.assertTrue(out[0] == '')
            os.unlink(test_f)

            
        def test_dbg(self):
            self._test_func('dbg')

            
        def test_err(self):
            self._test_func('err')

            
        def test_warn(self):
            self._test_func('warn')

            
        def test_log(self):
            self._test_func('log')
            
    unittest.main()
