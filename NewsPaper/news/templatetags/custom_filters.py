from django import template
import re

register = template.Library() 


badWords = ['Fuck', 'Bitch']

@register.filter(name='Censor') 
def Censor(value): 
    
    w=value.split()
    
    for i in range(len(w)):
        if w[i] in badWords:
            w[i] ='*******'
    string = ' '.join([str(item) for item in w])
    return string
    
    