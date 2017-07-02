from subprocess import Popen
import unittest
import os.path

from rmtest import ModuleTestCase


MODULE_PATH = os.path.abspath(os.path.dirname(__file__)) + '/' + 'module.so'


def build_module():
    csrc = MODULE_PATH[0:-3] + '.c'
    po = Popen(['cc', '-o', MODULE_PATH, '-shared', csrc])
    po.communicate()
    if po.returncode != 0:
        raise Exception('Failed to compile module')


class TestTestCase(ModuleTestCase(MODULE_PATH, module_args=('foo','bar'))):
    @classmethod
    def setUpClass(cls):
        super(TestTestCase, cls).setUpClass()
        # Check for the presence of the module
        if not os.path.exists(MODULE_PATH):
            build_module()

    def testContext(self):
        with self.redis() as r:
            with self.redis() as r:
                for _ in r.retry_with_rdb_reload():
                    self.assertOk(r.execute_command('TEST.TEST'))
                    with self.assertResponseError():
                        r.execute_command('TEST.ERR')

    def testBasic(self):
        self.assertTrue(self.server)
        self.assertTrue(self.client)
        with self.assertResponseError():
            self.cmd('TEST.ERR')


if __name__ == '__main__':
    unittest.main()