vos-mjjo <br>
[![PyPI version](https://badge.fury.io/py/vos-mjjo.svg)](https://pypi.org/project/vos-mjjo/)
========

vos-mjjo is a Python port of [vos-mjjo](https://github.com/jomujin/vos-mjjo) v1.0.5

</br>

# Notable Changes

<details>
<summary><strong>Version 0.0.9 - 2023.05</strong></summary>

<div style="color: gray;">

-   Add GitHub Action workflow
-   Add decision tree model to creating date_dictionary
-   Update the date_dictionary
-   Refactoring Cordate class
    -   Apply naming Convention for Built-in Functions
    -   Apply static type hints
    -   Add module tests

</details>
<!-- <div style="line-height:50%;"><br></div> -->

<details>
<summary><strong>Version 0.0.10 - 2023.05</strong></summary>

<div style="color: gray;">

-   Refactoring Cordate class
    -   Add metadata-providing method
    -   Add methods (look_up_one_clean, look_up_array_clean)
    -   Enhance method descriptions
    -   Add error handling based on method input conditions
    -   Add module tests

</details>
<!-- <div style="line-height:50%;"><br></div> -->

<details>
<summary><strong>Version 0.0.11 - 2023.05</strong></summary>

<div style="color: gray;">

-   Issue Update
    -   By applying the zfill(8) method, the strftime method will generate a date string with 8 characters, ensuring that leading zeros are included for years below 1000

</details>
<!-- <div style="line-height:50%;"><br></div> -->

<details>
<summary><strong>Version 0.0.12 - 2023.08</strong></summary>

<div style="color: gray;">

-   Version Update
    -   Update the date dictionary to reflect the time reference of August 2023

</details>
<!-- <div style="line-height:50%;"><br></div> -->

<details>
<summary><strong>Version 0.0.13 - 2023.08</strong></summary>

<div style="color: gray;">

-   Built Bjd class
    -   Built metadata with essential functionality
    -   Developed internal functions within the class
    -   Created file data for Convaddr internal functions
-   Built Convaddr class
    -   Built metadata with essential functionality
    -   Developed internal functions within the class
    -   Add module tests

</details>
<!-- <div style="line-height:50%;"><br></div> -->

<details>
<summary><strong>Version 1.0.0 - 2023.08</strong></summary>

<div style="color: gray;">

-   Update Convaddr class
    -   Add method (union_similar_changed_bjd)
    -   Update method (correct_changed_bjd)

</details>
<!-- <div style="line-height:50%;"><br></div> -->

<details>
<summary><strong>Version 1.0.1 - 2023.08</strong></summary>

<div style="color: gray;">

-   Update Bjd file data for Convaddr internal functions
-   Structuring the Relationship Between Legal Administrative Districts
-   Built BjdObject class
    -   Built metadata with essential functionality
    -   Developed internal functions within the class
-   Built BjdConnector class
    -   Built metadata with essential functionality
    -   Developed internal functions within the class
-   Built BjdConnectorGraph class
    -   Built metadata with essential functionality
    -   Developed internal functions within the class
-   Built FullBjdConnector class
    -   Built metadata with essential functionality
    -   Developed internal functions within the class
-   Built FullBjdConnectorGraph class
    -   Built metadata with essential functionality
    -   Developed internal functions within the class
-   Built ConvAddrByBjdConnector class
    -   Built metadata with essential functionality
    -   Developed internal functions within the class
    -   Created pickle file for ConvAddrByBjdConnector internal functions

</details>
<!-- <div style="line-height:50%;"><br></div> -->

<details>
<summary><strong>Version 1.0.4 - 2023.12</strong></summary>

<div style="color: gray;">

-   Version Update
    -   Update the date dictionary to reflect the time reference of December 2023
    -   Update Bjd file data to reflect the time reference of December 2023

</details>
<!-- <div style="line-height:50%;"><br></div> -->

<details>
<summary><strong>Version 1.0.5 - 2024.01</strong></summary>

<div style="color: gray;">

-   Update and Design the Structure for Managing Changes in Administrative Districts
-   Version Update
    -   Update the date dictionary to reflect the time reference of January 2024
    -   Update Bjd file data to reflect the time reference of January 2024
    -   Reflect Changes in Administrative Districts as of January 2024
        -   January 1, 2024: Changes in administrative districts related to '부천시'
        -   January 18, 2024: Changes in administrative districts related to '전북특별자치도'

</details>
<!-- <div style="line-height:50%;"><br></div> -->

</br>

# Install

```python
pip install vos-mjjo
```

</br>

# Usage

## Cordate(Correct Date)

8자리의 날짜(`YYYYMMDD`) 형식으로 작성되어 있지 못하고 6자리(`YYYYMM` or `YYMMDD`, ...) 혹은 다른 자리수로 날짜와 오타 혹은 오기입으로 현재시점에서 부적절한 날짜가 제공되었을 경우, 이를 교정하여 8자리의 날짜(`YYYYMMDD`) 형식으로 전달하는 모듈\
해당 날짜 교정 모듈은 **건축물대장 날짜**(`착공연월`, `허가연월`, `준공연월`)를 교정하기 위해 개발되었으며 건축물대장 날짜 특성상 현재 기준으로 미래 날짜는 존재할 수 없기 때문에 현재를 기준으로 과거 날짜로만 교정됨

해당 날짜 교정 모듈에서 날짜를 교정하는 알고리즘은 2가지로\
첫번째는 연, 월, 일의 범위와 규칙을 이용하여 `현재 날짜` 까지 생성 가능한 모든 날짜 리스트와 최신 날짜로 교정하는 방법\
두번째는 미리 생성되어 있는 건축물대장 날짜 빈도 딕셔너리(`data.date_dictionary.txt`)에서 거리(날짜 문자열간의 차이 문자열 개수)와 빈도를 이용하여 가장 유사한 리스트와 최유사 날짜로 교정하는 방법으로 구성되어 있음

<details>
<summary><strong>Show instructions</strong></summary>
<br></br>

**`cordate.get_correct_array`**

-   입력된 문자열을 이용해 날짜 생성 규칙에 따라 현재 날짜까지 생성 가능한 모든 날짜를 리스트로 리턴
-   날짜 생성 규칙이란 연, 월, 일의 범위를 이용하는것으로 연도는 올해연도까지, 월은 1부터 12월까지, 일은 월별로 지정된 일까지를 의미하며 YYYYMMDD 형식의 날짜에서 연도는 4자리, 월, 일은 2자리로 표기하지만 자리수 범위는 각 [0:4],[0:2],[0:2] 차지함
-   `1999` 이라는 문자열을 입력받았을 경우, 이를 활용하여 연, 월, 일을 생성한다면 다양한 경우의 수가 존재한다. 단, 미래를 제외한 현재까지의 제한을 준다면 1999년 -월 -일처럼
-   연(년도)는 일반적으로 YYYY 네자리로 작성하지만 앞의 두자리를 생략하여 YY 로 작성하기도 하며 오타가 발생하면 1~4 자리로 다양하게 작성될 수 있음
-   Example

    -   Run

        ```python
        from mjjo import cordate

        cordate.get_correct_array("99990101")
        cordate.get_correct_array("9990101")
        cordate.get_correct_array("990101")
        cordate.get_correct_array("199901")
        cordate.get_correct_array("019991")
        cordate.get_correct_array("19991")
        cordate.get_correct_array("1999")
        cordate.get_correct_array("9901")

        ```

    -   Output

        ```python
        []
        ["19990101"]
        ["19900101", "19901001", "19990101"]
        ["01990901", "19990101"]
        ["01990901", "19990101"]
        ["01990901", "19990101"]
        ["01990109", "00190909", "01990901", "19990101"]
        ["19900101", "00090901", "19990101"]
        ```

</br>

**`cordate.get_correct_one`**

-   입력된 문자열을 이용해 날짜 생성 규칙에 따라 현재 날짜까지 생성 가능한 모든 날짜 리스트중 가장 최신날짜를 리턴
-   날짜 생성 규칙이란 연,월,일의 범위를 이용하는것으로 연도는 올해연도까지, 월은 1부터 12월까지, 일은 월별로 지정된 일까지를 의미하며 YYYYMMDD 형식의 날짜에서 연도는 4자리, 월, 일은 2자리로 표기하지만 자리수 범위는 각 [0:4],[0:2],[0:2] 차지
-   Example

    -   Run

        ```python
        from mjjo import cordate

        cordate.get_correct_one("99990101")
        cordate.get_correct_one("9990101")
        cordate.get_correct_one("990101")
        cordate.get_correct_one("199901")
        cordate.get_correct_one("019991")
        cordate.get_correct_one("19991")
        cordate.get_correct_one("1999")
        cordate.get_correct_one("9901")

        ```

    -   Output

        ```python
        None
        "19990101"
        "19990101"
        "19990101"
        "19990101"
        "19990101"
        "19990101"
        "19990101"
        ```

</br>

**`cordate.look_up_array`**

-   건축물대장 날짜 빈도 딕셔너리(`data.date_dictionary.txt`) 로드 필요
-   입력된 문자열을 이용해 data 건축물대장 날짜 빈도 딕셔너리(`data.date_dictionary.txt`) 에서 Symspellpy(`max_distance=2`) 알고리즘 적용하여 유사한 날짜 리스트 리턴
-   유사도 가중은 거리, 빈도 순으로 거리가 가까운 순서로 빈도수가 많은 순서로 정렬
-   Example

    -   Run

        ```python
        from mjjo import cordate

        CD = cordate.CorDate()
        CD.load_date_dictionary() # 라이브러리 배포 폴더에 있는 date_dictionary.txt 로드
        CD.look_up_array("99990101")
        ```

    -   Output

        ```python
        [<symspellpy.suggest_item.SuggestItem at 0x7fe5facdab60>,
        <symspellpy.suggest_item.SuggestItem at 0x7fe5fad145e0>,
        <symspellpy.suggest_item.SuggestItem at 0x7fe5fad15960>,
        <symspellpy.suggest_item.SuggestItem at 0x7fe5fad14220>,
        <symspellpy.suggest_item.SuggestItem at 0x7fe5fad164a0>,
        <symspellpy.suggest_item.SuggestItem at 0x7fe5fad151e0>,
        <symspellpy.suggest_item.SuggestItem at 0x7fe5fad155a0>,
        <symspellpy.suggest_item.SuggestItem at 0x7fe5facf5870>,
        <symspellpy.suggest_item.SuggestItem at 0x7fe5fad0c4c0>,
        <symspellpy.suggest_item.SuggestItem at 0x7fe5fad0c520>,
        ...]
        ```

    -   Run

        ```python
        from mjjo import cordate

        CD = cordate.CorDate()
        CD.load_date_dictionary() # 라이브러리 배포 폴더에 있는 date_dictionary.txt 로드

        suggestions = CD.look_up_array("99990101")
        for sugg in suggestions: # symspellpy.suggest_item 타입의 리스트는 반복문을 이용해 값을 확인 가능
            print(sugg)
        ```

    -   Output

        ```python
        19990101, 1, 716 # term, distance, count
        19980101, 2, 1361
        19960101, 2, 1351
        19970101, 2, 1317
        19950101, 2, 1286
        19940101, 2, 1236
        19920101, 2, 870
        19930101, 2, 843
        19910101, 2, 816
        19990901, 2, 743
        ...
        ```

</br>

**cordate.look_up_one**

-   건축물대장 날짜 빈도 딕셔너리(`data.date_dictionary.txt`) 로드 필요
-   입력된 문자열을 이용해 data 건축물대장 날짜 빈도 딕셔너리(`data.date_dictionary.txt`) 에서 Symspellpy(`max_distance=2`) 알고리즘 적용하여 거리, 빈도 순으로 유사도 정렬된 날짜 리스트 중 첫번째 날짜(최유사)를 리턴
-   Example

    -   Run

        ```python
        from mjjo import cordate

        CD = cordate.CorDate()
        CD.load_date_dictionary() # 라이브러리 배포 폴더에 있는 date_dictionary.txt 로드
        CD.look_up_one("99990101")
        ```

    -   Output

        ```python
        <symspellpy.suggest_item.SuggestItem at 0x7fe5fad0c190>
        ```

    -   Run

        ```python
        from mjjo import cordate

        CD = cordate.CorDate()
        CD.load_date_dictionary() # 라이브러리 배포 폴더에 있는 date_dictionary.txt 로드
        print(CD.look_up_one("99990101")) # symspellpy.suggest_item 타입의 값 출력문을 이용해 확인 가능
        ```

    -   Output

        ```python
        19990101, 1, 158 # term, distance, count
        ```

</br>

**`cordate.look_up_array_clean`**

-   cordate.look_up_array 와 동일하지만 symspellypy.suggest_item.SuggestItem 타입 리스트를 정렬을 유지한 날짜값만 추출하여 리스트 리턴
-   Example

    -   Run

        ```python
        from mjjo import cordate

        CD = cordate.CorDate()
        CD.load_date_dictionary() # 라이브러리 배포 폴더에 있는 date_dictionary.txt 로드
        CD.look_up_array_clean("99990101")
        ```

    -   Output

        ```python
        ['19990101',
        '19980101',
        '19960101',
        '19970101',
        '19950101',
        '19940101',
        '19920101',
        '19930101',
        '19910101',
        ...]
        ```

</br>

**`cordate.look_up_one_clean`**

-   cordate.look_up_one 과 동일하지만 symspellypy.suggest_item.SuggestItem 타입 리스트를 정렬을 유지한 날짜값만 추출하여 리스트 리턴
-   Example

    -   Run

        ```python
        from mjjo import cordate

        CD = cordate.CorDate()
        CD.load_date_dictionary() # 라이브러리 배포 폴더에 있는 date_dictionary.txt 로드
        CD.look_up_one_clean("99990101")
        ```

    -   Output

        ```python
        '19990101'
        ```

</br>

</details><br>

## ConvAddr(Convert Address)

법정동 변경내역을 기반으로 과거 법정동명의 주소를 입력시에 현행 법정동으로 변환하여 전달하는 모듈\
입력되는 주소는 시도, 시군구, 읍면동, 동리, 번지 순으로 기재되는 지번 체계를 기반으로 하며 해당 법정동 교정 모듈에서는 법정동(시도, 시군구, 읍면동, 동리)와 번지 사이의 공백을 일부 교정하고 과거 법정동명으로 입력되었을 경우 현행 법정동명으로 교체함\
법정동명 교체 예시로는 `인천직할시` -> `인천광역시`, `강원도` -> `강원특별자치도`, `경북 군위군` -> `대구 군위군` 등을 들 수 있으며 시도, 시군구, 읍면동, 동리 모든 변경사항에 적용됨

<details>
<summary><strong>Show instructions</strong></summary>
<br></br>

**`convaddr.correct_simple_spacing`**

-   입력된 주소 문자열(한글로 이루어진 지번 체계 주소)의 2개 이상의 연속된 공백을 단일 공백으로 변환하여 리턴
-   Example

    -   Run

        ```python
        from mjjo import convaddr

        CA = convaddr.ConvAddr()
        print(CA.correct_simple_spacing(addr="서울시 강남구  삼성동 1"))
        ```

    -   Output

        ```python
        서울시 강남구 삼성동 1
        ```

</br>

**`convaddr.correct_smallest_bjd_spacing`**

-   입력된 주소 문자열(한글로 이루어진 지번 체계 주소)의 최소 단위 법정동명("가", "동", "로", "리")과 번지 사이의 공백이 없을경우 단일 공백을 추가하여 리턴
-   Example

    -   Run

        ```python
        from mjjo import convaddr

        CA = convaddr.ConvAddr()
        print(CA.correct_smallest_bjd_spacing(addr="서울시 강남구 삼성동1"))
        ```

    -   Output

        ```python
        서울시 강남구 삼성동 1
        ```

</br>

**`convaddr.correct_changed_bjd`**

-   입력된 주소 문자열(한글로 이루어진 지번 체계 주소)의 과거 법정동명이 존재하면 변경 후 법정동명으로 변환하여 리턴
-   is_log == True 일 경우, 변경 전 후 법정동명을 출력
-   Example

    -   Run

        ```python
        from mjjo import convaddr

        CA = convaddr.ConvAddr()
        print(CA.correct_changed_bjd(addr="강원도 춘천시 서면 현암리 1-1", is_log=False))
        ```

    -   Output

        ```python
        강원특별자치도 춘천시 서면 현암리 1-1
        ```

    -   Run

        ```python
        from mjjo import convaddr

        CA = convaddr.ConvAddr()
        print(CA.correct_changed_bjd(addr="강원도 춘천시 서면 현암리 1-1", is_log=True))
        ```

    -   Output

        ```python
        2024-01-17 14:03:27 | [INFO] | 강원도 춘천시 서면 현암리
        2024-01-17 14:03:27 | [INFO] | 해당 법정동명은 변경되었습니다. 변경전 : [ 강원도 춘천시 서면 현암리 ] 변경후 : [ 강원특별자치도 춘천시 서면 현암리 ]
        강원특별자치도 춘천시 서면 현암리
        ```

</br>

**`convaddr.correct_bjd`**

-   입력된 주소 문자열(한글로 이루어진 지번 체계 주소)의 correct_simple_spacing(법정동 사이 2개 이상의 연속된 공백을 단일 공백으로 변경하는 함수), correct_smallest_bjd_spacing(최소단위 법정동과 번지 사이 공백 수정하는 함수), correct_changed_bjd(과거 법정동명 현행 법정동명으로 교정하는 함수) 순차적으로 실행하여 교정된 현행 주소 문자열을 리턴
-   is_log == True 일 경우, 변경 전 후 법정동명을 출력
-   Example

    -   Run

        ```python
        from mjjo import convaddr

        CA = convaddr.ConvAddr()
        print(CA.correct_bjd(addr="서울시 강남구 삼성동 1", is_log=False))
        ```

    -   Output

        ```python
        서울시 강남구 삼성동 1
        ```

    -   Run

        ```python
        from mjjo import convaddr

        CA = convaddr.ConvAddr()
        print(CA.correct_bjd(addr="강원도춘천시 서면 현암리 1-1", is_log=False))
        print(CA.correct_bjd(addr="강원도 춘천 시 서면 현암리 1-1", is_log=False))
        print(CA.correct_bjd(addr="강원도 춘천시 서면 현암리", is_log=False))
        print(CA.correct_bjd(addr="강원도 춘천시 서면 현암리 1-1", is_log=False))
        print(CA.correct_bjd(addr="강원도 춘천시 서면 현암리1-1", is_log=False))
        print(CA.correct_bjd(addr="강원도   춘천시 서면 현암리 1-1", is_log=False))
        ```

    -   Output

        ```python
        강원도춘천시 서면 현암리 1-1 # 시도, 시군구와 같이 최소단위 법정동의 띄어쓰기가 올바르지 않을 경우, 변환 불가
        강원도 춘천 시 서면 현암리 1-1 # 시도, 시군구와 같이 최소단위 법정동의 띄어쓰기가 올바르지 않을 경우, 변환 불가
        강원특별자치도 춘천시 서면 현암리
        강원특별자치도 춘천시 서면 현암리 1-1
        강원특별자치도 춘천시 서면 현암리 1-1
        강원특별자치도 춘천시 서면 현암리 1-1
        ```
