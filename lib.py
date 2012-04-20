"""
Libraries.

1. def sort
   # Sorting out only unique array elements.
2. def sort_ss
   # Sorting out unique slip systems..
   # for the give set of slip normal and slip direction
"""
def sort(given, iopp=True):
    """
    Arguments:
     given: an array having arrays as elements.
     iopp : True  -> include the opposite direction
            False -> exclude the opposite direction
    """
    import numpy as np

    sortedout = []
    sortedout.append(given[0])
    for i in range(len(given)):
        isUnique = True
        for j in range(len(sortedout)):
            if all(given[i]==sortedout[j]) or all(given[i]==-sortedout[j]):
            
                isUnique = False
        if isUnique:
            sortedout.append(given[i])

    ## if iopp is True, duplicate the above unique set
    ## by multiplying -1
    if iopp==True:
        master = []
        for i in range(len(sortedout)):
            master.append(map(int,sortedout[i]))
            master.append(map(int,-sortedout[i]))
        sortedout = master[::]

    return np.array(sortedout)

def isthisvectorin(a, b, iopptell=False):
    """
    is a vector in b?
    arugment: 
      a   : a vector
      b   : a list of vectors
      iopptell : Bool
         True:  tell the opposite vector apart
              [1,1,1] != [-1,-1,-1]
         False: Opposite vector is the same.
              [1,1,1] =  [-1,-1,-1]
    """
    import numpy as np
    a = np.array(a)
    b = np.array(b)
    for i in b:
        if iopptell==False:
            if all(a==i) or all(a==-i): return True
        elif iopptell==True:
            if all(a==i): return True
        else: pass
    return False

def isthisvectornotin(a, b, iopptell=False):
    """
    is a vector in not b?
    arugment: 
      a   : a vector
      b   : a list of vectors
      iopptell : Bool
         True:  tell the opposite vector apart
              [1,1,1] != [-1,-1,-1]
         False: Opposite vector is the same.
              [1,1,1] =  [-1,-1,-1]
    """
    return not(isthisvectorin(a,b, iopptell))


def sort_ss(sn, sb):
    """
    Applicable only to cubic structure yet.

    find unique slip system set..
    # method:
      slip plane normal and slip system should be
      all unique at the same time.

    -- arguments
    sn : slip plane normals
    sb : slip system directions
    """
    import numpy as np
    mastersn = [sn[0]]
    mastersb = [sb[0]]
    master   = [[sn[0], sb[0]]]
    skip_indices = []

    ## find the first unique memeber
    for j in range(len(sb)):
        if is_orthogonal(sn[0], sb[j]):
            mastersn = [sn[0]]
            mastersb = [sb[j]]
            master   = [[sn[0], sb[j]]]
            break
    ##

    for i in range(len(sn)):
        for j in range(len(sb)):

            # condition1: orthogonal?
            if is_orthogonal(sn[i], sb[j]):
                iunique = True
                for k in range(len(master)):
                    if all(sn[i]==master[k][0]) and all(sb[j]==master[k][1]) or \
                            all(sn[i]==master[k][0]) and all(sb[j]==-np.array(master[k][1])):
                        iunique = False
                        break

                if iunique:
                    master.append([map(int, sn[i]),
                                   map(int, sb[j])])

                    mastersn.append(map(int,sn[i]))
                    mastersb.append(map(int,sb[j]))

            else: pass

    return np.array(master)

def is_orthogonal(a,b):
    """
    a and b vectors are mutually orthogonal?
    """
    import numpy as np
    if np.dot(a, b)==0:
        return True
    elif 0 < abs(np.dot(a, b)) < 0.0000001:
        print 'Warning!!! It is just very close to orthognal'
        return True
    else: return False
