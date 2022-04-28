# data_analysis

## dependencies
``` pip install -r requirements.txt ```

## parsing

### To run unit tests, run:
``` cd parsing ```
``` python -m unittest discover ```

### To run consolidator:
``` python pmn_table_consolidator.py```

This functionality expects pmn.txt in format:

```
country;dial_code;operator_prefix;msn;operator_name
Ukraine;380;67;data;UKRKS
Ukraine;380;98;data;UKRKS
Ukraine;380;50;data;UKRUM
Ukraine;380;95;data;UKRUM
Ukraine;380;66;data;UKRUM
Ukraine;380;63;data;URKAS
```

From content above script returns:

```
"Ukraine","380","67;98","data","UKRKS"
"Ukraine","380","50;95;66","data","UKRUM"
"Ukraine","380","63","data","URKAS"
```