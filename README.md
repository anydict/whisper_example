**# whisper_example
Scratches for a quick launch of whisper


## **Real time use CPU (AMD Ryzen 5 5600X)**

|Длительность ролика, сек|Whisper Tiny|Vosk Small|Vosk 0.42|Wav2Vec2 (Large Data)|Wav2Vec2 (Small Data)|
| :-: | :-: | :-: | :-: | :-: | :-: |
|1|0\.374|0\.223|0\.233|0\.239|0\.245|
|3|0\.472|0\.356|0\.487|0\.668|0\.645|
|5|0\.572|0\.451|0\.782|1\.098|1\.012|
|10|1\.318|0\.723|1\.671|2\.421|2\.273|
|30|2\.280|1\.434|4\.216|8\.062|8\.166|
|60|4\.974|2\.324|7\.854|20\.447|20\.706|
|600|53\.600|24\.116|117\.635|Memory error|Memory error|
## **Kernel time use CPU (AMD Ryzen 5 5600X)**
 
|Длительность ролика, сек|Whisper Tiny|Vosk Small|Vosk 0.42|Wav2Vec2 (Large Data)|Wav2Vec2 (Small Data)|
| :-: | :-: | :-: | :-: | :-: | :-: |
|1|2\.007|0\.227|0\.232|1\.451|1\.416|
|3|2\.554|0\.358|0\.487|3\.874|3\.873|
|5|3\.019|0\.452|0\.782|5\.857|6\.200|
|10|7\.413|0\.712|1\.669|13\.833|13\.350|
|30|12\.562|1\.407|4\.212|47\.352|47\.145|
|60|26\.853|2\.243|7\.846|116\.512|117\.32|
|600|282\.045|24\.091|117\.516|Memory error|Memory error|
## **Real time use CUDA (Nvidia 3050 8GB)**

|Длительность ролика, сек|Whisper Tiny|Whisper Small|Faster Whisper Tiny|Vosk Small (batch 8 sec)|Vosk 0.42 (batch 8 sec)|Wav2Vec2|Nvidia NeMo|
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
|1|0\.064|0\.200|0\.068|0\.206|0\.306|0\.028|0\.029|
|3|0\.111|0\.266|0\.087|0\.235|0\.451|0\.054|0\.027|
|5|0\.131|0\.603|0\.111|0\.267|0\.837|0\.073|0\.028|
|10|0\.348|0\.851|0\.154|0\.462|1\.472|0\.165|0\.035|
|30|0\.691|1\.831|0\.289|1\.136|4\.176|0\.535|0\.069|
|60|1\.304|3\.351|0\.512|1\.984|7\.932|1\.352|0\.104|
|600|17\.676|32\.216|10\.584|18\.155|78\.541|Mem error|0\.684|
## **WER (Word Error Rate)**

|clip|Whisper Tiny|Whisper Base|Whisper Small|Faster Whisper Tiny|Faster Whisper Small|Vosk Small |Vosk 0.22|Vosk 0.42 |Wav2Vec2|Nvidia NeMo (Sber)|
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
|simple|51\.3|24\.02|9\.27|44\.79|13\.23|24\.68|20\.14|15\.51|39\.94|39\.61|
|ivrclip|35\.55|22\.91|17\.31|34\.37|15\.44|19\.39|18\.47|16\.39|30\.67|24\.49|

## **Time parallel use all resources GPU (Nvidia 3050 8GB)**

| clip count dur=5 | Whisper Tiny | Whisper Base | Whisper Small | Faster Whisper Tiny | Faster Whisper Small | Vosk Small | Vosk 0.22 | Vosk 0.42 | Wav2Vec2 | Nvidia NeMo (Sber) |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 1000 | 94.48 | 177.07 | 401.97 | 66.61 | 155.24 | 78.67 | 70.52 | 762.28 | 90.118 | 11.59 |
