#!/bin/bash

rev=$(git rev-parse --short HEAD)
echo "Revision is $rev"

cd docs/cpp
echo "Building C++ Intro"
xelatex cpp-intro.tex
xelatex cpp-intro.tex
cd ../python
echo "Building Python Intro"
xelatex py-intro.tex
xelatex py-intro.tex
cd ../..

echo "Building Artifact" 
rm -rf build
mkdir build
cp docs/README_template.md build/README.md
cp judger.py build/
cd build

mkdir cpp-sdk-$rev
cp -R ../cpp/* cpp-sdk-$rev/
cp ../docs/cpp/cpp-intro.pdf cpp-sdk-$rev/README.pdf
rm -rf cpp-sdk-$rev/build
rm -rf cpp-sdk-$rev/Makefile

mkdir py-sdk-$rev
cp -R ../python/* py-sdk-$rev
cp ../docs/python/py-intro.pdf py-sdk-$rev/README.pdf
rm -rf py-sdk-$rev/aisdk/.DS_Store

cd cpp-sdk-$rev
zip -r cpp-sdk-$rev.zip ./*
mv cpp-sdk-$rev.zip ../
cd ../py-sdk-$rev
zip -r py-sdk-$rev.zip ./*
mv py-sdk-$rev.zip ../

cd ..
rm -rf cpp-sdk-$rev
rm -rf py-sdk-$rev

echo "Built successfully"
