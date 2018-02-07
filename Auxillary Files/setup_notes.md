# Notes
Alec Kulakowski

Commands into Anaconda Prompt:
```{Anaconda Prompt}
>conda create -n chatbot python=2 #not3?
>source activate chatbot #didn't work, source is not a command
#some way to check which things you have installed
#some other thing here #ipaddress, msgpack-numpy, like 30 others
>conda
>conda install -c conda-forge spacy
```

```{Anaconda Prompt}
~/BIA660D/pyclausie-master $
#insert my path here
```
^^ this worked
```{Anaconda Prompt}
ipython
from pyclausie import ClausIE
```

```{Anaconda Prompt}
python
pip freeze | grep -i ipython
python
from pyclausie import ClausIE
cl = ClausIE.get_instance()
```

## Issues

pyclausie issues:
```{Anaconda Prompt}
(base) C:\Users\usr>python2.7
>>> from pyclausie import ClausIE
ImportError: No module called pyclausie
```
```{Anaconda Prompt}
(base) C:\Users\usr>python
>>> from pyclausie import ClausIE
SyntaxError: invalid syntax
```

## Actions done not mentioned by teacher:
#Downloads\pyclausie-master\pyclausie-master
conda install -c anaconda setuptools
