import sys
tokens =[]


def scanner(tokenstr):
    global linenumber
    global output
    global word
    global tokens
    global j
    float_sign=0
    j=0
    linenumber+=1
    increment(tokenstr)
    while nextchar:
        if currentchar.isdigit():
            word=currentchar
            while nextchar!=None and nextchar.isdigit():
                word+=nextchar
                increment(tokenstr)
            if nextchar:
                increment(tokenstr)
            if currentchar =='.':
                float_sign=1
                word+='.'
                while nextchar and nextchar.isdigit():
                    word+=nextchar
                    increment(tokenstr)
                if nextchar and nextchar not in [' ','\n',';','=','!','%','^','*','(',')','/','>','<','+','-']:
                    error(linenumber)
                else:
                    increment(tokenstr)
            elif currentchar not in [' ','\n',';','=','!','%','^','*','(',')','/','>','<','+','-',None]:
                error(linenumber)
            if float_sign==0:
                token=('T_decimalnumber',word,linenumber)
            elif float_sign==1:
                token=('T_floatnumber',word,linenumber)
            tokens.append(token)
        elif currentchar==' ':
            word=' '
            token=('T_whitespace',word,linenumber)
            tokens.append(token)
            if nextchar:
                increment(tokenstr)
        elif currentchar.isalpha():
            word=currentchar
            while nextchar and nextchar.isalpha():
                word+=nextchar
                increment(tokenstr)
                #increment(tokenstr)
            if nextchar and nextchar.isdigit():
                increment(tokenstr)
                word+=currentchar
                while nextchar and nextchar.isalnum():
                    increment(tokenstr)
                    word+=currentchar
                token=('T_identifier',word,linenumber)
                tokens.append(token)
            elif nextchar and nextchar=='_':
                increment(tokenstr)
                word+=currentchar
                while nextchar and (nextchar.isalnum() or nextchar=='_'):
                    increment(tokenstr)
                    word+=currentchar
                token=('T_identifier',word,linenumber)
                tokens.append(token)
            elif nextchar and nextchar in ['@','#','$','&']:
                print nextchar
                error(linenumber)
                if nextchar:
                    increment(tokenstr)
            elif word in ['string','integer','bool','float','global','in','out','while','if','then','else','case','for','and','or','not','program','procedure','begin','return','end','is','true','false','program']:
                token=('T_keyword',word,linenumber)
                tokens.append(token)                    
            else:
                token=('T_identifier',word,linenumber)
                tokens.append(token)
            if nextchar:
                if currentchar!='(':
                    increment(tokenstr)
        elif currentchar in ['\n','\t','\r']:
            word=' '
            token=('T_whitespace',word,linenumber)
            tokens.append(token)
            if nextchar:
                increment(tokenstr)
        elif currentchar in ['=','^','%','*','/','+','-','>','<','&','|']:
            word=currentchar
            if nextchar and currentchar in ['>','<','=']:
                increment(tokenstr)
                if currentchar=='=':
                    word+='='
                    if nextchar:
                        increment(tokenstr)
                token=('T_operator',word,linenumber)
                tokens.append(token)
            elif nextchar=='/':
                return
            else:
                token=('T_operator',word,linenumber)
                tokens.append(token)
                if nextchar:
                    increment(tokenstr)
        elif currentchar in ['!',':']:
            if nextchar:
                word=currentchar
                increment(tokenstr)
                if currentchar=='=':
                    word+=currentchar
                    token=('T_operator',word,linenumber)
                    tokens.append(token)
                    if nextchar:
                        increment(tokenstr)       
        elif currentchar=='(':
            word='('
            token=('T_lparen',word,linenumber)
            tokens.append(token)
            if nextchar:
                increment(tokenstr)
        elif currentchar==')':
            word=')'
            token=('T_rparen',word,linenumber)
            tokens.append(token)
            if nextchar:
                increment(tokenstr)
        elif currentchar=='"':
            word='"'
            while nextchar and nextchar!='"':
                word+=nextchar
                increment(tokenstr)
            if nextchar=='"':
                word+='"'
                token=('T_string',word,linenumber)
                tokens.append(token)
            else:
                error(linenumber)
                if nextchar:
                    increment(tokenstr)
            if nextchar:
                increment(tokenstr)
                increment(tokenstr)
        elif currentchar==';':
            token=('T_semicolon',';',linenumber)
            tokens.append(token)
            if nextchar:
                increment(tokenstr)
        elif currentchar==',':
            token=('T_comma',',',linenumber)
            tokens.append(token)
            if nextchar:
                increment(tokenstr)
        elif currentchar=='[':
            token=('T_lbracket','[',linenumber)
            tokens.append(token)
            if nextchar:
                increment(tokenstr)
        elif currentchar==']':
            token=('T_rbracket',']',linenumber)
            tokens.append(token)
            if nextchar:
                increment(tokenstr)
        else:
            token=('T_unknown',currentchar,linenumber)
            tokens.append(token)
            if nextchar:
                increment(tokenstr)

        


def increment(tokenstr):
    global j
    global currentchar
    global nextchar
    if j==len(tokenstr)-1:
        nextchar=None
    else:
        if tokenstr[j].isupper():
            currentchar=tokenstr[j].lower()#in case the char is in higher case
        else:
            currentchar=tokenstr[j]
        if tokenstr[j+1].isupper():
            nextchar=tokenstr[j+1].lower()#in case upper case
        else:
            nextchar=tokenstr[j+1]
    j+=1

def error(linenumber):
    global output
    print 'program has error in linenumber '+str(linenumber)



word=''
output=''
currentchar=''
nextchar=''
linenumber=0

filename=sys.argv[1]
f=open('out.txt','a')
fread=open(filename,'r')
lines=fread.readlines()

for i in lines:
    token=scanner(i)

print "Tokens:"
print "-------"
for token in tokens:
    print token
    
