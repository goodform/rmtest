# rmtest

A simple nano-framework for testing redis modules using python unit test, and a disposable ephemeral redis subprocess.

## Example:

```py

from rmtest import ModuleTestCase

class MyTestCase(ModuleTestCase('../module.so')):
    
            
    def testCmd(self):
        with self.redis() as r:
            
            self.assertOk(r.execute_command('mymodule.dosomething', 'foo', 'bar'))
               
```

## Install

1. Clone this repo

2. `sudo python setup.py install`
