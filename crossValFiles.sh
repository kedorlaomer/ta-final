mkdir "crossval"
cd "crossval"
for i in {0..9}
do
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
python "crossvalidation.py" "trainingham/" "trainingspam/" "crossval/"