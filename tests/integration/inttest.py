import subprocess


def test1():
    res = subprocess.run(["build/app.exe"], input="1 + 2", text=True, capture_output=True)
    assert res.returncode == 0
    assert int(res.stdout) == 3
    
def test2():
    res = subprocess.run(["build/app.exe"], input=" ((    11 + 3   * 3) + ( 4 - 1 \v  \t \r )/ 3\r)", text=True, capture_output=True)
    assert res.returncode == 0
    assert int(res.stdout) == 21
    
def test3():
    res = subprocess.run(["build/app.exe", "--float"], input="5 / 2", text=True, capture_output=True)
    assert res.returncode == 0
    assert float(res.stdout) == 2.5
