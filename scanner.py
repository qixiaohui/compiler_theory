j=0
def scanner(token):
    string=''
    if token=='string':
        return 'T_string '
    elif token=='int':
        return 'T_integer '
    elif token=='bool':
        return 'T_boolean '
    elif token=='float':
        return 'T_float '
    elif token=='gloabl':
        return 'T_global '
    elif token=='in':
        return 'T_in '
    elif token=='out':
        return 'T_out '
    elif token=='if':
        return 'T_if '
    elif token=='then':
        return 'T_then '
    elif token=='else':
        return 'T_else '
    elif token=='while':
        return 'T_while '
    elif token=='case':
        return 'T_case '
    elif token=='for':
        return 'T_for '
    elif token=='and':
        return 'T_and '
    elif token=='or':
        return 'T_or '
    elif token=='not':
        return 'T_not '
    elif token=='program':
        return 'T_program '
    elif token=='procedure':
        return 'T_prodecure '
    elif token=='begin':
        return 'T_begin '
    elif token=='return':
        return 'T_return '
    elif token=='end':
        return 'T_end '
    elif token=='\t':
	return ''
    elif token=='\n':
	return ''
    elif token=='\b':
	return ''
    else:
	print token
        increment(token)
        while nextchar:
	    print currentchar
            if currentchar.isalpha():
                string+='T_identifier '
                while nextchar and(nextchar.isalpha() or nextchar.isdigit()):
                    increment(token)
                increment(token)
            elif currentchar.isdigit():
                string+='T_identifier '
                while nextchar and nextchar.isdigit():
                    increment(token)
                if nextchar!=None and (nextchar.isalpha() or nextchar=='"' or nextchar==':' or nextchar==',' or nextchar=='(' or nextchar==')' or nextchar=='{' or nextchar=='}' or nextchar=='[' or nextchar==']'):
                    return 'T_error '
                elif nextchar=='.':
		    increment(token)
                    while nextchar and nextchar.isdigit():
                        increment(token)
                        continue
                    if nextchar!=None and (nextchar=='.' or nextchar.isalpha() or nextchar=='"' or nextchar==':' or nextchar==';' or nextchar==',' or nextchar=='(' or nextchar==')' or nextchar=='{' or nextchar=='}' or nextchar=='[' or nextchar==']'):
                        return 'T_error '
                increment(token)
            elif currentchar=='"':
                string+='T_qutation '+'T_string '
                while nextchar and nextchar!='"':
                    increment(token)
                if nextchar=='"':
                    string+='T_qutation '
                else:
                    return 'T_error '
                increment(token)
                increment(token)
            elif currentchar==' ':
                increment(token)
            elif currentchar==':':
                string+='T_colon '
                increment(token)
            elif currentchar=='+':
                string+='T_add '
                increment(token)
            elif currentchar=='-':
                string+='T_minus '
                increment(token)
            elif currentchar=='*':
                string+='T_multiply '
                increment(token)
	    elif currentchar=='/t':
		increment(token)
            elif currentchar=='/':
                string+='T_devide '
                incremnt(toekn)
            elif currentchar=='(':
                string+='T_parent '
                while nextchar!=')':
                    increment(token)
		    if nextchar==None:
		        return 'T_error '
                    elif currentchar.isdigit():
                        string+='T_identifier '
                        while nextchar.isdigit():
                            increment(token)
                            continue
                        if nextchar.isalpha() or nextchar=='"' or nextchar==':' or nextchar==',' or nextchar=='(' or nextchar==')' or nextchar=='{' or nextchar=='}' or nextchar=='[' or nextchar==']' or nextchar=='/t':
                            return 'T_error '
                        elif nextchar=='.':
                            while nextchar.isdigit():
                                increment(token)
                                continue
                            if nextchar=='.' or nextchar.isalpha() or nextchar=='"' or nextchar==':' or nextchar==',' or nextchar=='(' or nextchar==')' or nextchar=='{' or nextchar=='}' or nextchar=='[' or nextchar==']' or nextchar=='/t':
                                return 'T_error '
                    elif currentchar.isalpha():
                        string+='T_identifier '
                        while nextchar and (nextchar.isalpha() or nextchar.isdigit()):
                            increment(token)
                    elif currentchar=='+':
                        string+='T_add '
                    elif currentchar=='-':
                        string+='T_minus '
                    elif currentchar=='*':
                        string+='T_multiply '
                    elif currentchar=='/':
                        string+='T_devide '
                    else:
                        return 'T_error '
                increment(token)
                increment(token)
                string+='T_parent '
            elif currentchar=='<':
                string+='T_lessthan '
                increment(token)
            elif currentchar=='>':
                string+='T_biggerthan '
                increment(token)
            elif currentchar=='=':
                string+='T_equal '
                increment(token)
            elif currentchar=='!':
                string+=''
                if nextchar=='=':
                    string+='T_notequal '
                    increment(token)
                    increment(token)
                else:
                    string+='T_not '
                    increment(token)
            elif currentchar==';':
                string+='T_semicolon '
                if j!=len(token)-1:
                    return 'T_error '
                else:
                    return string
    return string

def increment(token):
    global j
    global currentchar
    global nextchar
    if j==len(token)-1:
        nextchar=None
    else:
        currentchar=token[j]
        nextchar=token[j+1]
    j+=1



currentchar=''
nextchar=''

filename=raw_input('input the file name')
f=open('out.txt','a')
fread=open(filename,'r')
lines=fread.readlines()
for i in lines:
    words=i.split(" ")
    for word in words:
        token=scanner(word)
	print token
        j=0
        f.write(token)
