# Notes
Alec Kulakowski

Commands into Anaconda Prompt:
```
>conda create -n chatbot python=2 #not3?
>source activate chatbot #didn't work, source is not a command
#some other thing here #ipaddress, msgpack-numpy,
>conda
>conda install -c conda-forge spacy
```





~/BIA660D/pyclausie-master $
#insert my path here #it worked
ipython
from pyclausie import ClausIE



python
pip freeze | grep -i ipython
python
from pyclausie import ClausIE
cl = ClausIE.get_instance()

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

note:
#Downloads\pyclausie-master\pyclausie-master
conda install -c anaconda setuptools
