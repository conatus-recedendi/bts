
../fasttext/fasttext skipgram -input dataset/data/train_default.txt -output model/sisg -dim 300 -epoch 5 -minCount 10 -minsc 3 -maxsc 0 -minjn 1 -maxjn 0 -minn 3 -maxn 0 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
../fasttext/fasttext skipgram -input dataset/data/train_default.txt -output model/sisg_ch -dim 300 -epoch 5 -minCount 10 -minsc 3 -maxsc 0 -minjn 1 -maxjn 0 -minn 1 -maxn 6 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
../fasttext/fasttext skipgram -input dataset/data/train_jamo.txt -output model/sisg_jm -dim 300 -epoch 5 -minCount 10 -minsc 3 -maxsc 0 -minjn 3 -maxjn 6 -minn 3 -maxn 0 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
../fasttext/fasttext skipgram -input dataset/data/train_jamo.txt -output model/sisg_ch4_jm -dim 300 -epoch 5 -minCount 10 -minsc 3 -maxsc 0 -minjn 3 -maxjn 6 -minn 4 -maxn 4 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
../fasttext/fasttext skipgram -input dataset/data/train_jamo.txt -output model/sisg_ch6_jm -dim 300 -epoch 5 -minCount 10 -minsc 3 -maxsc 0 -minjn 3 -maxjn 6 -minn 6 -maxn 6 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
../fasttext/fasttext skipgram -input dataset/data/train_stroke.txt -output model/sisg_stroke -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 0 -minn 0 -maxn 0 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
../fasttext/fasttext skipgram -input dataset/data/train_cji.txt -output model/sisg_cji -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 0 -minn 0 -maxn 0 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
../fasttext/fasttext skipgram -input dataset/data/train_bts.txt -output model/sisg_bts -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 6 -minn 6 -maxn 6 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
# ../fasttext/fasttext skipgram -input dataset/data/train_bts.txt -output model/sisg_bts -dim 300 -epoch 5 -minCount 10 -minsc 3 -maxsc 6 -minjn 1 -maxjn 0 -minn 1 -maxn 0 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025

