import argparse,json,os,tempfile
from .core import analyze
from .verify import verify

def main():
    p=argparse.ArgumentParser(description='Finite ROBDD evidence, at most five Boolean variables')
    p.add_argument('path');p.add_argument('--verify',action='store_true');p.add_argument('--output');a=p.parse_args()
    try:
        with open(a.path,encoding='utf-8') as f:r=json.load(f)
        if a.verify:verify(r);text='verified compilelab/1\n'
        else:text=json.dumps(analyze(r),indent=2,ensure_ascii=False)+'\n'
        if a.output:
            directory=os.path.dirname(os.path.abspath(a.output))
            fd,name=tempfile.mkstemp(dir=directory)
            try:
                with os.fdopen(fd,'w',encoding='utf-8') as f:f.write(text)
                os.replace(name,a.output)
            finally:
                if os.path.exists(name):os.unlink(name)
        else:print(text,end='')
    except (OSError,ValueError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()
