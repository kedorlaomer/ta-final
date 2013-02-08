#!/bin/bash
mkdir "crossval"
cd "crossval"
for i in {0..9}
do
    echo -n "."
    mkdir "train$i"
    cd "train$i"
    mkdir "ham"
    mkdir "spam"
    cd ".."
    mkdir "test$i"
    cd "test$i"
    mkdir "ham"
    mkdir "spam"
    cd ".."
done
cd ".."
echo ""
python "makeCrossvalFiles.py" "trainingham/" "trainingspam/" "crossval/"