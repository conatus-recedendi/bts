
# jm+stroke
# ../fasttext/fasttext skipgram -input ../dataset/data/train_stroke.txt -output ../model/sisg_jm_stroke -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 6 -minn 1 -maxn 2 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
# ../fasttext/fasttext analogies ../model/sisg_jm_stroke.bin ../dataset/word_analogy_korean_stroke.txt >> ../log_jm_stroke.txt
# ../fasttext/fasttext print-word-vectors ../model/sisg_jm_stroke.bin  < ../dataset/WS353_korean_stroke.csv > ../dataset/WS353_korean_sisg_jm_stroke.vec
# python word_similiarity.py ../dataset/WS353_korean.csv ../dataset/WS353_korean_sisg_jm_stroke.vec >> ../log_jm_stroke_ws.txt
# python nsmc.py sisg_stroke pretrain 10 0.5 0.5 sisg_jm_stroke >> ../log_jm_stroke_nsmc.txt
# rm ../dataset/WS353_korean_sisg_jm_stroke.vec

# jm+cji
../fasttext/fasttext skipgram -input ../dataset/data/train_cji.txt -output ../model/sisg_jm_cji -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 6 -minn 1 -maxn 2 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
../fasttext/fasttext analogies ../model/sisg_jm_cji.bin ../dataset/word_analogy_korean_cji.txt >> ../log_jm_cji.txt
../fasttext/fasttext print-word-vectors ../model/sisg_jm_cji.bin  < ../dataset/WS353_korean_cji.csv > ../dataset/WS353_korean_sisg_jm_cji.vec
python word_similiarity.py ../dataset/WS353_korean.csv ../dataset/WS353_korean_sisg_jm_cji.vec >> ../log_jm_cji_ws.txt
python nsmc.py sisg_cji pretrain 10 0.5 0.5 sisg_jm_cji >> ../log_jm_cji_nsmc.txt
# rm ../dataset/WS353_korean_sisg_jm_cji.vec

# jm+bts
../fasttext/fasttext skipgram -input ../dataset/data/train_bts.txt -output ../model/sisg_jm_bts -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 6 -minn 1 -maxn 2 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
../fasttext/fasttext analogies ../model/sisg_jm_bts.bin ../dataset/word_analogy_korean_bts.txt >> ../log_jm_bts.txt
../fasttext/fasttext print-word-vectors ../model/sisg_jm_bts.bin  < ../dataset/WS353_korean_bts.csv > ../dataset/WS353_korean_sisg_jm_bts.vec
python word_similiarity.py ../dataset/WS353_korean.csv ../dataset/WS353_korean_sisg_jm_bts.vec >> ../log_jm_bts_ws.txt
python nsmc.py sisg_bts pretrain 10 0.5 0.5 sisg_jm_bts >> ../log_jm_bts_nsmc.txt
# rm ../dataset/WS353_korean_sisg_jm_bts.vec


# ch4+stroke
../fasttext/fasttext skipgram -input ../dataset/data/train_stroke.txt -output ../model/sisg_ch4_stroke -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 0 -minn 1 -maxn 4 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
../fasttext/fasttext analogies ../model/sisg_ch4_stroke.bin ../dataset/word_analogy_korean_stroke.txt >> ../log_ch4_stroke.txt  
../fasttext/fasttext print-word-vectors ../model/sisg_ch4_stroke.bin  < ../dataset/WS353_korean_stroke.csv > ../dataset/WS353_korean_sisg_ch4_stroke.vec
python word_similiarity.py ../dataset/WS353_korean.csv ../dataset/WS353_korean_sisg_ch4_stroke.vec >> ../log_ch4_stroke_ws.txt
python nsmc.py sisg_stroke pretrain 10 0.5 0.5 sisg_ch4_stroke >> ../log_ch4_stroke_nsmc.txt
# rm ../dataset/WS353_korean_sisg_ch4_stroke.vec

# ch4+cji
../fasttext/fasttext skipgram -input ../dataset/data/train_cji.txt -output ../model/sisg_ch4_cji -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 0 -minn 1 -maxn 4 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
../fasttext/fasttext analogies ../model/sisg_ch4_cji.bin ../dataset/word_analogy_korean_cji.txt >> ../log_ch4_cji.txt
../fasttext/fasttext print-word-vectors ../model/sisg_ch4_cji.bin  < ../dataset/WS353_korean_cji.csv > ../dataset/WS353_korean_sisg_ch4_cji.vec
python word_similiarity.py ../dataset/WS353_korean.csv ../dataset/WS353_korean_sisg_ch4_cji.vec >> ../log_ch4_cji_ws.txt
python nsmc.py sisg_cji pretrain 10 0.5 0.5 sisg_ch4_cji >> ../log_ch4_cji_nsmc.txt
# rm ../dataset/WS353_korean_sisg_ch4_cji.vec


# ch4+bts
../fasttext/fasttext skipgram -input ../dataset/data/train_bts.txt -output ../model/sisg_ch4_bts -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 0 -minn 1 -maxn 4 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
../fasttext/fasttext analogies ../model/sisg_ch4_bts.bin ../dataset/word_analogy_korean_bts.txt >> ../log_ch4_bts.txt
../fasttext/fasttext print-word-vectors ../model/sisg_ch4_bts.bin  < ../dataset/WS353_korean_bts.csv > ../dataset/WS353_korean_sisg_ch4_bts.vec
python word_similiarity.py ../dataset/WS353_korean.csv ../dataset/WS353_korean_sisg_ch4_bts.vec >> ../log_ch4_bts_ws.txt
python nsmc.py sisg_bts pretrain 10 0.5 0.5 sisg_ch4_bts >> ../log_ch4_bts_nsmc.txt
# rm ../dataset/WS353_korean_sisg_ch4_bts.vec

# ch6+stroke
../fasttext/fasttext skipgram -input ../dataset/data/train_stroke.txt -output ../model/sisg_ch4_stroke -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 0 -minn 1 -maxn 6 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
../fasttext/fasttext analogies ../model/sisg_ch4_stroke.bin ../dataset/word_analogy_korean_stroke.txt >> ../log_ch6_stroke.txt
../fasttext/fasttext print-word-vectors ../model/sisg_ch4_stroke.bin  < ../dataset/WS353_korean_stroke.csv > ../dataset/WS353_korean_sisg_ch6_stroke.vec
python word_similiarity.py ../dataset/WS353_korean.csv ../dataset/WS353_korean_sisg_ch6_stroke.vec >> ../log_ch6_stroke_ws.txt
python nsmc.py sisg_stroke pretrain 10 0.5 0.5 sisg_ch6_stroke >> ../log_ch6_stroke_nsmc.txt
# rm ../dataset/WS353_korean_sisg_ch6_stroke.vec

# ch6+cji
../fasttext/fasttext skipgram -input ../dataset/data/train_cji.txt -output ../model/sisg_ch4_cji -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 0 -minn 1 -maxn 6 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
../fasttext/fasttext analogies ../model/sisg_ch4_cji.bin ../dataset/word_analogy_korean_cji.txt >> ../log_ch6_cji.txt
../fasttext/fasttext print-word-vectors ../model/sisg_ch4_cji.bin  < ../dataset/WS353_korean_cji.csv > ../dataset/WS353_korean_sisg_ch6_cji.vec
python word_similiarity.py ../dataset/WS353_korean.csv ../dataset/WS353_korean_sisg_ch6_cji.vec >> ../log_ch6_cji_ws.txt
python nsmc.py sisg_cji pretrain 10 0.5 0.5 sisg_ch6_cji >> ../log_ch6_cji_nsmc.txt
# rm ../dataset/WS353_korean_sisg_ch6_cji.vec

# ch6+bts
../fasttext/fasttext skipgram -input ../dataset/data/train_bts.txt -output ../model/sisg_ch4_bts -dim 300 -epoch 5 -minCount 10 -minsc 2 -maxsc 15 -minjn 3 -maxjn 0 -minn 1 -maxn 6 -ws 5 -neg 5 -loss ns -thread 16 -lr 0.025
../fasttext/fasttext analogies ../model/sisg_ch4_bts.bin ../dataset/word_analogy_korean_bts.txt >> ../log_ch6_bts.txt 
../fasttext/fasttext print-word-vectors ../model/sisg_ch4_bts.bin  < ../dataset/WS353_korean_bts.csv > ../dataset/WS353_korean_sisg_ch6_bts.vec
python word_similiarity.py ../dataset/WS353_korean.csv ../dataset/WS353_korean_sisg_ch6_bts.vec >> ../log_ch6_bts_ws.txt
python nsmc.py sisg_bts pretrain 10 0.5 0.5 sisg_ch6_bts >> ../log_ch6_bts_nsmc.txt
# rm ../dataset/WS353_korean_sisg_ch6_bts.vec
