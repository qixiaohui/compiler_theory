import sys
tokens =[]


def scanner(tokenstr):
    global linenumber
    global output
    global word
    global j
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
                word+='.'
                while nextchar and nextchar.isdigit():
                    word+=nextchar
                    increment(tokenstr)
                if nextchar and nextchar not in [' ','\n',';','=','!','%','^','*','(',')','/','>','<','+','-']:
                    return error(linenumber)
                else:
                    increment(tokenstr)
            elif currentchar not in [' ','\n',';','=','!','%','^','*','(',')','/','>','<','+','-',None]:
                return error(linenumber)
            token=('T_decimalnumber',word)
            tokens.append(token)
        elif currentchar==' ':
            increment(tokenstr)
        elif currentchar.isalpha():
            word=currentchar
            while nextchar and nextchar.isalpha():
                word+=nextchar
                increment(tokenstr)
            if word in ['string','int','bool','float','global','in','out','while','if','then','else','case','for','and','or','not','program','procedure','begin','return','end']:
                token=('T_keyword',word)
                tokens.append(token)
                increment(tokenstr)
            elif nextchar and nextchar.isdigit():
                increment(tokenstr)
                word+=currentchar
                while nextchar and nextchar.isalnum():
                    increment(tokenstr)
                    word+=currentchar
                token=('T_identifier',word)
                tokens.append(token)
            elif nextchar and nextchar in ['@','#','$','&','(']:
                print nextchar
                return error(linenumber)
            else:
                token=('T_identifier',word)
                tokens.append(token)
            if nextchar:
                increment(tokenstr)
        elif currentchar =='\\':
            if currentchar=='\\':
                return 
            if nextchar:
                increment(tokenstr)
        elif currentchar in ['\n','\t','\r']:
            if nextchar:
                increment(tokenstr)
        elif currentchar in ['=','^','%','*','/','+','-','>','<']:
            word=currentchar
            if nextchar and currentchar in ['>','<','=']:
                increment(tokenstr)
                if currentchar=='=':
                    word+='='
                    if nextchar:
                        increment(tokenstr)
                token=('T_operator',word)
                tokens.append(token)
            else:
                token=('T_operator',word)
                tokens.append(token)
                if nextchar:
                    increment(tokenstr)
        elif currentchar in ['!',':']:
            if nextchar:
                word=currentchar
                increment(tokenstr)
                if currentchar=='=':
                    word+=currentword
                    token=('T_operator',word)
                    tokens.append(token)
                    if nextchar:
                        increment(tokenstr)       
        elif currentchar=='(':
            word='('
            token=('T_lparen',word)
            tokens.append(token)
            if nextchar:
                increment(tokenstr)
        elif currentchar==')':
            word=')'
            token=('T_rparen',word)
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
                token=('T_string',word)
                tokens.append(token)
            else:
                return error(linenumber)
            if nextchar:
                increment(tokenstr)
                increment(tokenstr)
        elif currentchar==';':
            token=('T_semicolon',';')
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
        currentchar=tokenstr[j]
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
    
