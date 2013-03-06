import sys
import string 

kinds = ['standard', 'extended', 'both']

def generate(namespace, n, kind):
    if not kind in kinds:
        raise Exception('Unknown kind')

    instances = ''
    if kind == 'shared':
        instances = generate_instances(n, True)
    elif kind == 'non_shared':
        instances = generate_instances(n, False)
    else:
        instances = generate_instances(n, True) + generate_instances(n, False)

    t = string.Template(open('ChainLocker.cs.t').read())
    
    s = t.substitute(Namespace=namespace, Instances=instances)

    return s

def generate_instances(n, extended):
    instances = [generate_instance(x, extended) for x in range(2, n+1)]
    return '\n\n'.join(instances)
        
def generate_instance(n, extended):
    """ """
    filename = 'ExtendedInstance.t' if extended else 'StandardInstance.t'
    t = string.Template(open(filename).read())
    stateTypeList = ', '.join(['T%d' % i for i in range(n)])
    classConstraints = '\n'.join(['        where T%d : class' % i for i in range(n)])
    funcs = generate_funcs(n-1, extended)
    stages = generate_stages(n-1, extended)
    s = t.substitute(dict(
            StateTypeList=stateTypeList,
            ClassConstraints=classConstraints,
            Funcs=funcs,
            Last=str(n-1),
            OneBeforeLast=str(n-2),
            Count=str(n),
            Stages=stages))
    return s

def generate_funcs(n, extended):
    funcs = [generate_func(x, extended) for x in range(n)]
    return ',\n'.join(funcs)

def generate_func(n, extended):
    #Func<T, T0, T1>  stage0,

    extendedState = 'T, ' if extended else ''
    t = '                       Func<{0}T{1}, T{2}>    stage{1}'
    return t.format(extendedState, n, n+1) 

def generate_stages(n, extended):
    stages = [generate_stage(x, extended) for x in range(1, n)]
    return '\n'.join(stages)

def generate_stage(index, extended):
    filename = 'ExtendedInstance.t' if extended else 'StandardInstance.t'
    t = string.Template(open('Stage.t').read())
    return t.substitute(
      dict(Prev=str(index-1),
           Index=str(index),
           Next=str(index+1),
           SharedState='_sharedState, ' if extended else ''))

def usage():
    print("""\
Usage: python ChainLockerGenerator.py <namespace> <N> [kind]

namespace - The C# namespace of your project
N - the maximal number of stages to generate
Kind - one of standard, extended, both

ChainLockerGenerator generates a C# file that contains multiple generic ChainLocker classes.
If you don't know what that is you have no business running this script :-)
There are two variants of chain lockers: standard and extended. The extended one provides
a shared state that is not locked to the stage operations.

Each generated instance has a certain number of stages that are locked. All instances 
from 2 to N will be generated. For example, if you specified N=4 then 3 instances will be
generated with 2, 3 and 4 stages.

If you specfied Kind=standard (or omitted it) only the standard instances will be generated.
If you specified Kind=extended only the extended instances will be generated.
If you specified both then you get both standard and extended. Everything is printed out
to standard output as a single C# module with the namespace you chosee. The standard instances
are named ChainLocker<T1,...,Tn>. The extended instances are named ChainLockerEx<T, T1,...,Tn>
""")
    sys.exit()

def main(argv):
    if not len(argv) in (2, 3):
        usage()

    N = int(argv[1])
    if N < 2:
        usage()

    kind = argv[2] if len(argv) == 3 else 'standard'
    if kind not in ('standard', 'extended', 'both'):
        usage()

    s = generate(argv[0], N, kind)
    print(s)
    return s

def test():
    """ """
    s = main(['XXX', 4, 'both'])
    open('XXX.cs', 'w').write(s)

if __name__ == '__main__':
    #main(sys.argv[1:])
    test()
    print('Done.')
          
