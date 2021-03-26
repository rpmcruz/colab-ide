import tempfile, subprocess, io

def compile(code):
    fp = tempfile.NamedTemporaryFile('w', suffix='.cpp')
    fp.write(code)
    fp.seek(0)
    proc = subprocess.run(['g++', '-Wall', fp.name], stderr=subprocess.PIPE)
    out = proc.stderr.decode('utf-8')
    if '.cpp' in out:
        out = out[out.rindex('.cpp')+5:]
    return proc.returncode, out

def test(stdin):
    try:
        p = subprocess.Popen(['./a.out'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p.stdin.write(stdin.encode())
        stdout = p.communicate(timeout=2)[0]
        return stdout.decode('utf-8')
    except Exception as ex:
        return str(ex)
