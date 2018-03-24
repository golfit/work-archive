# Useful utilities when reading files

try:
    import re
    from numpy import size
except:
    print "Regular expression module 're' not available"
    raise

def file_tokens(fp):
    """ A generator to split a file into tokens
    """
    toklist = []
    while True:
        line = fp.readline()
        if not line: break
        toklist = line.split()
        for tok in toklist:
            yield tok

def file_numbers(fp):
    """Generator to get numbers from a text file"""
    toklist = []
    while True:
        line = fp.readline()
        if not line: break
        # Match numbers in the line using regular expression
        pattern = r'[+-]?\d*[\.]?\d+(?:[Ee][+-]?\d+)?'
        toklist = re.findall(pattern, line)
        for tok in toklist:
            yield tok

def writef(fp, val,item=0,depth=0):
    """ Write values to a file in Fortran style
    
    """
    
    if size(val) == 1:
        fp.write("%16.9E" % val)
        item+=1 #Increment item
        if (item) % 5 == 0 and item>0 :
            fp.write("\n") #New line when 5 data points are reached.
    else :
        for v in val :
            item=writef(fp,v,item,depth+1) #Make recursive
        #print('done with array, item='+str(item)+', depth='+str(depth))
        if item % 5 != 0 and item>0 and depth==0:
            fp.write('\n') #New lines after arrays are done.
            item=0 #Reset item counter
            #print('resetting line')
    return item
