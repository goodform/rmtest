from rmtest import ModuleTestCase
import unittest

class TestTestCase(ModuleTestCase('./test.so', module_args=('foo','bar'))):

    def testMe(self):

        with self.redis() as r:

            with self.redis() as r:

                for _ in r.retry_with_rdb_reload():
                    self.assertOk(r.execute_command('TEST.TEST'))

                    with self.assertResponseError():
                        r.execute_command('TEST.ERR')


if __name__ == '__main__':
    unittest.main()