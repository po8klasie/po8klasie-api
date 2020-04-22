# WarsawLO BE

## Queries
Besides normal URI syntax, you can also use OR's and AND's in GET requests.
For OR put a '|' (pipe) character between options, eg.:
```https://warsawlo.herokuapp.com/subject/?high_school_class=&id=&name=pol|hist```
should return a list of all subjects with name either "pol", "hist" or "ang".

For AND just add the param once again with a new condition, eg:
```https://warsawlo.herokuapp.com/subject/?high_school_class=&id=lt=10&id=gt=3```
should return a list of all subjects that has an ID less than 10 and greater than 3 
(syntax for ```lt``` and ```gt``` functions doesn't exist yet, it was used only to show any sensible usage of AND)

You can mix ORs and ANDs in the same request. OR has a higher precedence.