#!/usr/bin/env bash

OS=$(uname -s)

PIP='pip'
SETUPTOOLS='setuptools==34.3.3'
WHEEL='wheel==0.29.0'

if [ $OS = 'Linux' ]; then
    REL=$(lsb_release -sr)
    ARCH=$(uname -m)
    VENV_BIN='venv/bin'

    sudo add-apt-repository -yu ppa:jonathonf/python-3.6

    echo "Detected Ubuntu $REL $ARCH"
    echo "Installing runtime dependencies from apt"
    sudo apt-get -yqq update

    echo "Installing python36 packaging tools and venv from apt (pip, setuptools, wheel etc)"
    sudo apt-get install -yqq python3.6 python3.6-venv python3.6-dev

    echo "Creating venv/"
    python3.6 -m venv venv/ --clear

    echo "    Installing $PIP, $SETUPTOOLS, and $WHEEL into venv"
    $VENV_BIN/pip install --upgrade $PIP || exit 1
    $VENV_BIN/pip install --upgrade $SETUPTOOLS $WHEEL|| exit 1
else
    echo "Detected Windows"

    VENV_BIN='venv/Scripts'
    PY_VER='36'
    PYTHON_PATH="/c/Program Files/Python"$PY_VER

    echo "Creating venv/ using $PYTHON_PATH"
    "$PYTHON_PATH/python" -m venv venv/ --clear --copies

    echo "    Installing $PIP, $SETUPTOOLS, and $WHEEL into venv"
    $VENV_BIN/python -m pip install --upgrade $PIP $SETUPTOOLS $WHEEL || exit 1

    echo "    Installing pyopencl and numpy"
    # http://www.lfd.uci.edu/~gohlke/pythonlibs/tuoh5y4k/numpy-1.12.1+mkl-cp36-cp36m-win_amd64.whl
    $VENV_BIN/pip install deps/numpy-1.12.1+mkl-cp36-cp36m-win_amd64.whl

    #http://www.lfd.uci.edu/~gohlke/pythonlibs/tuoh5y4k/pyopencl-2016.2.1+cl21-cp36-cp36m-win_amd64.whl
    $VENV_BIN/pip install deps/pyopencl-2016.2.1+cl21-cp36-cp36m-win_amd64.whl

    cmd //c 'mklink /D venv\bin Scripts'
fi



