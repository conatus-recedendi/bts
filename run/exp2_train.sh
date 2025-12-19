# jm+stroke
../fasttext/fasttext skipgram -input ../dataset/data/train_stroke.txt -output ../model/sisg_jm_stroke -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 6 -minn 1 -maxn 2 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
# jm+cjı
../fasttext/fasttext skipgram -input ../dataset/data/train_cji.txt -output ../model/sisg_jm_cji -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 6 -minn 1 -maxn 2 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
# jm+bts
../fasttext/fasttext skipgram -input ../dataset/data/train_bts.txt -output ../model/sisg_jm_bts -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 6 -minn 1 -maxn 2 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025

# ch4+stroke
../fasttext/fasttext skipgram -input ../dataset/data/train_stroke.txt -output ../model/sisg_ch4_stroke -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 0 -minn 1 -maxn 4 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
# ch4+cjı
../fasttext/fasttext skipgram -input ../dataset/data/train_cji.txt -output ../model/sisg_ch4_cji -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 0 -minn 1 -maxn 4 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
# ch4+bts
../fasttext/fasttext skipgram -input ../dataset/data/train_bts.txt -output ../model/sisg_ch4_bts -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 0 -minn 1 -maxn 4 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025

# ch6+stroke
../fasttext/fasttext skipgram -input ../dataset/data/train_stroke.txt -output ../model/sisg_ch4_stroke -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 0 -minn 1 -maxn 6 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
# ch6+cjı
../fasttext/fasttext skipgram -input ../dataset/data/train_cji.txt -output ../model/sisg_ch4_cji -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 0 -minn 1 -maxn 6 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
# ch6+bts
../fasttext/fasttext skipgram -input ../dataset/data/train_bts.txt -output ../model/sisg_ch4_bts -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 0 -minn 1 -maxn 6 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025

