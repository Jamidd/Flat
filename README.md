# FLAT
FLAT is a **F**ormal **L**anguage to **A**utomaton **T**ransmogrifier. It compiles many temporally extended objective specification languages to DFA or [Reward Machine](https://www.ijcai.org/Proceedings/2019/840).
This tool is also available as a web service at [fl-at.herokuapp.com](fl-at.herokuapp.com).

## Dependencies
FLAT is built on top on MONA, which you can obtain [here](https://www.brics.dk/mona/download.html).  
It is also based on a few dependencies:  
[dd](https://pypi.org/project/dd/)  
[ply](https://pypi.org/project/ply/)  
[PySimpleAutomata](https://pypi.org/project/PySimpleAutomata/)  

On a linux based system, it will ask you to install all necesary dependencies automagically the first time you run the program. You can review all the installed packages at [functions/dependencies.sh](https://github.com/Jamidd/Flat/blob/master/functions/dependencies.sh).
