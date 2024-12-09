import nox

@nox.session
def tests(session):
    session.install('pytest', 'pytest-cov', 'pytest-asyncio', '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple')
    session.install('-r', 'requirements.txt', '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple')
    session.install('-r', 'requirements_option.txt', '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple')
    session.run('pytest', '--cov=seatools', '--cov-report=html')


