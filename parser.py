import scanner_rev1
from scanner_rev1 import scanner

import inspect

print '******************'



class symbol:
    def __init__(self):
        self.type=None
        self.value=None
        self.address=None
        self.line=None
        self.format=None
        self.label=None
        self.parameter_in=None #used by procedure num of input parameter
        self.parameter_out=None # used by procedure num of output parameter
        self.arraysize=None
        self.array_check=0#0 means it's not an array, 1 means it's an array
        self.return_address=None

def lineno():
    """Returns the current line number in our program."""
    print inspect.currentframe().f_back.f_lineno   
    

def getnext():
    global n
    global currenttoken
    global currenttokenqueue
    currenttoken=symbol()
    currenttoken.type=scanner_rev1.tokens[n][0]
    currenttoken.value=scanner_rev1.tokens[n][1]
    currenttoken.line=scanner_rev1.tokens[n][2]
    print currenttoken.value
    currenttokenqueue.append(currenttoken)
    n+=1
    if currenttoken.type=='T_whitespace':
        getnext()


def skipline():
    global linenumber
    linenumber=currenttoken.line
    while currenttoken.line==linenumber:
        getnext()
    
    
def reporterror():
    print 'ERROR ERROR ERROR ERROR ERROR'  

    
    


def program():
    global n
    getnext()
    programheader()
    programbody()

def programheader():
    global skip
    skip=0
    if currenttoken.type=='T_keyword' and currenttoken.value=='program':
        getnext()
    else:
        print "missing program at line ",currenttoken.line
    fwrite.write("\n#include <stdlib.h>")
    fwrite.write("\n#include <stdio.h>")
    fwrite.write("\n#include <string.h>")
    fwrite.write("\n#include <stdbool.h>")
    fwrite.write("\nunion T_union{")
    fwrite.write("\nint i;")
    fwrite.write("\nchar c;")
    fwrite.write("\nfloat f;")
    fwrite.write("\nbool b;")
    fwrite.write("\n}R[100],MM[1200];")
    fwrite.write("\nint main()")
    fwrite.write("\n{")
    fwrite.write("\nint procedurelabel;")
    fwrite.write("\nprocedurelabel=0;")
    fwrite.write("\nint return_address;")
    fwrite.write("\ngoto main;")
    if currenttoken.type=='T_identifier':
        getnext()
    else:
        print "missing program name at line ",currenttoken.line
    if currenttoken.type=='T_keyword' and currenttoken.value=='is':
        getnext()
    else:
        print "missing word is at line ",currenttoken.line


def programbody():
    global skip
    declaration()
    skip=0
    if currenttoken.type=='T_keyword' or currenttoken.value=='begin':
        getnext()
    else:
        print "missing word begin at line ",currenttoken.line
    fwrite.write("\nmain:")
    statement()
    if currenttoken.type=='T_keyword' and currenttoken.value=='end':
        getnext()
    else:
        print "missing word end at line ",currenttoken.line
    if currenttoken.type!='T_keyword' or currenttoken.value!='program':
        print "missing word program at line ",currenttoken.line
    fwrite.write("\nreturn 0;")
    fwrite.write("\n}")
    print 'done'


def declaration():
    while currenttoken.type=='T_keyword' and currenttoken.value in ['procedure','integer','float','bool','string','global']:
        if currenttoken.value=='global':
            getnext()
        if currenttoken.value=='procedure':
            proceduredeclaration()
        else:
            variabledeclaration()


def proceduredeclaration():
    global procedurecall
    global parameterstack
    global symboltablelocal
    global stack
    global proceduredec
    procedurecall=1
    proceduredec=0
    procedureheader()
    procedurebody()
    procedurecall=0
    parameterstack=900
    stack=1000
    proceduredec=1
    symboltablelocal.clear()#clear the local variable after jump out of the procedure

def procedureheader():
    global typecheck
    global symboltable
    global label
    global stack
    global procedurename
    global procedurelabel1
    if currenttoken.type=='T_keyword' and currenttoken.value=='procedure':
        getnext()
    else:
        print "missing word procedure at line ",currenttoken.line
    if currenttoken.type=='T_identifier':
        typecheck[currenttoken.value]='procedure'
        symboltable[currenttoken.value]=currenttoken
        symboltable[currenttoken.value].label=label
        symboltable[currenttoken.value].format='procedure'
        procedurename=currenttoken.value#assign the name of current procedure
        symboltable[currenttoken.value].parameter_in=0;
        symboltable[currenttoken.value].parameter_out=0;
        getnext()
        #fwrite.write("\ngoto *procedure_ptr;")
        fwrite.write("\nlabel%s:"%label)
        currenttoken.label=label
        label=label+1
    else:
        print "missing procedure name at line ",currenttoken.line
    if currenttoken.type=='T_lparen' and currenttoken.value=='(':
        getnext()
    else:
        print "missing left parentheses at line ",currenttoken.line
        fwrite.write("Currenttoken%s"%currenttoken.value)
    if currenttoken.type!='T_rparen' or currenttoken.value!=')':
        parameterlist()
        symboltable[procedurename].return_address=symboltable[procedurename].parameter_in+symboltable[procedurename].parameter_out;
    if currenttoken.type=='T_rparen' and currenttoken.value==')':
        getnext()
        stack+=1
        symboltable[procedurename].return_address=0;
    else:
        print "missing right parentheses at line ",currenttoken.line
        symboltable[procedurename].return_address=0;


def parameterlist():
    global parameterstack
    parameter()
    if currenttoken.type=='T_comma' and currenttoken.value==',':
        getnext()
        parameterlist()
        parameterstack+=1
    elif currenttoken.type=='T_keyword':
        print "missing comma at line ",currenttoken.line
        parameterlist()
        parameterstack+=1
    parameterstack+=1



def parameter():
    global symboltable
    global procedurename
    global parameterdec
    parameterdec=1
    variabledeclaration()
    if currenttoken.type!='T_keyword' or (currenttoken.value not in ['in','out']):
        print "missing word in or out at line ",currenttoken.line
    elif currenttoken.value=='in':
        symboltable[procedurename].parameter_in+=1#increment the number of input parameter
        getnext()
    elif currenttoken.value=='out':
        symboltable[procedurename].parameter_out+=1# same thing with output parameter
        getnext()
    parameterdec=0

def variabledeclaration():
    global pointer
    global symboltable
    global MM
    global procedurecall
    global pointerlocal
    global stack
    register=[]
    register.append(typemark())
    if currenttoken.type=='T_identifier':
        currenttoken.format=register[0]
        currenttoken.address=pointer
        register.append(currenttoken.value)
        if procedurecall==0:
            symboltable[currenttoken.value]=currenttoken
            pointer+=1
        elif procedurecall==1:
            currenttoken.address=stack #give the stack address to local variable
            symboltablelocal[currenttoken.value]=currenttoken
            stack+=1
        getnext()
    else:
        print "can't tell the identifier"
    if currenttoken.type=='T_lbracket' and currenttoken.value=='[':
        getnext()
        register.append(arraysize())
        if procedurecall==0:
            symboltable[register[1]].arraysize=register[2]
            symboltable[register[1]].array_check=1
            pointer=pointer+ int (register[2])-1#assign address for the array in memory
        elif procedurecall==1:
            symboltablelocal[register[1]].arraysize=register[2]
            symboltablelocal[register[1]].array_check=1
            stack=stack+ int (register[2])-1#assign address for the local array on stack
        if currenttoken.type=='T_rbracket' and currenttoken.value==']':
            getnext()
        else:
            print "missing right bracket at line ",currenttoken.line
    else:
        if currenttoken.type=='T_decimalnumber':
            "missing left bracket at line ",currenttoken.line
            register.append(arraysize())
            if procedurecall==0:
                symboltable[register[1]].arraysize=register[2]
                symboltable[register[1]].array_check=register[2]
                pointer=pointer+ int (register[2])-1#assign address for the array in memory
            elif procedurecall==1:
                symboltablelocal[register[1]].arraysize=register[2]
                symboltablelocal[register[1]].array_check=register[2]
                stack=stack+ int (register[2])-1#assign address for the local array on stack
            if currenttoken.type=='T_rbracket' and currenttoken.value==']':
                getnext()
            else:
                print "missing right bracket at line ",currenttoken.line
    if currenttoken.type=='T_semicolon' and currenttoken.value==';' and procedurecall==0:
        getnext()
    elif currenttoken.type=='T_semicolon' and currenttoken.value==';' and procedurecall==1:
        getnext()
    elif currenttoken.type=='T_comma' and currenttoken.value==',' and procedurecall==1:
        pass
    elif currenttoken.type=='T_keyword' and currenttoken.value=='in' and procedurecall==1:
        pass
    elif currenttoken.type=='T_keyword' and currenttoken.value=='out' and procedurecall==1:
        pass
    else:
        print "missing semicolon or comma at line ",currenttoken.line
       

def arraysize():
    register=[]
    if currenttoken.type=='T_decimalnumber':
        register.append(currenttoken.value)
        getnext()
        return register[0]#return the value for array size
    else:
        reporterror()
        lineno()
def typemark():
    register=[]
    if currenttoken.type=='T_keyword' and (currenttoken.value=='integer' or currenttoken.value=='float' or currenttoken.value=='bool' or currenttoken.value=='string'):
        register.append(currenttoken.value)
        getnext()
        return register[0]
    else:
        reporterror()
        lineno()

def procedurebody():
    global label
    global loadparameter
    global procedurelabel1
    global procedurename
    global symboltable
    global stack
    global returnstack
    declaration()
    if currenttoken.type=='T_keyword' and currenttoken.value=='begin':
        getnext()
        # loadparameter=1 means the parameter load from function needs to be loaded
    else:
        print "missing begin at line ",currenttoken.line
    statement()
    print "currenttoken"
    print currenttoken.value
    if currenttoken.type=='T_keyword' and currenttoken.value=='end':
        getnext()
    else:
        print "missing end at line ",currenttoken.line
    stack=1000
    for i in range(0,symboltable[procedurename].parameter_out):
        fwrite.write("\nMM[MM[%s].i].i=MM[%s].i;"%(returnstack+i,stack+symboltable[procedurename].parameter_in+i))#assign the value from stack to the address of var
    fwrite.write("\nreturn_address=MM[%s].i;"%(stack+symboltable[procedurename].parameter_in+symboltable[procedurename].parameter_out))
    if currenttoken.type=='T_keyword' and currenttoken.value=='procedure':
        getnext()
    else:
        print "missing procedure at line ",currenttoken.line
    if currenttoken.type=='T_semicolon' and currenttoken.value==';':
        getnext()
    else:
        print "missing semicolon at line ",currenttoken.line-1
    fwrite.write("\ngoto *(void *) return_address;")
    #fwrite.write("\n*procedure_ptr:")
    #fwrite.write("\nprocedurelabel+=1;")
    procedurelabel1+=1


def statement():
    register=[]
    global symboltable
    global MM
    global n
    global i
    global procedurecall
    global loadparameter
    global procedurelabel
    global inlocal
    global stack
    global proceduredec
    global parameterin
    global parameterout
    global procedurename
    global variablename
    global array
    global label
    global recursion
    while ((currenttoken.type=='T_keyword' and (currenttoken.value in ['if','for','return'])) or currenttoken.type=='T_identifier'):
        i=0
        if currenttoken.type=='T_keyword' and currenttoken.value=='if':
            ifstatement()
        elif currenttoken.type=='T_keyword' and currenttoken.value=='for':
            loopstatement()
        elif currenttoken.type=='T_keyword' and currenttoken.value=='return':
            returnstatement()
        elif currenttoken.type=='T_identifier':
            inlocal=1#default the in function assignment variable in in local
            if (((currenttoken.value in symboltable.keys())) and (procedurecall==0)):#out of function
                pass
            elif(((currenttoken.value in symboltablelocal.keys())) and (procedurecall==1)):#in function
                inlocal=1
            elif(((currenttoken.value in symboltable.keys())) and (procedurecall==1)):
                inlocal=0
            else:
                print "no such variable ",currenttoken.value," at line ",currenttoken.line
            register.append(currenttoken.value)
            variablename=currenttoken.value#assign the name of variable to the global variable name
            if (currenttoken.value in symboltable.keys()) and symboltable[currenttoken.value].format=='procedure':
                getnext()
                parameterin=symboltable[register[0]].parameter_in#assign the value of the input parameter
                parameterout=symboltable[register[0]].parameter_out#same case of output parameter
                procedurecall1()
                fwrite.write("\ngoto label%s;"%symboltable[register[0]].label)
                if loadparameter==1:# only write this in procedure call, exclude from recursion 
                    fwrite.write("\nprocedure_ptr%s:"%procedurelabel)
                    procedurelabel+=1 #assign new value to preocedure label
                    #fwrite.write("\nprocedurelabel+=1;")
                procedurecall=0
                if currenttoken.value==';':# missing semicolon
                    getnext()
                else:
                    print "missing semicolon at line ",currenttoken.line#if not miss then skip semicolon
                register.pop()
                loadparameter=0 #mark that the procedure call is over
            else:
                getnext()
                register.append(assignmentstatement())
                if register[0]!=None and register[1]!=None:
                    if procedurecall==0 and proceduredec==1:
                        MM[symboltable[register[0]].address+array]=register[1]
                        if symboltable[register[0]].array_check==1:# it's an array
                            if(symboltable[register[0]].format=='integer' and (type(register[1]) is int)):
                                fwrite.write("\nMM[R[0].i].i=R[1].i;")
                            elif symboltable[register[0]].format=='float' and (type(register[1]) is float):
                                fwrite.write("\nMM[R[0].i].f=R[1].f;")
                            elif symboltable[register[0]].format=='float' and (type(register[1]) is int):
                                fwrite.write("\nMM[R[0].i].f=R[1].i;") 
                            elif symboltable[register[0]].format=='integer' and (type(register[1]) is float):
                                fwrite.write("\nMM[R[0].i].i=R[1].f;")  
                            elif symboltable[register[0]].format=='char' and (register[1].isalpha() and len(register[1])==1):
                                fwrite.write("\nMM[R[0].i].c=R[1].c;")  
                            elif symboltable[register[0]].format=='bool' and (type(register[1]) is bool):
                                fwrite.write("\nMM[R[0].i].b=R[1].b;")    
                            elif symboltable[register[0]].format=='bool' and ((type(register[1]) is int) and (register[1] in [0,1])):  
                                fwrite.write("\nMM[R[0].i].b=R[1].i;")     
                            else:
                                print "type error at line ",currenttoken.line  
                        elif symboltable[register[0]].array_check==0:
                            if(symboltable[register[0]].format=='integer' and (type(register[1]) is int)):
                                fwrite.write("\nMM[%s].i=R[0].i;"%symboltable[register[0]].address)
                            elif symboltable[register[0]].format=='float' and (type(register[1]) is float):
                                fwrite.write("\nMM[%s].f=R[0].f;"%symboltable[register[0]].address)
                            elif symboltable[register[0]].format=='float' and (type(register[1]) is int):
                                fwrite.write("\nMM[%s].f=R[0].i;"%symboltable[register[0]].address) 
                            elif symboltable[register[0]].format=='integer' and (type(register[1]) is float):
                                fwrite.write("\nMM[%s].i=R[0].f;"%symboltable[register[0]].address)  
                            elif symboltable[register[0]].format=='char' and (register[1].isalpha() and len(register[1])==1):
                                fwrite.write("\nMM[%s].c=R[0].c;"%symboltable[register[0]].address)  
                            elif symboltable[register[0]].format=='bool' and (type(register[1]) is bool):
                                fwrite.write("\nMM[%s].b=R[0].b;"%symboltable[register[0]].address)    
                            elif symboltable[register[0]].format=='bool' and ((type(register[1]) is int) and (register[1] in [0,1])):  
                                fwrite.write("\nMM[%s].b=R[0].i;"%symboltable[register[0]].address)     
                            else:
                                print "type error at line ",currenttoken.line  
                        if forloop==1:
                            break       
                        register.pop()
                        register.pop()
                    elif procedurecall==1 and proceduredec==0:
                        if inlocal==1:
                            MM[symboltablelocal[register[0]].address+array]=register[1]
                            if symboltablelocal[register[0]].array_check==1:# it's an array                            
                                if(symboltablelocal[register[0]].format=='integer' and (type(register[1]) is int)):
                                    fwrite.write("\nMM[R[0].i].i=R[1].i;")
                                elif symboltablelocal[register[0]].format=='float' and (type(register[1]) is float):
                                    fwrite.write("\nMM[R[0].i].f=R[1].f;")
                                elif symboltablelocal[register[0]].format=='float' and (type(register[1]) is int):
                                    fwrite.write("\nMM[R[0].i].f=R[1].i;") 
                                elif symboltablelocal[register[0]].format=='integer' and (type(register[1]) is float):
                                    fwrite.write("\nMM[R[0].i].i=R[1].f;")  
                                elif symboltablelocal[register[0]].format=='char' and (register[1].isalpha() and len(register[1])==1):
                                    fwrite.write("\nMM[R[0].i].c=R[1].c;")  
                                elif symboltablelocal[register[0]].format=='bool' and (type(register[1]) is bool):
                                    fwrite.write("\nMM[R[0].i].b=R[1].b;")    
                                elif symboltablelocal[register[0]].format=='bool' and ((type(register[1]) is int) and (register[1] in [0,1])):  
                                    fwrite.write("\nMM[R[0].i].b=R[1].i;")     
                                else:
                                    print "type error at line ",currenttoken.line  
                            elif symboltablelocal[register[0]].array_check==0:# it's an array
                                if(symboltablelocal[register[0]].format=='integer' and (type(register[1]) is int)):
                                    fwrite.write("\nMM[%s].i=R[0].i;"%symboltablelocal[register[0]].address)
                                elif symboltablelocal[register[0]].format=='float' and (type(register[1]) is float):
                                    fwrite.write("\nMM[%s].f=R[0].f;"%symboltablelocal[register[0]].address)
                                elif symboltablelocal[register[0]].format=='float' and (type(register[1]) is int):
                                    fwrite.write("\nMM[%s].f=R[0].i;"%symboltablelocal[register[0]].address) 
                                elif symboltablelocal[register[0]].format=='integer' and (type(register[1]) is float):
                                    fwrite.write("\nMM[%s].i=R[0].f;"%symboltablelocal[register[0]].address)  
                                elif symboltablelocal[register[0]].format=='char' and (register[1].isalpha() and len(register[1])==1):
                                    fwrite.write("\nMM[%s].c=R[0].c;"%symboltablelocal[register[0]].address)  
                                elif symboltablelocal[register[0]].format=='bool' and (type(register[1]) is bool):
                                    fwrite.write("\nMM[%s].b=R[0].b;"%symboltablelocal[register[0]].address)    
                                elif symboltablelocal[register[0]].format=='bool' and ((type(register[1]) is int) and (register[1] in [0,1])):  
                                    fwrite.write("\nMM[%s].b=R[0].i;"%symboltablelocal[register[0]].address)     
                                else:
                                    print "type error at line ",currenttoken.line  
                            if forloop==1:
                                break 
                            register.pop()
                            register.pop()
                        elif inlocal==0:
                            MM[symboltable[register[0]].address+array]=register[1]
                            if symboltable[register[0]].array_check==1:# it's an array
                                if(symboltable[register[0]].format=='integer' and (type(register[1]) is int)):
                                    fwrite.write("\nMM[R[0].i].i=R[1].i;")
                                elif symboltable[register[0]].format=='float' and (type(register[1]) is float):
                                    fwrite.write("\nMM[R[0].i].f=R[1].f;")
                                elif symboltable[register[0]].format=='float' and (type(register[1]) is int):
                                    fwrite.write("\nMM[R[0].i].f=R[1].i;") 
                                elif symboltable[register[0]].format=='integer' and (type(register[1]) is float):
                                    fwrite.write("\nMM[R[0].i].i=R[1].f;")  
                                elif symboltable[register[0]].format=='char' and (register[1].isalpha() and len(register[1])==1):
                                    fwrite.write("\nMM[R[0].i].c=R[1].c;")  
                                elif symboltable[register[0]].format=='bool' and (type(register[1]) is bool):
                                    fwrite.write("\nMM[R[0].i].b=R[1].b;")    
                                elif symboltable[register[0]].format=='bool' and ((type(register[1]) is int) and (register[1] in [0,1])):  
                                    fwrite.write("\nMM[R[0].i].b=R[1].i;")     
                                else:
                                    print "type error at line ",currenttoken.line  
                            elif symboltable[register[0]].array_check==0:
                                if(symboltable[register[0]].format=='integer' and (type(register[1]) is int)):
                                    fwrite.write("\nMM[%s].i=R[0].i;"%symboltable[register[0]].address)
                                elif symboltable[register[0]].format=='float' and (type(register[1]) is float):
                                    fwrite.write("\nMM[%s].f=R[0].f;"%symboltable[register[0]].address)
                                elif symboltable[register[0]].format=='float' and (type(register[1]) is int):
                                    fwrite.write("\nMM[%s].f=R[0].i;"%symboltable[register[0]].address) 
                                elif symboltable[register[0]].format=='integer' and (type(register[1]) is float):
                                    fwrite.write("\nMM[%s].i=R[0].f;"%symboltable[register[0]].address)  
                                elif symboltable[register[0]].format=='char' and (register[1].isalpha() and len(register[1])==1):
                                    fwrite.write("\nMM[%s].c=R[0].c;"%symboltable[register[0]].address)  
                                elif symboltable[register[0]].format=='bool' and (type(register[1]) is bool):
                                    fwrite.write("\nMM[%s].b=R[0].b;"%symboltable[register[0]].address)    
                                elif symboltable[register[0]].format=='bool' and ((type(register[1]) is int) and (register[1] in [0,1])):  
                                    fwrite.write("\nMM[%s].b=R[0].i;"%symboltable[register[0]].address)     
                                else:
                                    print "type error at line ",currenttoken.line 
                            if forloop==1:
                                break 
                            register.pop()
                            register.pop()
                    else:
                        print "no value assigned at line ",currenttoken.line
                    array=0#reassign 0 to array in case the next variable is not a array
                getnext()
                
            
            
      

def procedurecall1():
    global procedurecall
    if currenttoken.type=='T_lparen' and currenttoken.value=='(':
        getnext()
        argumentlist()
    elif currenttoken.type=='T_decimalnumber' or currenttoken.type=='T_floatnumber' or currenttoken.type=='T_string' or currenttoken.type=='T_identifier':
        print "missing left parenthese at line ",currenttoken.line
        argumentlist()
    if currenttoken.type=='T_rparen' and currenttoken.value==')':
        getnext()
    else:
        print "missing right parenthese at line ",currenttoken.line

    
        
        
def assignmentstatement():
    register=[]  
    destination()
    if currenttoken.type=='T_operator' and currenttoken.value==':=':
        getnext()
        register.append(expression())
    else:
        print "missing assignment symbol at line ",currenttoken.line
    return register[0]

def destination():
    global variablename
    global procedurecall
    global symboltable
    global symboltablelocal
    global array
    global i
    register=[]
    if currenttoken.type=='T_lbracket' and currenttoken.value=='[':
        getnext()
        register.append(expression())
        if procedurecall==0:#not in a procedure
            if int(symboltable[variablename].arraysize)>int(register[0]):#if the index is within range
                array=register[0]
            elif int(symboltable[variablename].arraysize)<=int(register[0]):#index out of range
                array=0
                print "index out of range at line ",currenttoken.line
        elif procedurecall==1:#in a procedure
            if(variablename in symboltablelocal.keys()):
                if int(symboltablelocal[variablename].arraysize)>int(register[0]):#local variable
                    array=register[0]                
                elif int(symboltablelocal[variablename].arraysize)<=int(register[0]):
                    array=0
                    print "index out of range at line ",currenttoken.line 
            elif (variablename in symboltable.keys()):
                if int(symboltable[variablename].arraysize)>int(register[0]):#if the index is within range
                    array=register[0]
                elif int(symboltable[variablename].arraysize)<=int(register[0]):#index out of range
                    array=0
                    print "index out of range at line ",currenttoken.line            
        if currenttoken.type=='T_rbracket' and currenttoken.value==']':
            getnext()
        else:
            print "missing right bracket at line ",currenttoken.line
        i+=1
    elif currenttoken.type=='T_decimalnumber' or currenttoken.type=='T_identifier':
        print "missing left bracket at line ",currenttoken.line
        register.append(expression())
        if procedurecall==0:#not in a procedure
            if symboltable[variablename].arraysize>register[0]:#if the index is within range
                array=register[0]
            elif symboltable[variablename].arraysize<=register[0]:#index out of range
                print "index out of range at line ",currenttoken.line
        elif procedurecall==1:#in a procedure
            if symboltbalelocal[variablename].arraysize>register[0]:#local variable
                array=register[0]                
            elif symboltablelocal[variablename].arraysize<=register[0]:
                print "index out of range at line ",currenttoken.line 
        if currenttoken.type=='T_rbracket' and currenttoken.value==']':
            getnext()  
        else:
            print "missing right bracket at line ",currenttoken.line      
        i+=1
def ifstatement():
    global ifmark
    global skip
    global label
    ifmark=1
    register=[]
    skip=0
    if currenttoken.type=='T_keyword' and currenttoken.value=='if':
        getnext()
    if currenttoken.type=='T_lparen' and currenttoken.value=='(':
        getnext()
    else:
        print "missing left parenthese at line ",currenttoken.line
    register.append(expression())
    if(type(register[0]) is bool):
        fwrite.write("\nif(R[0].b==true) goto iflabel%s;"%label)
    elif(type(register[0]) is int):
        fwrite.write("\nif(R[0].i==0) goto iflabel%s;"%label)
    label+=2
    ifmark=0
    if currenttoken.type=='T_rparen' and currenttoken.value==')':
        getnext()
    else:
        print "missing right parenthese at line ",currenttoken.line
    if currenttoken.type=='T_keyword' and currenttoken.value=='then':
        getnext()
    else:
        print "missing then at line ",currenttoken.line
    statement()
    label-=2
    fwrite.write("\ngoto iflabel%s;"%(label+1))
    fwrite.write("\niflabel%s:"%(label))
    if currenttoken.type=='T_keyword' and currenttoken.value=='else':
        getnext()
        statement()
        fwrite.write("\niflabel%s:"%(label+1))
    else:
        fwrite.write("\niflabel%s:"%(label+1))
    if currenttoken.type=='T_keyword' and currenttoken.value=='end':
        getnext()
    else:
        print "missing word end at line ",currenttoken.line
    if currenttoken.type=='T_keyword' and currenttoken.value=='if':
        getnext()
    else:
        print "missing word if at line ",currenttoken.line
    if currenttoken.type=='T_semicolon' and currenttoken.value==';':
        getnext()
    else:
        print "missing semicolon at line ",currenttoken.line
    recursion=0
    #if_lable_global=if_label_local#assign the value of local if back to global if

    

                     
                    
def loopstatement():
    register=[]
    global skip
    global label
    global forloop
    skip=0
    forloop=1
    if currenttoken.type=='T_keyword' and currenttoken.value=='for':
        getnext()
    if currenttoken.type=='T_lparen' and currenttoken.value=='(':
        getnext()
    else:
        print "missing right parenthese at line ",currenttoken.line
    fwrite.write("\nlabel%s:"%label)
    statement()
    getnext()
    register.append(expression())
    label=label+1
    fwrite.write("\nif(R[2].i==0) goto label%s;"%label)
    getnext()
    forloop=0
    statement()
    fwrite.write("\ngoto label%s;"%(label-1))
    fwrite.write("\nlabel%s:"%label)
    print currenttoken.type
    if currenttoken.type=='T_keyword' and currenttoken.value=='end':
        getnext()
    else:
        print "missing word end at line ",currenttoken.line
    if currenttoken.type=='T_keyword' and currenttoken.value=='for':
        getnext()
    else:
        print "missing word for at line ",currenttoken.line
    if currenttoken.type=='T_semicolon' and currenttoken.value==';':
        getnext()
    else:
        print "missing semicolon at line ",currenttoken.line

  

def expression():
    register=[]
    global i
    global marker
    global ifmark
    global forloop
    global remaining # the already calculated number
    global loadparameter
    global count
    marker=0
    while currenttoken.type!='T_semicolon':
        if currenttoken.type=='T_keyword' and currenttoken.value=='not':
            getnext()
            register.append(~expression())  
            if((type(register[0]) is int) and register[0] in [0,1]):
                fwrite.write("\nR[%s].i=~R[%s].i;"%(i,i))      
            elif(type(register[0]) is bool):
                fwrite.write("\nR[%s].i=~R[%s].b;"%(i,i))    
            else:
                print "type error at line ",currenttoken.line                
            continue
        if currenttoken.type=='T_rparen' and currenttoken.value==')':
            return register[0]
        elif currenttoken.type=='T_rbracket' and currenttoken.value==']':
            return register[0]
        register.append(arithop())
        if currenttoken.type=='T_operator' and currenttoken.value=='&':
            getnext()
            i+=1
            register.append(expression())
            i-=1
            register[0]=register[0] & register[1]
            if((type(register[0]) is int) and register[0] in [0,1]) and ((type(register[1]) is int) and register[1] in [0,1]):
                fwrite.write("\nR[%s].i=R[%s].i&R[%s].i;"%(i,i,i+1))  
            elif ((type(register[0]) is int) and register[0] in [0,1]) and (type(register[1]) is bool):
                fwrite.write("\nR[%s].i=R[%s].i&R[%s].b;"%(i,i,i+1))     
            elif(type(register[0]) is bool) and (type(register[1]) is bool):
                fwrite.write("\nR[%s].i=R[%s].b&R[%s].b;"%(i,i,i+1))  
            elif(type(register[0]) is bool) and ((type(register[1]) is int) and register[1] in [0,1]):
                fwrite.write("\nR[%s].i=R[%s].b&R[%s].i;"%(i,i,i+1))       
            else:
                print "type error at line ",currenttoken.line                                            
        elif currenttoken.type=='T_operator' and currenttoken.value=='|':
            getnext()
            i+=1
            register.append(expression())
            i-=1
            register[0]=register[1] | register[0]
            if((type(register[0]) is int) and register[0] in [0,1]) and ((type(register[1]) is int) and register[1] in [0,1]):
                fwrite.write("\nR[%s].i=R[%s].i|R[%s].i;"%(i,i,i+1))  
            elif ((type(register[0]) is int) and register[0] in [0,1]) and (type(register[1]) is bool):
                fwrite.write("\nR[%s].i=R[%s].i|R[%s].b;"%(i,i,i+1))     
            elif(type(register[0]) is bool) and (type(register[1]) is bool):
                fwrite.write("\nR[%s].i=R[%s].b|R[%s].b;"%(i,i,i+1))  
            elif(type(register[0]) is bool) and ((type(register[1]) is int) and register[1] in [0,1]):
                fwrite.write("\nR[%s].i=R[%s].b|R[%s].i;"%(i,i,i+1))       
            else:
                print "type error at line ",currenttoken.line 
        elif loadparameter==1:
            break #if it's loading parameter then it should break out of the loop
        else:
            register[0]=register[register.__len__()-1]
            marker=1
            remaining=register[0]
        if ifmark==1:
            return register[0]
    return register[0]

def returnstatement():
    global procedurename
    global symboltable
    global stack
    global returnstack
    if currenttoken.type=='T_keyword' and currenttoken.value=='return':
        stack=1000 #reinitiate the value of stack
        for i in range(0,symboltable[procedurename].parameter_out):
            fwrite.write("\nMM[MM[%s].i].i=MM[%s].i;"%(returnstack+i,stack+symboltable[procedurename].parameter_in+i))#assign the value from stack to the address of var
        fwrite.write("\ngoto procedurelabel;")
        getnext()
        if currenttoken.type=='T_semicolon' and currenttoken.value==';':
            getnext()
        else:
            print "missing semicolon at line ",currenttoken.line-1


def arithop():
    global i
    global count
    register=[]
    register.append(relation())
    if currenttoken.type=='T_operator' and currenttoken.value=='+':
        getnext()
        i+=1
        register.append(relation())
        i-=1
        register[0]+=register[1]
        if (type(register[0]) is int) and (type(register[1]) is int):
            fwrite.write("\nR[%s].i=R[%s].i+R[%s].i;"%(i,i,i+1))
        elif (type(register[0]) is float) and (type(register[1]) is float):
            fwrite.write("\nR[%s].f=R[%s].f+R[%s].f;"%(i,i,i+1))   
        elif (type(register[0]) is float) and (type(register[1]) is int):
            fwrite.write("\nR[%s].f=R[%s].f+R[%s].i;"%(i,i,i+1))  
        elif (type(register[0]) is int) and (type(register[1] is float)):
            fwrite.write("\nR[%s].f=R[%s].i+R[%s].f;"%(i,i,i+1))    
        else:
            print "type error at line ",currenttoken.line
    elif currenttoken.type=='T_operator' and currenttoken.value=='-':
        getnext()
        i+=1
        register.append(relation())
        i-=1
        register[0]-=register[1]
        if (type(register[0]) is int) and (type(register[1]) is int):
            fwrite.write("\nR[%s].i=R[%s].i-R[%s].i;"%(i,i,i+1))
        elif (type(register[0]) is float) and (type(register[1]) is float):
            fwrite.write("\nR[%s].f=R[%s].f-R[%s].f;"%(i,i,i+1))   
        elif (type(register[0]) is float) and (type(register[1]) is int):
            fwrite.write("\nR[%s].f=R[%s].f-R[%s].i;"%(i,i,i+1))  
        elif (type(register[0]) is int) and (type(register[1] is float)):
            fwrite.write("\nR[%s].f=R[%s].i-R[%s].f;"%(i,i,i+1)) 
        else:
            print "type error at line ",currenttoken.line 
    return register[0]



def relation():
    global i
    register=[]
    register.append(term())
    if currenttoken.type=='T_operator' and currenttoken.value=='<':
        getnext()
        i+=1   
        register.append(relation())
        i-=1
        if forloop==0:
            if(type(register[0]) is int)  and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].i<R[%s].i;"%(i,i,i+1))
            elif(type(register[0]) is float) and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].f<R[%s].i;"%(i,i,i+1)) 
            elif(type(register[0]) is int) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].i<R[%s].f;"%(i,i,i+1))     
            elif(type(register[0]) is float) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].f<R[%s].f;"%(i,i,i+1))    
            else:
                print "type error at line ",currenttoken.line                                 
        elif forloop==1:
            if(type(register[0]) is int)  and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].i<R[%s].i;"%(i+2,i,i+1))
            elif(type(register[0]) is float) and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].f<R[%s].i;"%(i+2,i,i+1)) 
            elif(type(register[0]) is int) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].i<R[%s].f;"%(i+2,i,i+1))     
            elif(type(register[0]) is float) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].f<R[%s].f;"%(i+2,i,i+1))    
            else:
                print "type error at line ",currenttoken.line 
        if register[0]<register[1]:
            return 1
        else:
            return 0
    elif currenttoken.type=='T_operator' and currenttoken.value=='>=':
        getnext()
        i+=1
        register.append(relation())
        i-=1
        if forloop==0:
            if(type(register[0]) is int)  and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].i>=R[%s].i;"%(i,i,i+1))
            elif(type(register[0]) is float) and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].f>=R[%s].i;"%(i,i,i+1)) 
            elif(type(register[0]) is int) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].i>=R[%s].f;"%(i,i,i+1))     
            elif(type(register[0]) is float) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].f>=R[%s].f;"%(i,i,i+1))    
            else:
                print "type error at line ",currenttoken.line 
        elif forloop==1:
            if(type(register[0]) is int)  and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].i>=R[%s].i;"%(i+2,i,i+1))
            elif(type(register[0]) is float) and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].f>=R[%s].i;"%(i+2,i,i+1)) 
            elif(type(register[0]) is int) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].i>=R[%s].f;"%(i+2,i,i+1))     
            elif(type(register[0]) is float) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].f>=R[%s].f;"%(i+2,i,i+1))    
            else:
                print "type error at line ",currenttoken.line 
        if register[0]>=register[1]:
            return 1
        else:
            return 0
    elif currenttoken.type=='T_operator' and currenttoken.value=='<=':
        getnext()
        i+=1
        register.append(relation())
        i-=1
        if forloop==0:
            if(type(register[0]) is int)  and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].i<=R[%s].i;"%(i,i,i+1))
            elif(type(register[0]) is float) and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].f<=R[%s].i;"%(i,i,i+1)) 
            elif(type(register[0]) is int) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].i<=R[%s].f;"%(i,i,i+1))     
            elif(type(register[0]) is float) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].f<=R[%s].f;"%(i,i,i+1))    
            else:
                print "type error at line ",currenttoken.line 
        elif forloop==1:
            if(type(register[0]) is int)  and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].i<=R[%s].i;"%(i+2,i,i+1))
            elif(type(register[0]) is float) and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].f<=R[%s].i;"%(i+2,i,i+1)) 
            elif(type(register[0]) is int) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].i<=R[%s].f;"%(i+2,i,i+1))     
            elif(type(register[0]) is float) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].f<=R[%s].f;"%(i+2,i,i+1))    
            else:
                print "type error at line ",currenttoken.line 
        if register[0]<=register[1]:
            return 1
        else:
            return 0
    elif currenttoken.type=='T_operator' and currenttoken.value=='>':
        getnext()
        i+=1
        register.append(relation())
        i-=1
        if forloop==0:
            if(type(register[0]) is int)  and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].i>R[%s].i;"%(i,i,i+1))
            elif(type(register[0]) is float) and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].f>R[%s].i;"%(i,i,i+1)) 
            elif(type(register[0]) is int) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].i>R[%s].f;"%(i,i,i+1))     
            elif(type(register[0]) is float) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].f>R[%s].f;"%(i,i,i+1))    
            else:
                print "type error at line ",currenttoken.line 
        elif forloop==1:
            if(type(register[0]) is int)  and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].i>R[%s].i;"%(i+2,i,i+1))
            elif(type(register[0]) is float) and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].f>R[%s].i;"%(i+2,i,i+1)) 
            elif(type(register[0]) is int) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].i>R[%s].f;"%(i+2,i,i+1))     
            elif(type(register[0]) is float) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].f>R[%s].f;"%(i+2,i,i+1))    
            else:
                print "type error at line ",currenttoken.line
        if register[0]>register[1]:
            return 1
        else:
            return 0
    elif currenttoken.type=='T_operator' and currenttoken.value=='==':
        getnext()
        i+=1
        register.append(relation())
        i-=1
        if forloop==0:
            if(type(register[0]) is int)  and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].i==R[%s].i;"%(i,i,i+1))
            elif(type(register[0]) is float) and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].f==R[%s].i;"%(i,i,i+1)) 
            elif(type(register[0]) is int) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].i==R[%s].f;"%(i,i,i+1))     
            elif(type(register[0]) is float) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].f==R[%s].f;"%(i,i,i+1))    
            else:
                print "type error at line ",currenttoken.line 
        elif forloop==1:
            if(type(register[0]) is int)  and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].i==R[%s].i;"%(i+2,i,i+1))
            elif(type(register[0]) is float) and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].f==R[%s].i;"%(i+2,i,i+1)) 
            elif(type(register[0]) is int) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].i==R[%s].f;"%(i+2,i,i+1))     
            elif(type(register[0]) is float) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].f==R[%s].f;"%(i+2,i,i+1))    
            else:
                print "type error at line ",currenttoken.line
        if register[0]==register[1]:
            return 1
        else:
            return 0
    elif currenttoken.type=='T_operator' and currenttoken.value=='!=':
        getnext()
        i+=1
        register.append(relation())
        i-=1
        if forloop==0:
            if(type(register[0]) is int)  and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].i!=R[%s].i;"%(i,i,i+1))
            elif(type(register[0]) is float) and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].f!=R[%s].i;"%(i,i,i+1)) 
            elif(type(register[0]) is int) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].i!=R[%s].f;"%(i,i,i+1))     
            elif(type(register[0]) is float) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].f!=R[%s].f;"%(i,i,i+1))    
            else:
                print "type error at line ",currenttoken.line 
        elif forloop==1:
            if(type(register[0]) is int)  and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].i==R[%s].i;"%(i+2,i,i+1))
            elif(type(register[0]) is float) and (type(register[1]) is int):
                fwrite.write("\nR[%s].i=R[%s].f==R[%s].i;"%(i+2,i,i+1)) 
            elif(type(register[0]) is int) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].i==R[%s].f;"%(i+2,i,i+1))     
            elif(type(register[0]) is float) and (type(register[1]) is float):
                fwrite.write("\nR[%s].i=R[%s].f==R[%s].f;"%(i+2,i,i+1))    
            else:
                print "type error at line ",currenttoken.line
        if register[1]!=register[0]:
            return 1
        else:
            return 0
    else:
        return register[0]



def term():
    global MM
    global symboltable
    global i
    register=[]
    register.append(factor())
    if currenttoken.type=='T_operator' and currenttoken.value=='*':
        getnext()
        i+=1
        register.append(term())
        i-=1
        if (type(register[0]) is int) and (type(register[1]) is int):
            fwrite.write("\nR[%s].i=R[%s].i*R[%s].i;"%(i,i,i+1))
        elif (type(register[0]) is float) and (type(regsiter[1]) is float):
            fwrite.write("\nR[%s].f=R[%s].f*R[%s].f;"%(i,i,i+1))   
        elif (type(register[0]) is float) and (type(register[1]) is int):
            fwrite.write("\nR[%s].f=R[%s].f*R[%s].i;"%(i,i,i+1))  
        elif (type(register[0]) is int) and (type(register[1] is float)):
            fwrite.write("\nR[%s].f=R[%s].i*R[%s].f;"%(i,i,i+1))    
        else:
            print "type error at line ",currenttoken.line
    elif currenttoken.type=='T_operator' and currenttoken.value=='/':
        getnext()
        i+=1
        register.append(term())
        i-=1
        if (type(register[0]) is int) and (type(register[1]) is int):
            fwrite.write("\nR[%s].i=R[%s].i/R[%s].i;"%(i,i,i+1))
        elif (type(register[0]) is float) and (type(regsiter[1]) is float):
            fwrite.write("\nR[%s].f=R[%s].f/R[%s].f;"%(i,i,i+1))   
        elif (type(register[0]) is float) and (type(register[1]) is int):
            fwrite.write("\nR[%s].f=R[%s].f/R[%s].i;"%(i,i,i+1))  
        elif (type(register[0]) is int) and (type(register[1] is float)):
            fwrite.write("\nR[%s].f=R[%s].i/R[%s].f;"%(i,i,i+1))    
        else:
            print "type error at line ",currenttoken.line
    return register[0]


def factor():
    global marker
    register=[]
    global MM
    global symboltable
    global j
    global remaining
    global loadparameter
    global parameternumber
    global parameterstack
    global i
    global procedurecall
    global proceduredec
    global stack
    count=0
    variablename=''#used to store the name of the variable
    array=0 #used to store the index of thearray
    if marker==1:
        marker=0
        return remaining
    if currenttoken.type=='T_lparen' and currenttoken.value=='(':
        getnext()
        register.append(expression())
        if currenttoken.type=='T_rparen' and currenttoken.value==')':
            getnext()
            marker=0
            return register[0]
        else:
            reporterror()
            lineno()                
    elif currenttoken.type=='T_operator' and currenttoken.value=='-':
        getnext()
        if currenttoken.type=='T_decimalnumber':
            register.append(0-int(currenttoken.value))
            fwrite.write("\nR[%s].i=-%s;"%(i,currenttoken.value))         
            getnext()
            return register[0]
        elif currenttoken.type=='T_floatnumber':
            register.append(0-float(currenttoken.value))
            fwrite.write("\nR[%s].f=-%s;"%(i,currenttoken.value))         
            getnext()
            return register[0]            
        elif currenttoken.type=='T_identifier' and (currenttoken.value in symboltable.keys()) and procedurecall==0:
            j=j%2
            variablename=currenttoken.value
            getnext()  
            if currenttoken.type=='T_lbracket' and currenttoken.value=='[':#the value of a  arrays
                getnext()
                array=int (expression())
                if symboltable[variablename]!=None and symboltable[variablename].arraysize>array:#index within range
                    pass
                else:#index out of range
                    array=0
                    reporterror()
                    lineno()
                if currenttoken.value==']':
                    getnext()
                elif currenttoken.value!=']':
                    reporterror()
                    lineno()
            if(symboltable[variablename].array_check==0):
                if(symboltable[variablename].format=='integer'):
                    fwrite.write("\nR[%s].i=-MM[%s].i;"%(i,symboltable[variablename].address+array))
                elif (symboltable[variablename].format=='float'):
                    fwrite.write("\nR[%s].f=-MM[%s].f;"%(i,symboltable[variablename].address+array))  
                else:
                    print "type error at line ",currenttoken.line   
            elif (symboltable[variablename].array_check==1):  
                if(symboltable[variablename].format=='integer'):
                    fwrite.write("\nR[%s].i=-MM[%s].i;"%(i,i))
                elif (symboltable[variablename].format=='float'):
                    fwrite.write("\nR[%s].f=-MM[%s].f;"%(i,i))  
                else:
                    print "type error at line ",currenttoken.line  
                marker=0
            register.append(0-MM[symboltable[variablename].address+array])
            j+=1
            array=0#reinitiate array
            return register[0]
        elif currenttoken.type=='T_identifier' and (currenttoken.value in symboltablelocal.keys()) and procedurecall==1:
            j=j%2
            variablename=currenttoken.value
            getnext() 
            if currenttoken.type=='T_lbracket' and currenttoken.value=='[':#the value of a  arrays
                getnext()
                array=int (expression())
                if symboltable[variablename]!=None and symboltablelocal[variablename].arraysize>array:#index within range
                    pass
                else:#index out of range
                    array=0
                    reporterror()
                    lineno()
                if currenttoken.value==']':
                    getnext()
                elif currenttoken.value!=']':
                    reporterror()
                    lineno()
            if(symboltablelocal[variablename].array_check==0):
                if(symboltablelocal[variablename].format=='integer'):
                    fwrite.write("\nR[%s].i=-MM[%s].i;"%(i,symboltablelocal[variablename].address+array))
                elif (symboltablelocal[variablename].format=='float'):
                    fwrite.write("\nR[%s].f=-MM[%s].f;"%(i,symboltablelocal[variablename].address+array))  
                else:
                    print "type error at line ",currenttoken.line  
            elif (symboltablelocal[variablename].array_check==1):  
                if(symboltablelocal[variablename].format=='integer'):
                    fwrite.write("\nR[%s].i=-MM[%s].i;"%(i,i))
                elif (symboltablelocal[variablename].format=='float'):
                    fwrite.write("\nR[%s].f=-MM[%s].f;"%(i,i))  
                else:
                    print "type error at line ",currenttoken.line  
                marker=0
            if proceduredec==1:
                register.append(0-MM[symboltablelocal[variablename].address+array])
            j+=1
            array=0#reinitiate array
            if proceduredec==0:
                return 0   
            return register[0]
        elif currenttoken.type=='T_identifier' and (currenttoken.value in symboltable.keys()) and procedurecall==1:
            j=j%2
            variablename=currenttoken.value
            getnext() 
            if currenttoken.type=='T_lbracket' and currenttoken.value=='[':#the value of a  arrays
                getnext()
                array=int (expression())
                if symboltable[variablename]!=None and symboltable[variablename].arraysize>array:#index within range
                    pass
                else:#index out of range
                    array=0
                    reporterror()
                    lineno()
                if currenttoken.value==']':
                    getnext()
                elif currenttoken.value!=']':
                    reporterror()
                    lineno()
            if(symboltable[variablename].array_check==0):
                if(symboltable[variablename].format=='integer'):
                    fwrite.write("\nR[%s].i=-MM[%s].i;"%(i,symboltable[variablename].address+array))
                elif (symboltable[variablename].format=='float'):
                    fwrite.write("\nR[%s].f=-MM[%s].f;"%(i,symboltable[variablename].address+array))  
                else:
                    print "type error at line ",currenttoken.line   
            elif (symboltable[variablename].array_check==1):  
                if(symboltable[variablename].format=='integer'):
                    fwrite.write("\nR[%s].i=-MM[%s].i;"%(i,i))
                elif (symboltable[variablename].format=='float'):
                    fwrite.write("\nR[%s].f=-MM[%s].f;"%(i,i))  
                else:
                    print "type error at line ",currenttoken.line  
                marker=0 
            if proceduredec==1:
                register.append(0-MM[symboltable[variablename].address+array])
            j+=1
            array=0#reinitiate a array
            if proceduredec==0:
                return 0      
            return register[0]             
    elif currenttoken.type=='T_decimalnumber': #this line is right
        print "currenttoke"
        print currenttoken.value
        register.append(int(currenttoken.value))
        fwrite.write("\nR[%s].i=%s;"%(i,currenttoken.value)) 
        getnext()
        return register[0]
    elif currenttoken.type=='T_floatnumber':
        register.append(float(currenttoken.value))
        fwrite.write("\nR[%s].f=%s;"%(i,currenttoken.value))
        getnext()
        return register[0]
    elif currenttoken.type=='T_identifier' and (currenttoken.value in symboltable.keys()) and procedurecall==0:
        j=j%2
        variablename=currenttoken.value
        getnext()  
        if currenttoken.type=='T_lbracket' and currenttoken.value=='[':#the value of a  arrays
            getnext()
            array=int (expression())
            if symboltable[variablename]!=None and symboltable[variablename].arraysize>array:#index within range
                pass
            else:#index out of range
                array=0
                reporterror()
                lineno()
            if currenttoken.value==']':
                getnext()
            elif currenttoken.value!=']':
                reporterror()
                lineno()
        if(symboltable[variablename].array_check==0):
            if(symboltable[variablename].format=='integer'):
                fwrite.write("\nR[%s].i=MM[%s].i;"%(i,symboltable[variablename].address+array))
            elif (symboltable[variablename].format=='float'):
                fwrite.write("\nR[%s].f=MM[%s].f;"%(i,symboltable[variablename].address+array)) 
            elif (symboltable[variablename].format=='char'): 
                fwrite.write("\nR[%s].c=MM[%s].c;"%(i,symboltable[variablename].address+array)) 
            else:
                print "type error at line ",currenttoken.line 
        elif(symboltable[variablename].array_check==1):
            if(symboltable[variablename].format=='integer'):
                fwrite.write("\nR[%s].i=MM[R[%s].i].i;"%(i,i))
            elif (symboltable[variablename].format=='float'):
                fwrite.write("\nR[%s].f=MM[R[%s].i].f;"%(i,i)) 
            elif (symboltable[variablename].format=='char'): 
                fwrite.write("\nR[%s].c=MM[R[%s].i].c;"%(i,i)) 
            else:
                print "type error at line ",currenttoken.line   
            marker=0  
        print "proceduredec"
        print proceduredec
        if proceduredec==1:     
            register.append(MM[symboltable[variablename].address+array])
        else:
            return 0
        j+=1
        array=0#reinitiate array
        return register[0]
    elif currenttoken.type=='T_identifier' and (currenttoken.value in symboltablelocal.keys()) and procedurecall==1:
        j=j%2
        variablename=currenttoken.value
        getnext() 
        if currenttoken.type=='T_lbracket' and currenttoken.value=='[':#the value of a  arrays
            getnext()
            array=int (expression())
            print currenttoken.value
            print "currenttoken"
            if symboltablelocal[variablename]!=None and symboltablelocal[variablename].arraysize>array:#index within range
                pass
            else:#index out of range
                array=0
                reporterror()
                lineno()
            if currenttoken.value==']':
                getnext()
            else:
                print "missing right bracket at line ",currenttoken.line
        if(symboltablelocal[variablename].array_check==0):
            if(symboltablelocal[variablename].format=='integer'):
                fwrite.write("\nR[%s].i=MM[%s].i;"%(i,symboltablelocal[variablename].address+array))
            elif (symboltablelocal[variablename].format=='float'):
                fwrite.write("\nR[%s].f=MM[%s].f;"%(i,symboltablelocal[variablename].address+array)) 
            elif (symboltablelocal[variablename].format=='char'): 
                fwrite.write("\nR[%s].c=MM[%s].c;"%(i,symboltablelocal[variablename].address+array)) 
            else:
                print "type error at line ",currenttoken.line
        elif (symboltablelocal[variablename].array_check==1):
            if(symboltablelocal[variablename].format=='integer'):
                fwrite.write("\nR[%s].i=MM[R[%s].i].i;"%(i,i))
            elif (symboltablelocal[variablename].format=='float'):
                fwrite.write("\nR[%s].f=MM[R[%s].i].f;"%(i,i)) 
            elif (symboltablelocal[variablename].format=='char'): 
                fwrite.write("\nR[%s].c=MM[R[%s].i].c;"%(i,i)) 
            else:
                print "type error at line ",currenttoken.line    
            marker=0        
        if proceduredec==1:
            register.append(MM[symboltablelocal[variablename].address+array])
        j+=1
        array=0#reinitiate array
        if proceduredec==0:
            return 0   
        return register[0]
    elif currenttoken.type=='T_identifier' and (currenttoken.value in symboltable.keys()) and procedurecall==1:
        j=j%2
        variablename=currenttoken.value
        getnext() 
        if currenttoken.type=='T_lbracket' and currenttoken.value=='[':#the value of a  arrays
            getnext()
            array=int (expression())
            if symboltable[variablename]!=None and symboltable[variablename].arraysize>array:#index within range
                pass
            else:#index out of range
                array=0
                reporterror()
                lineno()
            if currenttoken.value==']':
                getnext()
            elif currenttoken.value!=']':
                reporterror()
                lineno()
        if(symboltable[variablename].array_check==0):
            if(symboltable[variablename].format=='integer'):
                fwrite.write("\nR[%s].i=MM[%s].i;"%(i,symboltable[variablename].address+array))
            elif (symboltable[variablename].format=='float'):
                fwrite.write("\nR[%s].f=MM[%s].f;"%(i,symboltable[variablename].address+array)) 
            elif (symboltable[variablename].format=='char'): 
                fwrite.write("\nR[%s].c=MM[%s].c;"%(i,symboltable[variablename].address+array)) 
            else:
                print "type error at line ",currenttoken.line
        elif(symboltable[variablename].array_check==1):
            if(symboltable[variablename].format=='integer'):
                fwrite.write("\nR[%s].i=MM[R[%s].i].i;"%(i,i))
            elif (symboltable[variablename].format=='float'):
                fwrite.write("\nR[%s].f=MM[R[%s].i].f;"%(i,i)) 
            elif (symboltable[variablename].format=='char'): 
                fwrite.write("\nR[%s].c=MM[R[%s].i].c;"%(i,i)) 
            else:
                print "type error at line ",currenttoken.line
            marker=0
        if proceduredec==1:
            register.append(MM[symboltable[variablename].address+array])
        j+=1
        array=0#reinitiate a array
        if proceduredec==0:
            return 0      
        return register[0] 
    elif currenttoken.type=='T_string':
        register[0]=currenttoken.value
        getnext()
    elif currenttoken.type=='T_keyword' and currenttoken.value=='true':
        register.append(True)
        fwrite.write("\nR[%s].b=true;"%i)
        getnext()
    elif currenttoken.type=='T_keyword' and currenttoken.value=='false':
        register.append(False)
        fwrite.write("\nR[%s].b=false;"%i)
        getnext()
    else:
        print "couldn't detect the type of variable at line ",currenttoken.line
        print currenttoken.value
        return None
    return register[0]

def name():
    register=[]
    if currenttoken.type=='T_identifier':
        fwrite
        if currenttoken.value in typecheck.keys():
            getnext()
            if currenttoken.type=='T_lbracket' and currenttoken.value=='[':
                getnext()
                register[0]=expression()
                getnext()
                if currenttoken.type=='T_rbracket' and currenttoken.value==']':
                    getnext()
                else:
                    reporterror()
                    lineno()
        else:
            reporterror()
            lineno()
    else:
        reporterror()
        lineno()


def argumentlist():
    global procedurecall
    global loadparameter#to flag to expression the value shoule be loaded from parameter stack to stack
    global parameternumber
    global marker
    global parameterin
    global parameterout
    global returnstack
    global procedurelabel
    register=[]
    marker=0
    loadparameter=1
    procedurecall=1#mark this is in a procedure
    if parameternumber<(parameterin):#if the in parameter is smaller than the defined input, if it;s larger than that then it's output
        register.append(expression())
        fwrite.write("\nMM[%s].i=R[0].i;"%(parameterstack+parameternumber))
        fwrite.write("\nMM[%s].i=MM[%s].i;"%(stack+parameternumber,parameterstack+parameternumber))
        if currenttoken.type=='T_comma' and currenttoken.value==',':
            getnext()
            parameternumber+=1
            argumentlist()
        if parameternumber==(parameterin-1):
            fwrite.write("\nMM[%s].i=(int)&&procedure_ptr%s;"%(stack+parameterin+parameterout,procedurelabel))        
    elif parameternumber<parameterin+parameterout:#if the parameter is now for output
        fwrite.write("\nMM[%s].i=%s;"%(returnstack+parameternumber-parameterin,symboltable[currenttoken.value].address))#put the address of the return variable onto the return stack
        getnext()
        if currenttoken.type=='T_comma' and currenttoken.value==',':
            getnext()
            parameternumber+=1
            argumentlist()
    parameternumber=0
    parameterin=0#all the input parameter has been loaded
    procedurecall=0#end of the procedure call
    

n=0
i=0
j=0
skip=0
pointer=0
ifmark=0
linenumber=0
label=0
forloop=0
procedurecall=0
marker=0
parameternumber=0
stack=1000
pointerlocal=0
recursion=0
parameterstack=900#starting point to store the input parameter
returnstack=950#the starting point of the stack to store the address of return value
procedureaddress=0
loadparameter=0
parameterin=0
parameterout=0
count=0
parameterdec=0
procedurename=''
proceduredec=0#to tell if the if it's procedure declaration(0) or initilization(1)
procedurelabel=0 #used for when procedure wants to go to the procedure call
inlocal=0#check if the variable assigned in function is in local table or general table
procedurelabel1=0
variablename=''#store the name of the variable in case it's a array
array=0#the position of a variable in a array
MM={}
symboltable={}
symboltablelocal={}
symboltableglobal={}
address={}
typecheck={}
currenttokenqueue=[]
fwrite=open('parserout.c','w')
program()


