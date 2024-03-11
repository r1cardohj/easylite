# easylite
就是sqlite包一层

``` python
from core import EasyLite
from datetime import date

db = EasyLite('test.db')

db.create_table('boss',
                name=str,
                age=int,
                birthday=date)


db.insert('boss', name='John', age=14, birthday=date.today())
```
