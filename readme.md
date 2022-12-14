vos-mjjo <br>
[![PyPI version](https://badge.fury.io/py/vos-mjjo.svg)](https://pypi.org/project/vos-mjjo/)
========


vos-mjjo is a Python port of [Vos-Mjjo](https://github.com/jomujin/vos-mjjo) v0.0.8

</br>

Notable Changes
===============
First Version

</br>

Install
=======
```python
pip install vos-mjjo
```

</br>

Usage
=====

**get_correct_array**

```python
from mjjo import cordate

test_date = "9990101"
# cordate.get_correct_one(date : str) -> list
cordate.get_correct_array(test_date)
# 입력된 문자열을 이용해 날짜 생성 규칙에 따라 현재 날짜까지 생성 가능한 모든 날짜를 리스트로 생성함
# 날짜 생성 규칙이란 연,월,일의 범위를 이용하는것으로 연도는 올해연도까지, 월은 1부터 12월까지, 일은 월별로 지정된 일까지
# 일반적으로 연도는 4자리, 월, 일은 2자리로 표기하지만 자리수 범위는 각 [0:4],[0:2],[0:2] 차지할 수 있음
```

Output:

```python
['19990101']
```

```python
from mjjo import cordate

test_date_1 = "99990101"
cordate.get_correct_array(test_date_1)

test_date_2 = "9990101"
cordate.get_correct_array(test_date_2)

test_date_3 = "990101"
cordate.get_correct_array(test_date_3)

test_date_4 = "199901"
cordate.get_correct_array(test_date_4)

test_date_5 = "019991"
cordate.get_correct_array(test_date_5)

test_date_6 = "19991"
cordate.get_correct_array(test_date_6)

test_date_7 = "1999"
cordate.get_correct_array(test_date_7)

test_date_8 = "9901"
cordate.get_correct_array(test_date_8)

```

Output:

```python
[]
['19990101']
['19900101', '19901001', '19990101']
['01990901', '19990101']
['01990901', '19990101']
['01990901', '19990101']
['01990109', '00190909', '01990901', '19990101']
['19900101', '00090901', '19990101']
```

</br>

**get_correct_one**

```python
from mjjo import cordate

test_date = "9990101"
# cordate.get_correct_one(date : str) -> str
cordate.get_correct_one(test_date)
# 입력된 문자열을 이용해 날짜 생성 규칙에 따라 현재 날짜까지 생성 가능한 모든 날짜 리스트중 가장 최신날짜를 출력
# 날짜 생성 규칙이란 연,월,일의 범위를 이용하는것으로 연도는 올해연도까지, 월은 1부터 12월까지, 일은 월별로 지정된 일까지
# 일반적으로 연도는 4자리, 월, 일은 2자리로 표기하지만 자리수 범위는 각 [0:4],[0:2],[0:2] 차지할 수 있음
```

Output:

```python
'19990101'
```

```python
from mjjo import cordate

test_date_1 = "99990101"
cordate.get_correct_array(test_date_1)

test_date_2 = "9990101"
cordate.get_correct_array(test_date_2)

test_date_3 = "990101"
cordate.get_correct_array(test_date_3)

test_date_4 = "199901"
cordate.get_correct_array(test_date_4)

test_date_5 = "019991"
cordate.get_correct_array(test_date_5)

test_date_6 = "19991"
cordate.get_correct_array(test_date_6)

test_date_7 = "1999"
cordate.get_correct_array(test_date_7)

test_date_8 = "9901"
cordate.get_correct_array(test_date_8)

```

Output:

```python
None
'19990101'
'19990101'
'19990101'
'19990101'
'19990101'
'19990101'
'19990101'
```

</br>


**look_up_array**

```python
from mjjo import cordate

CD = cordate.CorDate() 
# CorDate 클래스 부여
CD.load_date_dictionary() 
# 라이브러리 배포 폴더에 있는 date_dictionary.txt 로드
# CD.look_up_array(date : str) -> list
test_date = '99990101'
suggestions = CD.look_up_array(test_date) 
# 연월일 문자열에 Symspellpy로 max_distance=2로 날짜 리스트 출력
for sugg in suggestions:
  print(sugg)
  # or print(sugg.term, sugg.distance, sugg.count)
```

Output:

```python
# term, distance, count
19990101, 1, 158
19790101, 2, 2358
19690101, 2, 1243
19490101, 2, 1131
19590101, 2, 1106
19991101, 2, 1050
19920101, 2, 989
19990701, 2, 976
19990401, 2, 964
19990901, 2, 916
19990601, 2, 893
19991001, 2, 865
19930101, 2, 857
19900101, 2, 849
19910101, 2, 844
19950101, 2, 792
19890101, 2, 730
19940101, 2, 713
...
```

</br>

**look_up_one**

```python
from mjjo import cordate

CD = cordate.CorDate() 
# CorDate 클래스 부여
CD.load_date_dictionary() 
# 라이브러리 배포 폴더에 있는 date_dictionary.txt 로드
# CD.look_up_one(date : str) -> str 
test_date = '99990101'
suggestion = CD.look_up_one(test_date) 
# 연월일 문자열에 Symspellpy로 max_distance=2로 날짜 리스트 중 가장 거리, 빈도 가까운 값 출력
print(suggestion)
```

Output:

```python
# term, distance, count
19990101, 1, 158
```
