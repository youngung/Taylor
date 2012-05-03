def main():
    import os

    # compiler gfortran's path in this system
    compiler_path = os.popen('which gfortran').readline().split('\n')[0]

    # shear_gamma.for for compile
    iflag = os.system(
        "f2py -c --f77flags='-Wall' -m gammadot gammadot.for"
        )
    # 

    
def ex():
    import os
    # compile the example f2py.for : exf2py.for

    compiler_path = os.popen('which gfortran').readline().split('\n')[0]
    iflag = os.system('f2py -c -m exf2py exf2py.for')
    
