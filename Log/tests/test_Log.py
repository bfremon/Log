#!/usr/bin/python3

import unittest
import os
import stat
import Cmd
import pandas
import Log 

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
        s = Log._conc('prt', prefix=None)
        self.assertTrue(s == 'prt')
        s = Log._conc('prt', prefix='PRT:')
        self.assertTrue(s == 'PRT: prt')
        s = Log._conc('prt', prefix=True)
        self.assertTrue(s == 'True prt')
        s = Log._conc('prt', 'per', 'pr', prefix=True)
        self.assertTrue(s == 'True prt per pr')
        df = pandas.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6],
                               'c': [7, 8, 9]})
        s = Log._conc(df.head(), prefix = 'LOG:')
        str_df = ''
        for l in str(df).split('\n'):
            str_df += 'LOG: ' + l + '\n'
        self.assertTrue(str_df[:-1] == s)
        tmp_p = os.path.join(os.getcwd(), 'tmp')
        os.mkdir(tmp_p)
        tmp1_f_p = os.path.join(tmp_p, 'tmp1')
        f1_w = open(tmp1_f_p, 'w')
        f1_w.write('1')
        f1_w.close()
        tmp2_f_p = os.path.join(tmp_p, 'tmp2')
        f2_w = open(tmp2_f_p, 'w')
        f2_w.write('1')
        f2_w.close()
        s = Log._conc('prt', os.listdir(tmp_p))
        self.assertTrue(s == "prt ['tmp2', 'tmp1']")
        os.unlink(tmp1_f_p)
        os.unlink(tmp2_f_p)
        os.rmdir(tmp_p)
            
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
            
