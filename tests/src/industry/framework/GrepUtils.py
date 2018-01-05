import re, os
from pysys import log
from pysys.exceptions import FileNotFoundException

class OrderedGrepResults:
    def init(self):
        self.failureExpr = None
        self.groupValues = {}

def orderedgrep(file, exprList, groupValues = None):
    """Seach for ordered matches to a set of regular expressions in an input file, returning true if the matches occur in the correct order.
    
    The ordered grep method will only return true if matches to the set of regular expression in the expression 
    list occur in the input file in the order they appear in the expression list. Matches to the regular expressions 
    do not have to be across sequential lines in the input file, only in the correct order. For example, for a file 
    with contents ::
      
        A is for apple 
        B is for book
        C is for cat
        D is for dog
    
    an expression list of ["^A.*$", "^C.*$", "^D.*$"] will return true, whilst an expression list of 
    ["^A.*$", "^C.$", "^B.$"] will return false.
    
    @param file: The full path to the input file
    @param exprList: A list of regular expressions (uncompiled) to search for in the input file
    @returns: success (True / False)
    @rtype: integer
    @raises FileNotFoundException: Raised if the input file does not exist
        
    """
    list = map(lambda x:(re.compile(x), x),exprList)
    list.reverse();
    result = OrderedGrepResults()
    item = list.pop()
    result.failureExpr = item[1]
    
    result.groupValues = groupValues
    if groupValues == None:
        result.groupValues = {}
    

    if not os.path.exists(file):
        raise FileNotFoundException, "unable to find file %s" % (os.path.basename(file))
    else:
        contents = open(file, 'r').readlines()      
        for i in range(len(contents)):
            matched = item[0].search(r"%s"%contents[i])
            if matched != None:
                #check all groups match
                for group in matched.groupdict():
                    if result.groupValues.has_key(group):
                        if matched.group(group) != result.groupValues[group]:
                            log.error("Value of group (%s) has value \"%s\" should be \"%s\""%(group,matched.group(group),result.groupValues[group]))
                            return result
                    else:
                        result.groupValues[group] = matched.group(group)
                try:
                    item = list.pop()
                    result.failureExpr = item[1]
                except:
                    result.failureExpr = None
                    return result
    return result