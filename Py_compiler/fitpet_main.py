#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import io
import requests
import re
import pandas as pd
import numpy as np
import json
import base64

# .py import 한 곳
import request_api
import regular as reg

# 네이버 크로바 호출 및 저장
def naver_clova_reader(clova_api, clova_key, uuid, image_route):
    # url img
    response = requests.get(str(image_route))
    # img to dytes
    image_bytes = io.BytesIO(response.content)
    byte_img = io.BufferedReader(image_bytes)
    # Nave clova 호출 후 호출된 row json 저장
    clova_result = request_api.request_api(clova_api, clova_key, uuid, byte_img)

    return clova_result


# 영수증 2차 분류(카드영수증/동물병원 영수증)
def Categorizer(rowdata):

    Card_data = ''
    Mixed_data = ''
    # 1차적으로 카드영수증이 의심되는 영수증 재 분류
    regex_1 = ' ?동 ?물 ?명 ?'
    regex_2 = ' ?상 ?품 ?명 ?'
    regex_3 = ' ?진 ?료 ?내 ?역 ?서 ?'
    regex_4 = ' ?수 ?량 ?'
    
    if re.search(regex_1, rowdata) != None:
        Mixed_data = rowdata
    elif re.search(regex_2, rowdata) != None:
        Mixed_data = rowdata
    elif re.search(regex_3, rowdata) != None:
        Mixed_data = rowdata
    elif re.search(regex_4, rowdata) != None:
        Mixed_data = rowdata
    # 그 외에는 card data로 판단
    else:
        Card_data = rowdata

    return Card_data, Mixed_data
    

# 영수증 1차 분류(카드영수증)
def filtering(data_saved):
    new = ''
    trash = ''
    check = True
    
    # 영수증에 청구영수증을 구분할 수 있는 키워드
    search = ['신용', '승인', '매출전표', '카드', 'Web 발신']

    for i in search:
        result = data_saved.find(i)
        if result == -1:
            new = data_saved
        else:
            trash, new = Categorizer(data_saved)
            
    if trash != '':
        check = False
            
        
    return new, check



# CSV file 을 DF으로 전환
def csv_to_data(csv_file):
    df = pd.read_csv(csv_file, header=0)
    dataset = df.values
    return dataset


# 금액관련 중복데이터 및 다중 데이터 발생시 실질데이터를 가장 큰값 혹은 가장 작은 값으로 선택
def find_one(data):
    int_data = []
    result = []
    size_Type = "min"
    if len(data) > 0:
        for i in data:
            if i != "":
                try:
                    ch_int = int(
                        i.replace(',', '').replace(' ', '').replace('.', '').replace('-', '').replace('/', '').replace(
                            ':', ''))
                    int_data.append(ch_int)
                except ValueError:
                    continue
                if ch_int >= 0:
                    size_Type = "max"
        if size_Type == "max":
            if len(int_data) > 0:
                result.append(format(max(int_data), ','))  # 중복되는 총계 및 잘못된 총계값 필터링을 위해 최대값 추출
            else:
                return 0
        else:
            if len(int_data) > 0:
                result.append(format(min(int_data), ','))  # 중복되는 총계 및 잘못된 총계값 필터링을 위해 최솟값 추출 (할인에서 사용)
            else:
                return 0
        return result
    else:
        return 0


# 정규식을 받아서 해당 내용을 지우는 함수 + 다중공백 제거
def Remover(regex, data_save):
    # 지워진거 따로 반환하기
    data_save = re.sub(regex, " ", data_save)
    data_save = Remove_Multiple_Space(data_save)
    return data_save


# 다중공백 제거 전용함수(2개 이상의 공백 제거)
def Remove_Multiple_Space(data_save):
    data_save = re.sub(" {2,}", " ", data_save)
    return data_save


# 수집된 다양한 형태의 금액 데이터를 통일된 형태로 변환
# 항목 금액 <- 형태로 변화
def Cost_Maker(cost):
    cost_result = []

    for i in cost:
        temp = []
        temp.append(i[0])
        temp.append(i[1])
        cost_result.append(temp)

    return cost_result

# 불필요한 영수증의 고정적인 내용 제거
def Remove_Words(data_save):
    data_save = Remover(" ?진료 ?및 ?미용 ?[내역]{0,}", data_save)
    data_save = Remover(" ?항 ?목 ?단 ?가 ?수 ?량 ?금 ?액 ?", data_save)
    data_save = Remover(" ?구 ?분 ?내 ?용 ?[수스] ?량 ?금 ?액 ?할 ?인 할 ?증 ?", data_save)
    data_save = Remover(" ?구 ?분 ?내 ?용 ?수 ?량 ?금 ?액 ?할 ?인 ?", data_save)
    data_save = Remover(" ?구 ?분 ?내 ?용 ?수 ?량 ?금 ?액 ?", data_save)
    data_save = Remover(" ?내 ?용 ?수 ?량 ?금 ?액 ?할 ?인 ?할 ?증 ?적 ?용 ?금 ?액 ?", data_save)
    data_save = Remover(" ?구 ?분 ?금 ?액 ?할 ?인 ?할 ?증 ?적 ?용 ?금 ?액 ?", data_save)
    data_save = Remover(" ?구 ?분 ? 할 ?인 ?할 ?증 ? 비 ?과 ?세 ? 과 ?세 ?부 ?가 ?세 ?추 ?가 ?할 ?증 ?추 ?가 ?할 ?인 ?적 ?용 ?금 ?액 ?", data_save)
    data_save = Remover(" ?발 ?행 ?일 ?:? ?", data_save)
    data_save = Remover(" ?결 ?제 ?일 ?:? ?", data_save)
    data_save = Remover(" ?믿 ?고 ? [맡말] ?길 ?수 ?있 ?는 ?병 ?원 ?[이미] ?되 ?도 ?록 ?항 ?상 ?노 ?력 ?하 ?겠 ?습 ?", data_save)
    data_save = Remover(" ?감 ?사 ?합 ?니 ?다 ?[\.!]{0,}", data_save)
    data_save = Remover(" ?S ?e ?r ?i ?a ?l N ?o ?\. ?:? ?\d{5} ?", data_save)
    data_save = Remover(" ?:? ?'?\"?\]$", data_save)
    data_save = re.sub('^ ?\[ ?\'?\"? ?', "", data_save)

    return data_save

# 흔히 발생하는 OCR 인식 오류 자체 수정
def OCR_Error_Correction(data_save):
    data_save = re.sub("합 계", "합계", data_save)
    data_save = re.sub("소 계", "소계", data_save)
    data_save = re.sub("부 가 세", "부가세", data_save)
    data_save = re.sub("할 인", "할인", data_save)
    data_save = re.sub("합 ?인", "할인", data_save)
    data_save = re.sub("할인 내역", "할인내역", data_save)
    data_save = re.sub("할인 금액", "할인금액", data_save)
    data_save = re.sub("할인 소계", "할인소계", data_save)
    data_save = re.sub("추가 할인", "추가할인", data_save)
    data_save = re.sub("합 계", "합계", data_save)
    data_save = re.sub("합 ?겨", "합계", data_save)
    data_save = re.sub("_", " ", data_save)
    data_save = re.sub("\d{1,} ?ko", "\1 kg", data_save)  # OCR 흔한 에러 수정
    data_save = re.sub("O ?kg", "0kg", data_save)  # OCR 흔한 에러 수정
    data_save = re.sub(" l ", " 1 ", data_save)  # OCR 흔한 에러 수정
    data_save = re.sub(" G ", " 6 ", data_save)  # OCR 흔한 에러 수정
    data_save = re.sub("↓", "1", data_save)  # OCR 흔한 오류 수정
    data_save = re.sub("[kK].[gG]", 'kg', data_save)  # OCR 흔한 에러 수정
    data_save = re.sub("■", ' ', data_save)  # 이상한 특수문자 제거
    data_save = re.sub("\-[ ]{0,2}\~", " ~", data_save)  # 에러 수정
    data_save = re.sub("(\d[ ]{0,1})kq", r"\1kg", data_save)  # OCR 흔한 에러 수정
    data_save = re.sub("결 ?제 ?액 ?정 ?", "결제예정", data_save)
    data_save = re.sub("합 ?거 ?", "합계", data_save)
    data_save = re.sub("항 ?독 ?", "항목", data_save)
    data_save = re.sub("동 ?물 ?이 ?름 ?", "동물명", data_save)
    data_save = re.sub("경 ?제 ?요 ?정 ?", "결제요청", data_save)
    data_save = re.sub("루 ?가 ?세", "부가세", data_save)
    data_save = re.sub("부 ?과 ?세", "부가세", data_save)
    data_save = re.sub("부 ?가 ?가 ?치 ?세 ?", "부가세", data_save)
    data_save = re.sub("발 ?햄 ?일 ?", "발행일", data_save)
    data_save = re.sub("포 ?힘", "포함", data_save)
    data_save = re.sub("수랑", "수량", data_save)
    data_save = re.sub("kq", "kg", data_save)
    data_save = re.sub("4,5-10", "4.5-10kg", data_save)
    data_save = re.sub("산 ?업 ?자", "사업자", data_save)
    data_save = re.sub(" ?Ⅱ ?", "표", data_save)
    data_save = re.sub(" ?원 ?창 ?", " 원장", data_save)
    data_save = re.sub("송 ?재 ?지 ?", "소재지", data_save)
    data_save = re.sub(" I ", " 1 ", data_save)

    return data_save

# 사업자 등록번호 관리
def Registration_Number(data_save):
    registration_number = []
    # 사업자 등록번호 : (숫자 10자리)
    regex_1 = " ?사 ?업 ?자? ?등? ?록? ?번? ?호? ?N?o? ?:? ?(\d\d\d)(\d\d)(\d\d\d\d\d) "
    # regex_2, 3 는 수정 진행
    regex_2 = " ?사 ?업 ?자? ?등? ?록? ?번? ?호? ?N?o? ?:? ?(\d{3}) ? ? ?(\d{2}) ?- ?(\d{5})\D"
    regex_3 = " ?사 ?업 ?자? ?등? ?록? ?번? ?호? ?N?o? ?:? ?(\d{3}) ?- ?(\d{2}) ? ?(\d{5})\D"
    # 사업자 등록번호 : (숫자3 - 숫자2 - 숫자5)
    regex_4 = " ?사 ?업 ?자? ?등? ?록? ?번? ?호? ?N?o? ?:? ?(\d{3} ?- ?\d{2} ?- ?\d{5})\D"
    # 사업자 등록번호 : (숫자3 - 숫자2 - 숫자3 - 숫자2)
    regex_5 = " ?사 ?업 ?자? ?등? ?록? ?번? ?호? ?N?o? ?:? ?(\d{3} ?- ?\d{2} ?- ?\d{3} ?- ?\d{2})"
    # 숫자3 - 숫자2 - 숫자5
    regex_6 = "\D(\d{3} ?- ?\d{2} ?- ?\d{5})\D"
    regex_7 = "(\d{3} ?- ?\d{2} ?- ?\d{5})\D"
    # 사업자 등록번호 뽑아내고 남는 찌꺼기 제거
    regex_8 = " ?사 ?업 ?자 ? ?등? ?록? ?번? ?호? ?-? ?:? ?"
    regex_9 = " ?등 ?록 ?번 ?호 ?:? ?"
    # 10자리로 되어있는 사업자 등록번호 및 이레귤러 케이스들 나누어서 저장하게 치환
    data_save = re.sub(regex_1, r'\1-\2-\3', data_save)
    data_save = re.sub(regex_2, r'\1-\2-\3', data_save)
    data_save = re.sub(regex_3, r'\1-\2-\3', data_save)

    registration_number_4 = re.findall(regex_4, data_save)
    registration_number.extend(registration_number_4)
    data_save = Remover(regex_4, data_save)

    registration_number_5 = re.findall(regex_5, data_save)
    registration_number.extend(registration_number_5)
    data_save = Remover(regex_5, data_save)

    registration_number_6 = re.findall(regex_6, data_save)
    registration_number.extend(registration_number_6)
    data_save = Remover(regex_6, data_save)

    registration_number_7 = re.findall(regex_7, data_save)
    registration_number.extend(registration_number_7)
    data_save = Remover(regex_7, data_save)

    data_save = Remover(regex_8, data_save)
    data_save = Remover(regex_9, data_save)

    return data_save, registration_number


# 여러 포맷의 날짜데이터를 숫자데이터만 뽑아서 리스트화
def date_strip(date):
    if date is not None:
        for i in range(len(date)):
            date[i] = date[i].replace('-', ' ')
            date[i] = date[i].replace('년', ' ')
            date[i] = date[i].replace('월', ' ')
            date[i] = date[i].replace('일', ' ')
            date[i] = date[i].strip()

            temp = date[i].split(' ')
            try:
                if len(temp) != 3:
                    temp = [x for x in temp if x]
                if len(temp[1]) != 2:
                    temp[1] = '0' + temp[1][0]
                if len(temp[2]) != 2:
                    temp[2] = '0' + temp[2][0]
                date[i] = ''.join(temp)
            except IndexError:
                continue
    return date


# 년,월,일에 해당하는 숫자데이터를 사용하여 '-'구분자를 사용하는 포맷으로 변경
def date_formatting(date):
    if date is not None:
        for i in range(len(date)):
            temp = date[i][0:4] + '-' + date[i][4:6] + '-' + date[i][6:8]
            date[i] = temp

    return date


# 날짜 데이터 추출 및 하나의 포맷으로 변경
def Charge_Date(data_save):
    date = []
    regex_1 = ' ?[\[\(]?(20\d{2} ?[ -\/~] ?[0-1]\d ?[ -\/~] ?[0-3]\d)[\]\)]? ?오?전?후? ?[0-2]{0,1}\d? ?:? ?[0-5]{0,1}\d? ?:? ?[0-5]{0,1}\d? ? ?'
    regex_2 = ' ?[\[\(]?(20\d{2} ?년 ?[0-1]?\d ?월 ?[0-3]?\d ?일) ?[0-2]{0,1}\d? ?[시:;]? ?[0-5]{0,1}\d? ?분? ?'
    regex_3 = " ?날 ?짜 ?: ?"
    regex_4 = " ?오 ?전 ?\d{1,2}시 ?[-~]? ?오? ?후? ?\d?\d? ?시? ?"
    regex_5 = " ?\(? ?오 ?전 ?\d?시? ? \d? ?밤?\d?\d?시?\)?"
    regex_6 = " 거 ?래 ?일 ?시 ?: ?"

    date_1 = re.findall(regex_1, data_save)
    date_1 = date_strip(date_1)
    date.extend(date_formatting(date_1))
    data_save = Remover(regex_1, data_save)

    date_2 = re.findall(regex_2, data_save)
    date_2 = date_strip(date_2)
    date.extend(date_formatting(date_2))
    data_save = Remover(regex_2, data_save)

    data_save = Remover(regex_3, data_save)
    data_save = Remover(regex_4, data_save)
    data_save = Remover(regex_5, data_save)
    data_save = Remover(regex_6, data_save)

    return data_save, list(set(date))


# 무게데이터 2차 필터링
def Weight_Filtering(weight):
    weight_data = []
    numbers = []
    if len(weight) != 0:# 정규식으로 가져온 무게데이터가 하나라도 있을 경우
        for i in weight:
            number = re.findall("\d*\.\d+|\d+", i)
            numbers.extend(number)
        for index, j in enumerate(numbers):
            numbers[index] = float(j)
        Num_maximum = max(numbers)
        Num_minimum = min(numbers)
        if Num_maximum == Num_minimum: # 무게데이터들중 가장 큰 값과 가장 작은 값이 같은 경우
            less = [s for s in weight if "이하" in s]
            less2 = [s for s in weight if "미만" or "<" in s]
            if len(less2) > 0:
                weight_data.append(str(Num_maximum) + "kg" + "미만")
            elif len(less) > 0:
                weight_data.append(str(Num_maximum) + "kg" + "이하")
            else:
                weight_data.append(str(Num_maximum) + "kg")
        else:
            # 무게 데이터들 중 가장 큰 값과 작은 값이 구분되는 경우
            less = [s for s in weight if "이하" in s]
            less2 = [s for s in weight if "미만" in s]
            if len(less2) > 0:
                weight_data.append(str(Num_minimum) + "kg" + "이상")
                weight_data.append(str(Num_maximum) + "kg" + "미만")
            elif len(less) > 0:
                weight_data.append(str(Num_minimum) + "kg" + "이상")
                weight_data.append(str(Num_maximum) + "kg" + "이하")
            else:
                weight_data.append(str(Num_minimum) + "kg ~ " + str(Num_maximum) + "kg")

        return weight_data
    else:# 정규식에서 가져온 무게데이터가 하나도 없을 경우
        return 0

# 동물 체중 유추가능한 데이터 수집
def Weight_Data(data_save):
    weight = []

    regex_1 = ' ?체? ?중? ?:? ? ?[\(\[\/]? ?(\d?[\.,]?\d{0,2} ?[-~]? ?\d?[\.,]?<? ?\d{1,3} ?[kK][gGo] ?~?-?이? ?상?이?하?미?만?초?과?)[\)\]\/]? ?'
    regex_2 = ' ?(\d\.\d{1,2}\-\d\.?\d{0,2}0?)'
    regex_3 = ' ?\(?~? ?kg\)?'
    regex_4 = ' [<>] '

    weight_1 = re.findall(regex_1, data_save)
    weight.extend(weight_1)
    data_save = Remover(regex_1, data_save)

    weight_2 = re.findall(regex_2, data_save)
    weight.extend(weight_2)
    data_save = Remover(regex_2, data_save)

    data_save = Remover(regex_3, data_save)
    data_save = Remover(regex_4, data_save)

    filtering_weight = Weight_Filtering(weight)
    if filtering_weight != 0:
        weight = filtering_weight

    return data_save, weight


# 동물명 추출
def Animal_Name(data_save):
    name = []
    regex_1 = "[\[\(]? ?동 ?물 ?명 ?:? ?([^진 ?료 ?비? ?][가-힣]{0,3}[^가-힣1-9\(\)]) ?[\]\)]?"
    regex_2 = "[\(]?([가-힣]{2,3}) ?\[\d{9}\]"
    regex_3 = " ?([가-힣]{1,3}) ?\' ?[sS] ?[Tt]? ?o? ?t? ?a? ?l? ?"

    name_1 = re.findall(regex_1, data_save)
    name.extend(name_1)
    data_save = Remover(regex_1, data_save)

    name_2 = re.findall(regex_2, data_save)
    name.extend(name_2)
    data_save = Remover(regex_2, data_save)

    name_3 = re.findall(regex_3, data_save)
    name.extend(name_3)
    data_save = Remover(regex_3, data_save)

    return data_save, name


# 비과세 품목, 면세 금액, 면세품목 관련 금액 추출
def Non_Texable_item(data_save):
    non_texable_item = []
    regex_1 = " ?비 ?과 ?세 ?품 ?목 ?합 ?계 ?(-?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{2}0)"
    regex_2 = " ?비 ?과 ?세 ?품 ?목 ?합 ?계 ?(-?[1-9]\d{0,2}[,\. ]\d{3})"
    regex_3 = " ?비 ?과 ?세 ?품 ?목 ?합 ?계 ?:? ?(\d{3})"
    regex_4 = " ?비 ?과 ?세 ?:? ?-?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3} ?[\d]{0,1} (-?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3})"
    regex_5 = " ?비 ?과 ?세 ?:? ?-?[1-9]\d{0,2}[,\.]\d{3} ?[\d]{0,1} (-?[1-9]\d{0,2}[,\.]\d{3})"
    regex_6 = " ?비 ?과 ?세 ?:? ?[\d]{0,1} (-?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3})"
    regex_7 = " ?비 ?과 ?세 ?:? ?[\d]{0,1} (-?[1-9]\d{0,2}[,\.]\d{3})"
    regex_8 = " ?비 ?과 ?세 \d{1,2} -?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3} (-?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3})"
    regex_9 = " ?비 ?과 ?세 \d{1,2} -?[1-9]\d{0,2}[,\.]\d{3} (-?[1-9]\d{0,2}[,\.]\d{3})"
    regex_10 = " ?비 ?과 ?세 ?:? ?([1-9]\d{0,2})"
    regex_11 = " ?비 ?과 ?세 ?:? ?0?"
    regex_12 = " ?면 ?세 ?금 ?액 ?[: ]? ?([1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3})"
    regex_13 = " ?면 ?세 ?금 ?액 ?[: ]? ?([1-9]\d{0,2}[,\.]\d{3})"
    regex_14 = " ?면 ?세 ?금 ?액 ?[: ]? ?([1-9]\d{0,2})"
    regex_15 = " ?면 ?세 ?금 ?액 ?[: ]? ?0?"
    regex_16 = " ?\( ?\* ?\) ?[는은]? 면? ?세? ?품? ?목? ?"
    regex_17 = " ?물 ?품 ?명 ?앞 ?에 ?"
    regex_18 = " ?면 ?세 ?물 ?품 ?이? ?원? ?"
    regex_19 = " ?\(?\*?\)?\·? ?표 ?시 ?가? ?되? ?어? ?는?기?"
    regex_20 = " ?있 ?는 ?"
    regex_21 = " ?되 ?어 ?"

    # * 표시가 되어있는 항목은 비과세 입니다 제거(저장X)
    data_save = Remover("\* ?표 ?시 ?가 ?[되퇴] ?어 ?있 ?는 ?항 ?목 ?은 ?비 ?과 ?세 ?", data_save)
    data_save = Remover("[표시가 ]{0,5} ?[되퇴] ?어 ?있 ?는 ?항 ?목 ?은 ?비 ?과 ?세 ?입 ?니 ?다 ?[\.]?", data_save)
    data_save = Remover("\* ?표 ?시 ?가 ?", data_save)
    data_save = Remover(" [되퇴] ?어 있 ?는 항 ?목 ?은 ?", data_save)
    data_save = Remover(" ?[되퇴] ?어 ?있 ?는 ?", data_save)
    data_save = Remover("항 ?목 ?은 ?", data_save)
    data_save = Remover(" ?상 ?품 ?명 ?앞 ?에 ?[\*]?은 ?면 ?세 ?물 ?품 ?입 ?니 ?다 ?[,\.]?", data_save)
    data_save = Remover(" ?입 ?니 ?다 ?[\.]?", data_save)

    non_texable_item_1 = re.findall(regex_1, data_save)
    non_texable_item.extend(non_texable_item_1)
    data_save = Remover(regex_1, data_save)

    non_texable_item_2 = re.findall(regex_2, data_save)
    non_texable_item.extend(non_texable_item_2)
    data_save = Remover(regex_2, data_save)

    non_texable_item_3 = re.findall(regex_3, data_save)
    non_texable_item.extend(non_texable_item_3)
    data_save = Remover(regex_3, data_save)

    non_texable_item_4 = re.findall(regex_4, data_save)
    non_texable_item.extend(non_texable_item_4)
    data_save = Remover(regex_4, data_save)

    non_texable_item_5 = re.findall(regex_5, data_save)
    non_texable_item.extend(non_texable_item_5)
    data_save = Remover(regex_5, data_save)

    non_texable_item_6 = re.findall(regex_6, data_save)
    non_texable_item.extend(non_texable_item_6)
    data_save = Remover(regex_6, data_save)

    non_texable_item_7 = re.findall(regex_7, data_save)
    non_texable_item.extend(non_texable_item_7)
    data_save = Remover(regex_7, data_save)

    non_texable_item_8 = re.findall(regex_8, data_save)
    non_texable_item.extend(non_texable_item_8)
    data_save = Remover(regex_8, data_save)

    non_texable_item_9 = re.findall(regex_9, data_save)
    non_texable_item.extend(non_texable_item_9)
    data_save = Remover(regex_9, data_save)

    data_save = Remover(regex_10, data_save)

    non_texable_item_11 = re.findall(regex_11, data_save)
    non_texable_item.extend(non_texable_item_11)
    data_save = Remover(regex_11, data_save)

    non_texable_item_12 = re.findall(regex_12, data_save)
    non_texable_item.extend(non_texable_item_12)
    data_save = Remover(regex_12, data_save)

    non_texable_item_13 = re.findall(regex_13, data_save)
    non_texable_item.extend(non_texable_item_13)
    data_save = Remover(regex_13, data_save)

    non_texable_item_14 = re.findall(regex_14, data_save)
    non_texable_item.extend(non_texable_item_14)
    data_save = Remover(regex_14, data_save)

    data_save = Remover(regex_15, data_save)
    data_save = Remover(regex_16, data_save)
    data_save = Remover(regex_17, data_save)
    data_save = Remover(regex_18, data_save)
    data_save = Remover(regex_19, data_save)
    data_save = Remover(regex_20, data_save)
    data_save = Remover(regex_21, data_save)

    return data_save, non_texable_item


# 과세품목 관련 금액 추출
def Texable_item(data_save):
    texable_item = []
    regex_1 = " ?[고과] ?세 ?[품불] ?[목복독] ?[합업] ?계 ?:? ?-?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3} (-?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3})"
    regex_2 = " ?[고과] ?세 ?[품불] ?[목복독] ?[합업] ?계 ?:? ?-?[1-9]\d{0,2}[,\.]\d{3} (-?[1-9]\d{0,2}[,\.]\d{3})"
    regex_3 = " ?[고과] ?세 ?[품불] ?[목복독] ?[합업] ?계 ?:? ?(-?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3})"
    regex_4 = " ?[고과] ?세 ?[품불] ?[목복독] ?[합업] ?계 ?:? ?(-?[1-9]\d{0,2}[,\.]\d{3})"
    regex_5 = " ?[고과] ?세 ?[품불] ?[목복독] ?[합업] ?계 ?:? ?(-?[1-9]\d{0,2})"
    regex_6 = " ?[고과] ?세 ?[품불] ?[목복독] ?[합업] ?계 ?:? ?-?0?"
    regex_7 = " ?[고과] ?세 ?공 ?급 ?가 ?액 ?:? ?([1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3}) ?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3}"
    regex_8 = " ?[고과] ?세 ?공 ?급 ?가 ?액 ?:? ?([1-9]\d{0,2}[,\.]\d{3}) ?[1-9]\d{0,2}[,\.]\d{3}"
    regex_9 = " ?[고과] ?세 ?공 ?급 ?가 ?액 ?:? ([1-9]\d{0,2}) [1-9]\d{0,2}"
    regex_10 = " ?[고과] ?세 ?공 ?급 ?가 ?액 ?:? ?([1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3})"
    regex_11 = " ?[고과] ?세 ?공 ?급 ?가 ?액 ?:? ?([1-9]\d{0,2}[,\.]\d{3})"
    regex_12 = " ?[고과] ?세 ?공 ?급 ?가 ?액 ?:? ([1-9]\d{0,2})"
    regex_13 = " ?[고과] ?세 ?공 ?급 ?가 ?액 ?:? ?0?"

    texable_item_1 = re.findall(regex_1, data_save)
    texable_item.extend(texable_item_1)
    data_save = Remover(regex_1, data_save)

    texable_item_2 = re.findall(regex_2, data_save)
    texable_item.extend(texable_item_2)
    data_save = Remover(regex_2, data_save)

    texable_item_3 = re.findall(regex_3, data_save)
    texable_item.extend(texable_item_3)
    data_save = Remover(regex_3, data_save)

    texable_item_4 = re.findall(regex_4, data_save)
    texable_item.extend(texable_item_4)
    data_save = Remover(regex_4, data_save)

    texable_item_5 = re.findall(regex_5, data_save)
    texable_item.extend(texable_item_5)
    data_save = Remover(regex_5, data_save)

    data_save = Remover(regex_6, data_save)

    texable_item_7 = re.findall(regex_7, data_save)
    texable_item.extend(texable_item_7)
    data_save = Remover(regex_7, data_save)

    texable_item_8 = re.findall(regex_8, data_save)
    texable_item.extend(texable_item_8)
    data_save = Remover(regex_8, data_save)

    texable_item_9 = re.findall(regex_9, data_save)
    texable_item.extend(texable_item_9)
    data_save = Remover(regex_9, data_save)

    texable_item_10 = re.findall(regex_10, data_save)
    texable_item.extend(texable_item_10)
    data_save = Remover(regex_10, data_save)

    texable_item_11 = re.findall(regex_11, data_save)
    texable_item.extend(texable_item_11)
    data_save = Remover(regex_11, data_save)

    texable_item_12 = re.findall(regex_12, data_save)
    texable_item.extend(texable_item_12)
    data_save = Remover(regex_12, data_save)

    data_save = Remover(regex_13, data_save)
    find_texable_item = find_one(texable_item)

    if find_texable_item != 0:
        texable_item = find_texable_item
    return data_save, texable_item


# 부가세액, 세금합계 등 세금 정보
def Tex(data_save):
    tex_item = []
    regex_1 = " ?[과고] ?세 ?품 ?[목독] ?에 ?포 ?[함힘] ?된 ?부 ?[가기] ?세 ?:? ?-?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3} (-?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3})"
    regex_2 = " ?[과고] ?세 ?품 ?[목독] ?에 ?포 ?[함힘] ?된 ?부 ?[가기] ?세 ?:? ?-?[1-9]\d{0,2}[,\.]\d{3} (-?[1-9]\d{0,2}[,\.]\d{3})"
    regex_3 = " ?[과고] ?세 ?품 ?[목독] ?에 ?포 ?[함힘] ?된 ?부 ?[가기] ?세 ?:? ?(-?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3})"
    regex_4 = " ?[과고] ?세 ?품 ?[목독] ?에 ?포 ?[함힘] ?된 ?부 ?[가기] ?세 ?:? ?(-?[1-9]\d{0,2}[,\.]\d{3})"
    regex_5 = " ?[과고] ?세 ?품 ?[목독] ?에 ?포 ?[함힘] ?된 ?부 ?[가기] ?세 ?:? ?(-?[1-9]\d{0,2})"
    regex_6 = " ?[과고] ?세 ?품 ?[목독] ?에 ?포 ?[함힘] ?된 ?부 ?[가기] ?세 ?:? ?-?0?"
    regex_7 = " ?부 ?가 ?세 ?액? ?:? ?-?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3} (-?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3})"
    regex_8 = " ?부 ?가 ?세 ?액? ?:? ?-?[1-9]\d{0,2}[,\.]\d{3} (-?[1-9]\d{0,2}[,\.]\d{3})"
    regex_9 = " ?부 ?가 ?세 ?액? ?:? ?(-?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3})"
    regex_10 = " ?부 ?가 ?세 ?액? ?:? ?(-?[1-9]\d{0,2}[,\.]\d{3})"
    regex_11 = " ?부 ?가 ?세 ?액? ?:? ?(-?[1-9]\d{0,2})"
    regex_12 = " ?부 ?가 ?세 ?액? ?:? ?-?0?"
    regex_13 = " ?[\(\[]? ?세 ?금 ?합 ?계 ?[\)\]]? ?(-?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3}) ?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3}"
    regex_14 = " ?[\(\[]? ?세 ?금 ?합 ?계 ?[\)\]]? ?(-?[1-9]\d{0,2}[,\.]\d{3}) ?[1-9]\d{0,2}[,\.]\d{3}"
    regex_15 = " ?[\(\[]? ?세 ?금 ?합 ?계 ?[\)\]]? ?(-?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3})"
    regex_16 = " ?[\(\[]? ?세 ?금 ?합 ?계 ?[\)\]]? ?(-?[1-9]\d{0,2}[,\.]\d{3})"
    regex_17 = " ?부 ?가 ?가 ?치 ?세 ?:? ?(\d{0,3}[,\.]?\d{0,3}) ?원? ? ?(\d{0,3}[,\.]?\d{0,3}) ?원?액? ?:? ?행? ?일? ?:?"

    tex_item_1 = re.findall(regex_1, data_save)
    tex_item.extend(tex_item_1)
    data_save = Remover(regex_1, data_save)

    tex_item_2 = re.findall(regex_2, data_save)
    tex_item.extend(tex_item_2)
    data_save = Remover(regex_2, data_save)

    tex_item_3 = re.findall(regex_3, data_save)
    tex_item.extend(tex_item_3)
    data_save = Remover(regex_3, data_save)

    tex_item_4 = re.findall(regex_4, data_save)
    tex_item.extend(tex_item_4)
    data_save = Remover(regex_4, data_save)

    tex_item_5 = re.findall(regex_5, data_save)
    tex_item.extend(tex_item_5)
    data_save = Remover(regex_5, data_save)

    data_save = Remover(regex_6, data_save)

    tex_item_7 = re.findall(regex_7, data_save)
    tex_item.extend(tex_item_7)
    data_save = Remover(regex_7, data_save)

    tex_item_8 = re.findall(regex_8, data_save)
    tex_item.extend(tex_item_8)
    data_save = Remover(regex_8, data_save)

    tex_item_9 = re.findall(regex_9, data_save)
    tex_item.extend(tex_item_9)
    data_save = Remover(regex_9, data_save)

    tex_item_10 = re.findall(regex_10, data_save)
    tex_item.extend(tex_item_10)
    data_save = Remover(regex_10, data_save)

    tex_item_11 = re.findall(regex_11, data_save)
    tex_item.extend(tex_item_11)
    data_save = Remover(regex_11, data_save)

    data_save = Remover(regex_12, data_save)

    tex_item_13 = re.findall(regex_13, data_save)
    tex_item.extend(tex_item_13)
    data_save = Remover(regex_13, data_save)

    tex_item_14 = re.findall(regex_14, data_save)
    tex_item.extend(tex_item_14)
    data_save = Remover(regex_14, data_save)

    tex_item_15 = re.findall(regex_15, data_save)
    tex_item.extend(tex_item_15)
    data_save = Remover(regex_15, data_save)

    tex_item_16 = re.findall(regex_16, data_save)
    tex_item.extend(tex_item_16)
    data_save = Remover(regex_16, data_save)

    tex_item_17 = re.findall(regex_17, data_save)
    tex_item.extend(tex_item_17)
    data_save = Remover(regex_17, data_save)

    find_tex_item = find_one(tex_item)
    if find_tex_item != 0:
        tex_item = find_tex_item
    return data_save, tex_item


# 전화번호 추출
def Phone_Number(data_save):
    phone_number = []
    fixed_phone_number_to_list = []
    fixed_phone_number = ''

    regex_1 = " ?전? ?화? ?번? ?호?:? ?핸? ?드? ?폰? ?:?\D(01[0|6-9][-]?\d{3,4}[-]?\d{4})\D"
    regex_2 = " ?전? ?화? ?번? ?호? ?:? ?[\(]?\D(0\d{1,2}-\d{3,4}-\d{4})[\)]?"
    regex_3 = " ?전? ?화 ?번 ?호 ?:? ?[\(\[]?(0\d{1,2}[ -]{0,}\d{3,4}[ -]{0,}\d{4})"
    regex_4 = " ?전 ?화 ?번 ?호 ?:? ?(\d{3}-\d{4})"
    regex_5 = " ?전 ?화 ?번 ?호 ?[:;]? ?"
    regex_6 = " ?[\(\[]? ?T ?E ?L ?[:;]? ?[\d-]+[\)\]]? ?"
    regex_7 = " ?T ?E ?L ?[\)\]]? ?(\d{2,4}-?\d{2,4})"
    regex_8 = " [\(\[]? ?T ?E ?L ?[\)\]]? ?"

    phone_number_1 = re.findall(regex_1, data_save)
    phone_number.extend(phone_number_1)
    data_save = Remover(regex_1, data_save)

    phone_number_2 = re.findall(regex_2, data_save)
    phone_number.extend(phone_number_2)
    data_save = Remover(regex_2, data_save)

    phone_number_3 = re.findall(regex_3, data_save)
    phone_number.extend(phone_number_3)
    data_save = Remover(regex_3, data_save)

    phone_number_4 = re.findall(regex_4, data_save)
    phone_number.extend(phone_number_4)
    data_save = Remover(regex_4, data_save)

    data_save = Remover(regex_5, data_save)

    phone_number_6 = re.findall(regex_6, data_save)
    phone_number.extend(phone_number_6)
    data_save = Remover(regex_6, data_save)

    phone_number_7 = re.findall(regex_7, data_save)
    phone_number.extend(phone_number_7)
    data_save = Remover(regex_7, data_save)

    data_save = Remover(regex_8, data_save)
    try:
        fixed_phone_number = re.sub(' ?- ?', '', phone_number[0])
        fixed_phone_number = re.sub(' ', '', fixed_phone_number)

    except:
        fixed_phone_number = ''

    fixed_phone_number_to_list.append(fixed_phone_number)

    return data_save, fixed_phone_number_to_list


# 소계 품목 합계
def Small_Sum(data_save):
    small_sum = []

    regex_1 = " ?[소스] ?[계게] ?:? ?([1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3} [1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3})"
    regex_2 = " ?[소스] ?[계게] ?:? ?([1-9]\d{0,2}[,\.]\d{3} ?[1-9]\d{0,2}[,\.]\d{3})"
    regex_3 = " ?[소스] ?[계게] ?:? ?([1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3})"
    regex_4 = " ?[소스] ?[계게] ?:? ?([1-9]\d{0,2}[,\.]\d{3})"
    regex_5 = " ?[소스] ?[계게] ?:? ?-?(\d{0,3}[,\.]?\d{0,3}[,\.]?\d{0,3} ?-?\d{0,3}[,\.]?\d{0,3}[,\.]?\d{0,3} ?-?\d{0,3}[,\.]?\d{0,3}[,\.]?\d{0,3} ?-?\d{0,3}[,\.]?\d{0,3}[,\.]?\d{0,3} ?-?\d{0,3}[,\.]?\d{0,3}[,\.]?\d{0,3}) ?"
    regex_6 = " ?[소스] ?[계게] ?:? ?-?(\d{0,3}[,\.]?\d{0,3} ?-?\d{0,3}[,\.]?\d{0,3} ?-?\d{0,3}[,\.]?\d{0,3} ?-?\d{0,3}[,\.]?\d{0,3} ?-?\d{0,3}[,\.]?\d{0,3}) ?"
    regex_7 = " ?[고과] ?세 ? ?0? ?원?공? ?급? ?[기가]? ?액? ?:? ?(\d{0,3}[,\.]?\d{0,3}) ?원?"

    small_sum_1 = re.findall(regex_1, data_save)
    small_sum.extend(small_sum_1)
    data_save = Remover(regex_1, data_save)

    small_sum_2 = re.findall(regex_2, data_save)
    small_sum.extend(small_sum_2)
    data_save = Remover(regex_2, data_save)

    small_sum_3 = re.findall(regex_3, data_save)
    small_sum.extend(small_sum_3)
    data_save = Remover(regex_3, data_save)

    small_sum_4 = re.findall(regex_4, data_save)
    small_sum.extend(small_sum_4)
    data_save = Remover(regex_4, data_save)

    data_save = Remover(regex_5, data_save)
    data_save = Remover(regex_6, data_save)

    small_sum_7 = re.findall(regex_7, data_save)
    small_sum.extend(small_sum_7)
    data_save = Remover(regex_7, data_save)

    find_small_sum = find_one(small_sum)

    if find_small_sum != 0:
        small_sum = find_small_sum

    return data_save, small_sum


# 합계
def Total_Sum(data_save):
    total_sum = []
    regex_1 = " ?[가-힣]{2,3} ?의 ?합 ?계 ?([1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3}) [1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3} ?원?"
    regex_2 = " ?[가-힣]{2,3} ?의 ?합 ?계 ?([1-9]\d{0,2}[,\.]\d{3}) [1-9]\d{0,2}[,\.]\d{3} ?원?"
    regex_3 = " ?[가-힣]{2,3} ?의 ?합 ?계 ?([1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3}) ?원?"
    regex_4 = " ?[가-힣]{2,3} ?의 ?합 ?계 ?([1-9]\d{0,2}[,\.]\d{3}) ?원?"
    regex_5 = " ?품? ?목? ?결? ?제? ?금? ?액?총? ?포? ?[함암]? ? ?중? ?간? ?합 ?계 ?금? ?액? ?:? ?([1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3}) ?원?"
    regex_6 = " ?품? ?목? ?결? ?제? ?금? ?액?총? ?포? ?[함암]? ? ?중? ?간? ?합 ?계 ?금? ?액? ?:? ?([1-9]\d{0,2}[,\.]\d{3}) ?원?"
    regex_7 = " ?총? ?청? ?구? ?금 ?액 ?:? ?([1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3}) ?원? ? ?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3} ?원?"
    regex_8 = " ?총? ?청? ?구? ?금 ?액 ?:? ?([1-9]\d{0,2}[,\.]\d{3}) ?원? ? ?[1-9]\d{0,2}[,\.]\d{3} ?원?"
    regex_9 = " ?총? ?청? ?구? ?금 ?액 ?:? ?([1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3}) ?원?"
    regex_10 = " ?총? ?청? ?구? ?금 ?액 ?:? ?([1-9]\d{0,2}[,\.]\d{3}) ?원?"
    regex_11 = " ?진? Sign ?:? "
    regex_12 = " ?결 ?제 ?[요예] ?[청정] ?:? ?([1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3})"
    regex_13 = " ?결 ?제 ?[요예] ?[청정] ?:? ?([1-9]\d{0,2}[,\.]\d{3})"
    regex_14 = " DC "
    regex_15 = " ?구? ?분? ?내? ?용? ?일? ?자? ?세? ?부? ?용? ?품? ?내?역? ?품? ?목? ?단? ?가? ? ?수 ?량 금 ?액 ?단? ?가? ?항? ?목? ?"
    regex_16 = " ?총? ?청? ?구? ?적? ?용? ?금 ?액 ?:?"
    regex_17 = " ?결? ?제? ?전? ?체? ?품? ?목? ?포? ?함? ?합 ?계 ?:? ? ?0? ?0? ?0?(\d{0,} ?[\d]{0,}[, ]{0,2}\d{0,})원?"
    regex_18 = " ?\( ?V ?A ?T ? ?포? ?함? ?\) ?([1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3}) ?원?"
    regex_19 = " ?\( ?V ?A ?T ? ?포? ?함? ?\) ?([1-9]\d{0,2}[,\.]\d{3}) ?원?"
    regex_20 = " ?\( ?V ?A ?T ? ?포? ?함? ?\) ?([1-9]\d{0,2}) ?원?"

    total_sum_1 = re.findall(regex_1, data_save)

    total_sum.extend(total_sum_1)
    data_save = Remover(regex_1, data_save)

    total_sum_2 = re.findall(regex_2, data_save)
    total_sum.extend(total_sum_2)
    data_save = Remover(regex_2, data_save)

    total_sum_3 = re.findall(regex_3, data_save)
    total_sum.extend(total_sum_3)
    data_save = Remover(regex_3, data_save)

    total_sum_4 = re.findall(regex_4, data_save)
    total_sum.extend(total_sum_4)
    data_save = Remover(regex_4, data_save)

    total_sum_5 = re.findall(regex_5, data_save)
    total_sum.extend(total_sum_5)
    data_save = Remover(regex_5, data_save)

    total_sum_6 = re.findall(regex_6, data_save)
    total_sum.extend(total_sum_6)
    data_save = Remover(regex_6, data_save)

    total_sum_7 = re.findall(regex_7, data_save)
    total_sum.extend(total_sum_7)
    data_save = Remover(regex_7, data_save)

    total_sum_8 = re.findall(regex_8, data_save)
    total_sum.extend(total_sum_8)
    data_save = Remover(regex_8, data_save)

    total_sum_9 = re.findall(regex_9, data_save)
    total_sum.extend(total_sum_9)
    data_save = Remover(regex_9, data_save)

    total_sum_10 = re.findall(regex_10, data_save)
    total_sum.extend(total_sum_10)
    data_save = Remover(regex_10, data_save)

    data_save = Remover(regex_11, data_save)

    total_sum_12 = re.findall(regex_12, data_save)
    total_sum.extend(total_sum_12)
    data_save = Remover(regex_12, data_save)

    total_sum_13 = re.findall(regex_13, data_save)
    total_sum.extend(total_sum_13)
    data_save = Remover(regex_13, data_save)

    data_save = Remover(regex_14, data_save)
    data_save = Remover(regex_15, data_save)
    data_save = Remover(regex_16, data_save)

    total_sum_17 = re.findall(regex_17, data_save)
    total_sum.extend(total_sum_17)
    data_save = Remover(regex_17, data_save)

    total_sum_18 = re.findall(regex_18, data_save)
    total_sum.extend(total_sum_18)
    data_save = Remover(regex_18, data_save)

    total_sum_19 = re.findall(regex_19, data_save)
    total_sum.extend(total_sum_19)
    data_save = Remover(regex_19, data_save)

    total_sum_20 = re.findall(regex_20, data_save)
    total_sum.extend(total_sum_20)
    data_save = Remover(regex_20, data_save)

    # 총계 금액으로 선택된 데이터들 중 가장 큰 금액 선택
    find_total_sum = find_one(total_sum)
    if find_total_sum != 0:
        total_sum = find_total_sum
    return data_save, total_sum


# 할인금액
def Discount(data_save):
    discount = []

    regex_1 = "\(? ?[CcPp] ?:? ?-?(\d{1,3} ?%)\)?"
    regex_2 = "\( ?[PpCc] ?:? ?\d{1,2}[\., ]{1,2}\d{1,2} ?%?\)"
    regex_3 = " ?진? ?료? ?추? ?가? ?등? ?급? ?할 ?인 ?금? ?액? ?\/?\(? ?[가-힣A-Za-z]{0,3}? ?\? ?:? ?-?[1-9]\d{0,2} ?[,\.] ?\d{1,3} ?[,\.] ?\d{1,3} ?원?"
    regex_4 = " ?진? ?료? ?추? ?가? ?등? ?급? ?할 ?인 ?금? ?액? ?\/?\(? ?[가-힣A-Za-z]{0,3}? ?\? ?:? ?-?[1-9]\d{0,2} ?[,\.] ?\d{1,3} ?원?"
    regex_5 = " ?진? ?료? ?추? ?가? ?등? ?급? ?할 ?인 ?금? ?액? ?\/?\(? ?[가-힣A-Za-z]{0,3}? ?\? ?:? ?\d ?(- ?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3})"
    regex_6 = " ?\(? ?할 ?인 ?\d{1,3} ?% ?\)?|\(? ?\d{1,3} ?% ? ?할 ?인 ?이? ?벤? ?트? ?\)? ?원?"
    regex_7 = " ?진? ?료? ?추? ?가? ?등? ?급? ?할 ?인 ?금? ?액? ?:? ?\d ?(- ?[1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3}) ?원?"
    regex_8 = " ?진? ?료? ?추? ?가? ?등? ?급? ?할 ?인 ?금? ?액? ?:? \d{1,2} (-[1-9]\d{0,2}[,\.]\d{3}) ?원?"
    regex_9 = " ?진? ?료? ?추? ?가? ?등? ?급? ?할 ?인 ?금? ?액? ?:? \d{1,2} [1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3} (-\d{1,3}[,\.]\d{3}[,\.]\d{3})"
    regex_10 = " ?진? ?료? ?추? ?가? ?등? ?급? ?할 ?인 ?금? ?액? ?:? \d{1,2} [1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3} (-\d{1,3}[,\.]\d{3})"
    regex_11 = " ?진? ?료? ?추? ?가? ?등? ?급? ?할 ?인 ?금? ?액? ?:? \d{1,2} [1-9]\d{0,2}[,\.]\d{3} (-\d{1,3}[,\.]\d{3}[,\.]\d{3})"
    regex_12 = " ?진? ?료? ?추? ?가? ?등? ?급? ?할 ?인 ?금? ?액? ?:? \d{1,2} [1-9]\d{0,2}[,\.]\d{3} (-\d{1,3}[,\.]\d{3})"
    regex_13 = " ?진? ?료? ?추? ?가? ?등? ?급? ?할 ?인 ?금? ?액? ?:? ?(-?\d{0,3}[\.,]?\d{0,3}) ?원?"
    regex_14 = " ?백? ?신? ?추? ?가? ?할 ?증 ?액? ?:? ?\+? ?\d{0,3}[,\.]?\d{0,3}[,\.]?\d{0,3} ?원?\+? ?\d{0,3}[,\.]?\d{0,3} ? ?원?"

    discount_1 = re.findall(regex_1, data_save)
    discount.extend(discount_1)
    data_save = Remover(regex_1, data_save)

    discount_2 = re.findall(regex_2, data_save)
    discount.extend(discount_2)
    data_save = Remover(regex_2, data_save)

    discount_3 = re.findall(regex_3, data_save)
    discount.extend(discount_3)
    data_save = Remover(regex_3, data_save)

    discount_4 = re.findall(regex_4, data_save)
    discount.extend(discount_4)
    data_save = Remover(regex_4, data_save)

    discount_5 = re.findall(regex_5, data_save)
    discount.extend(discount_5)
    data_save = Remover(regex_5, data_save)

    discount_6 = re.findall(regex_6, data_save)
    discount.extend(discount_6)
    data_save = Remover(regex_6, data_save)

    discount_7 = re.findall(regex_7, data_save)
    discount.extend(discount_7)
    data_save = Remover(regex_7, data_save)

    discount_8 = re.findall(regex_8, data_save)
    discount.extend(discount_8)
    data_save = Remover(regex_8, data_save)

    discount_9 = re.findall(regex_9, data_save)
    discount.extend(discount_9)
    data_save = Remover(regex_9, data_save)

    discount_10 = re.findall(regex_10, data_save)
    discount.extend(discount_10)
    data_save = Remover(regex_10, data_save)

    discount_11 = re.findall(regex_11, data_save)
    discount.extend(discount_11)
    data_save = Remover(regex_11, data_save)

    discount_12 = re.findall(regex_12, data_save)
    discount.extend(discount_12)
    data_save = Remover(regex_12, data_save)

    discount_13 = re.findall(regex_13, data_save)
    discount.extend(discount_13)
    data_save = Remover(regex_13, data_save)

    # 할증액
    discount_14 = re.findall(regex_14, data_save)
    discount.extend(discount_14)
    data_save = Remover(regex_14, data_save)

    # 할인데이터에 붙은 문자열 데이터 필터링
    for index, data in enumerate(discount):
        discount[index] = re.sub("[ ?진? ?료? ?추? ?가? ?등? ?급? ?할? ?인? ?[가-힣A-Za-z]{0,3}? ?금? ?액? ?:? ?%? ?이? ?벤? ?트? ?할 ?증 ?액?]", "", data)  # 할인금액에 붙은 '할인' 문자열 삭제
    find_discount = find_one(discount)
    if find_discount != 0:
        discount = find_discount
    return data_save, discount


# 영수증 내 주소 수집
def Address(data_save):
    address = []

    regex_1 = "가? ?맹? ?점? ? ?주 ?소 ?:? ?[가-힣]{1,}시? ?[가-힣]{1,}구? ?[가-힣]{0,}\d{0,2} ?[동로][가-힣]{0,}\d{0,3}번? ?길? ?\d{0,3} ?\d? ?층? ?-? ?\d?\d?번? ?지?\d{0,} ?층? ?\d{0,}호?"
    regex_2 = "가? ?맹? ?점? ? ?주 ?소 ?:? ?[\D ]+시 ?\D+구 ?\D+[동로]"
    regex_3 = "가 ?맹 ?점 ?명? ?:? ?(\D+병 ?원 ?)"
    regex_4 = " ?\)? ?정? ?상? ?매? ?입? ?가 ?맹 ?점 ?명? ?:? ?정? ?보? ?즉? ?시? ?결? ?제? ?\/? ?사? ?업? ?자? ?2?4?시?\D+병원"
    regex_5 = "\( ?\D+ ?동 ?\)"
    regex_6 = " ?[가-힣]+도 ?[가-힣]+시 ?[가-힣]{0,}구?로?동?번?길? ?[가-힣1-9]{0,}구?로?동?번?길? ?\d?층?"

    address_1 = re.findall(regex_1, data_save)
    address.extend(address_1)
    data_save = Remover(regex_1, data_save)

    address_2 = re.findall(regex_2, data_save)
    address.extend(address_2)
    data_save = Remover(regex_2, data_save)

    address_3 = re.findall(regex_3, data_save)
    address.extend(address_3)
    data_save = Remover(regex_3, data_save)

    address_4 = re.findall(regex_4, data_save)
    address.extend(address_4)
    data_save = Remover(regex_4, data_save)

    address_5 = re.findall(regex_5, data_save)
    address.extend(address_5)
    data_save = Remover(regex_5, data_save)

    address_6 = re.findall(regex_6, data_save)
    address.extend(address_6)
    data_save = Remover(regex_6, data_save)

    return data_save, address


# 대표자명
def Ceo(data_save):
    ceo = []

    regex_1 = " ?대 ?표 ?자 ?명? ?:? ?([가-힣]{2,4} ?외? ?[1-9]{0,1} ?명) ?"
    regex_2 = " ?대 ?표 ?자 ?명? ?:? ?:? ?([가-힣]{2,4})"
    regex_3 = " ?\[?대 ?표 ?자 ?명? ?\]? ?:? ?([가-힣]{0,4})"
    regex_4 = "[가-힣]+청? ?구? ?서? ?병? ?원? ? 원 ?장 ?:? ?([가-힣]{0,4})"

    ceo_1 = re.findall(regex_1, data_save)
    ceo.extend(ceo_1)
    data_save = Remover(regex_1, data_save)

    ceo_2 = re.findall(regex_2, data_save)
    ceo.extend(ceo_2)
    data_save = Remover(regex_2, data_save)

    ceo_3 = re.findall(regex_3, data_save)
    ceo.extend(ceo_3)
    data_save = Remover(regex_3, data_save)

    ceo_4 = re.findall(regex_4, data_save)
    ceo.extend(ceo_4)
    data_save = Remover(regex_4, data_save)

    return data_save, ceo


# 병원명
def Hospital_name(data_save):
    hospital_name = []
    regex_1 = " ?병 ?원 ?명 ?:? ?(2? ?4?시? ?[가-힣 24]{2,}병 ?원 ?2? ?4? ?시?) ?"
    regex_2 = " ?청 ?구 ? ?원 ?명 ?:? ?(2? ?4?시? ?[가-힣 24]{2,}병 ?원 ?2? ?4? ?시?) ?"
    regex_3 = " ?병 ?원 ?명 ?:? ?(2? ?4?시? ?[가-힣 24]{2,}센 ?터 ?2? ?4? ?시?) ?"
    regex_4 = " ?청 ?구 ? ?원 ?명 ?:? ?(2? ?4?시? ?[가-힣 24]{2,}센 ?터 ?2? ?4? ?시?) ?"
    regex_5 = " ?병 ?원 ?명 ?:? ?"
    regex_6 = " ?청 ?구 ?원 ?명 ?:? ?"
    regex_7 = "[가-힣]+ 동 ?물 ?병 ?원 ?"
    regex_8 = " ?(2?4? ?시? ?[가-힣]{0,} ?2?4?시? ?V?I?P?N? ?[가-힣]+센 ?터 ?)"

    hospital_name_1 = re.findall(regex_1, data_save)
    hospital_name.extend(hospital_name_1)
    data_save = Remover(regex_1, data_save)

    hospital_name_2 = re.findall(regex_2, data_save)
    hospital_name.extend(hospital_name_2)
    data_save = Remover(regex_2, data_save)

    hospital_name_3 = re.findall(regex_3, data_save)
    hospital_name.extend(hospital_name_3)
    data_save = Remover(regex_3, data_save)

    hospital_name_4 = re.findall(regex_4, data_save)
    hospital_name.extend(hospital_name_4)
    data_save = Remover(regex_4, data_save)

    data_save = Remover(regex_5, data_save)
    data_save = Remover(regex_6, data_save)
    data_save = Remover(regex_7, data_save)

    hospital_name_8 = re.findall(regex_8, data_save)
    hospital_name.extend(hospital_name_8)
    data_save = Remover(regex_8, data_save)

    return data_save, hospital_name


# 담당자명
def Manager_name(data_save):
    manager_name = []

    regex_1 = " ?[담당] ?[담당] ?자? ?수? ?의? ?사? ?:? ?([가-힣]{0,4})"

    manager_name_1 = re.findall(regex_1, data_save)
    manager_name.extend(manager_name_1)
    data_save = Remover(regex_1, data_save)

    return data_save, manager_name


# 영수증에서 불필요 데이터 2차 제거
def receipt_filter(data_saved):
    data_save = ''
    data_removed = ''

    regex_1 = "기간 : (.+)"
    regex_2 = "고? ?객? ?이 ?름 ? ?:? ?[가-힣]{2,4} (.+)"
    regex_3 = "다 ?음 ?예 ?[정약] ?일? ?:?(.+)"
    regex_4 = "(재? ?진 ?찰? ?료 ?비?.+)"

    if re.search(regex_1, data_saved) != None:
        data_save = re.search(regex_1, data_saved).group(1)
        data_removed = re.sub(regex_1, "", data_saved)

    elif re.search(regex_2, data_saved) != None:
        data_save = re.search(regex_2, data_saved).group(1)
        data_removed = re.sub(regex_2, "", data_saved)

    elif re.search(regex_3, data_saved) != None:
        data_save = re.search(regex_3, data_saved).group(1)
        data_removed = re.sub(regex_3, "", data_saved)

    elif re.search(regex_4, data_saved) != None:
        data_save = re.search(regex_4, data_saved).group(1)
        data_removed = re.sub(regex_4, "", data_saved)

    else:
        data_save = data_saved

    return data_save, data_removed


# 글씨 공백 글씨 합치는 함수
def Text_Whitespace_Text_Editer(data_save):
    regex_1 = "([가-힣a-zA-Z-\.\,\(\)]) ([가-힣a-zA-Z-\.\,\(\)])"
    regex_2 = "(\d) ?([,\.]) ?(\d)"
    data_save = re.sub(regex_1, r'\1\2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_1, r'\1\2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_2, r'\1\2\3', data_save)
    data_save = Remove_Multiple_Space(data_save)

    return data_save


# 다중 0 제거 (일부 이레귤러 영수증에 필요)
def Too_Many_0_Remover(data_save):
    regex_1 = "(\d) \d \d \d \d \d \d \d \d \d \d \d \d \d \d \d \d \d \d \d (\d)"
    regex_2 = "(\d) \d \d \d \d \d \d \d \d \d \d \d \d \d \d \d \d \d \d (\d)"
    regex_3 = "(\d) \d \d \d \d \d \d \d \d \d \d \d \d \d \d \d \d \d (\d)"
    regex_4 = "(\d) \d \d \d \d \d \d \d \d \d \d \d \d \d \d \d \d (\d)"
    regex_5 = "(\d) \d \d \d \d \d \d \d \d \d \d \d \d \d \d \d (\d)"
    regex_6 = "(\d) \d \d \d \d \d \d \d \d \d \d \d \d \d \d (\d)"
    regex_7 = "(\d) \d \d \d \d \d \d \d \d \d \d \d \d \d (\d)"
    regex_8 = "(\d) \d \d \d \d \d \d \d \d \d \d \d \d (\d)"
    regex_9 = "(\d) \d \d \d \d \d \d \d \d \d \d \d (\d)"
    regex_10 = "(\d) \d \d \d \d \d \d \d \d \d \d (\d)"
    regex_11 = "(\d) \d \d \d \d \d \d \d \d \d (\d)"
    regex_12 = "(\d) \d \d \d \d \d \d \d \d (\d)"
    regex_13 = "(\d) \d \d \d \d \d \d \d (\d)"
    regex_14 = "(\d) \d \d \d \d \d \d (\d)"
    regex_15 = "(\d) \d \d \d \d \d (\d)"
    regex_16 = "(\d) \d \d \d \d (\d)"
    regex_17 = "(\d) \d \d \d (\d)"
    regex_18 = "(\d) \d \d (\d)"

    data_save = re.sub(regex_1, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_2, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_3, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_4, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_5, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_6, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_7, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_8, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_9, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_10, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_11, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_12, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_13, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_14, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_15, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_16, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_17, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub(regex_18, r'\1 0 \2', data_save)
    data_save = Remove_Multiple_Space(data_save)

    return data_save


# 자주 있는 0 관련 에러 항목을 0 -> O로 치환하여 처리(금액 추출 문제 해결위해 사용)
# 표준화 과정에서 해결됨
def Error_0_Fixer(data_save):
    data_save = re.sub("NPH\(? ?1 ?0 ?0 ?I? ?U? ?1? ?0? ?\)?", "NPH(1OOIU)", data_save)
    data_save = re.sub("00 ?g", "OOg", data_save)
    data_save = re.sub("0 ?g", "Og", data_save)
    data_save = re.sub("00 ?매", "OO매", data_save)
    data_save = re.sub("0 ?매", "O매", data_save)
    data_save = re.sub("0 ?ea", "Oea", data_save)
    data_save = re.sub("0cm", "Ocm", data_save)
    data_save = re.sub("0층", "O층", data_save)
    data_save = re.sub("iSmart ?300", "iSmart3OO", data_save)
    data_save = re.sub("00ml", "OOml", data_save)
    data_save = re.sub("0ml", "Oml", data_save)
    data_save = re.sub("0개", "O개", data_save)
    data_save = re.sub("NX ?- ?\d00", "NX-5OO", data_save)
    data_save = re.sub("Physicalexam 1", "Physicalexam1", data_save)
    data_save = re.sub("혈 ?액 ?검 ?사 ?0", "혈액검사", data_save)
    data_save = re.sub("피 ?하 ?주 ?사 ?0", "피하주사O", data_save)
    data_save = re.sub("잘라탄0.00\d ?", "잘라탄", data_save)
    data_save = re.sub(" ?마 ?취 ?전 ?1 ?0 ?종 ?", "마취전1O종", data_save)
    data_save = re.sub("PT10", "PT1O", data_save)
    data_save = re.sub("진 ?료 ?비?0+", "진료 ", data_save)
    data_save = re.sub("BS\-330", "BS\-33O", data_save)

    return data_save


# 불필요한 내용 제거 3차
def Remove_Words_2(data_save):
    data_save = Remover(" 0%", data_save)
    data_save = Remover(" 0 ?원", data_save)
    data_save = Remover("\(?\[? ?I? ?C? ?신 ?용 ?구? ?매? ?\]?승? ?인? ?\]?정? ?보? ?\(?고? ?객? ?용? ?\)? ?:? ?I? ?\)", data_save)
    data_save = Remover("\d{2} ?: ?\d{2} ?: ?\d{2} ?", data_save)
    data_save = Remover("\[ ?일 ?시 ?불 ?:? ?\]? ?", data_save)
    data_save = Remover("\(? ?일 ?시 ?불 ?\)?", data_save)
    data_save = Remover("\(? ?일 ?시 ?불 ?\)?", data_save)
    data_save = Remover("계? ?좌? ? ?E? ?보? ?호? ? ?카? ?드? ?가? ?맹? ?점? ?/?일? ?련? ?사? ?업? ?자? ?등? ?록? ?가? ?맹? ?점? ?전? ?표? ?거? ?래? ? ?승? ?인? ?번 ?호 ?:? ?", data_save)
    data_save = Remover("섹? ?션? ?자? ?금? ?가? ?맹? ?점? ?청? ?구? ?매? ?형? ?지? ?급? ?형? ?캐? ?시? ?백? ?카? ?드? ?결 ?제 ?\(?[예에]? ?정? ?\)? ?일? ?:? ?요? ?청? ?:? ?0? ?\?? ?:? ?없? ?음? ?:? ?:? ?취? ?소? ?가? ?가? ?능? ?액? 현? ?금? ?드? ?:? ?현? ?:? ?\d{0,3}[,\.]{0,2}\d{0,3}[,\.]{0,2}\d{0,3} ? ?중?원?섹? ?션? ?", data_save)
    data_save = Remover(" ?거 ?래 ?내 ?용 ?", data_save)
    data_save = Remover(" ?신? ?한? ?K? ?B? ?최? ?종? ?롯? ?데? ?자? ?사? ?현? ?대? ?하? ?나? ?체? ?크? ?카? ?드? ?\/? ?삼? ?성? ?하? ?나? ?비? ?자? ?카? ?드? ?페? ?이? ?\/?I? ?C? ?신? ?용? ?승 ?인 ?상? ?태? ?", data_save)
    data_save = Remover(" ?원? ?봉? ?사? ?료? ?체? ?크? ?카? ?드? ?\)? ?정? ?상? ?매? ?입? ?가 ?맹 ?점 ?명? ?:? ?정? ?보? ?즉? ?시? ?결? ?제? ?\/? ?사? ?업? ?자? ?2?4?시?\d{0,11}", data_save)
    data_save = Remover(" ?\(?실? ?물? ? ?N? ?H? ?삼? ?성? ?국? ?민? ?[하히]? ?나? ?신? ?한? ?롯? ?데? ?V? ?I? ?S? ?A? ?우? ?리? ?비? ?씨? ?체? ?크? ?카 ?드 ?종? ? ?류? ?사?체? ?크? ?\)?명? ?", data_save)
    data_save = Remover(" ?5?0?[,\.]{0,1}0?0?0?원? ?이? ?하? ?는? ?무서명거래 ?알? ?림? ?자? ?동? ?이? ?[체제]? ?[Kk]? ?[Il]? ?S? ?로? ?제? ?출? ?E? ?D? ?C? ?매? ?출? ?전? ?표? ?알? ?림? ?", data_save)
    data_save = Remover(" ?\d\d\ ?/ ?\d\d ?/ ?\d\d ?원?\(? ?I? ?C? ?\)?", data_save)
    data_save = Remover(" ?새? ?마? ?을? ?차? ?이? ?B? ?C? ?국? ?민? ?우? ?리? ?삼? ?성? ?[Nn]? ?[Hh]? ?신? ?한? ?카? ?카? ?오? ?마? ?스? ?터? ?\d{4} ?- ?\d{4} ?- ?\d{4} ?-? ?\d?\d?\d?\d? ?-?\d?\d?\d?\d? ?원?계?", data_save)
    data_save = Remover(" ?K? ?B? ? ?가 ?맹 ?섬? ?점? ?N? ?o? ?:? ?이? ?용? ?내? ?역? ?", data_save)
    data_save = Remover(" ?\D+24 ?시 ?\D+[센터병원]{2} ?", data_save)
    data_save = Remover(" ?\[? ?IC ?신 ?용 ?한?구? ?매? ?\]?", data_save)
    data_save = Remover(" ?할? ?부? ?:? ?\d?\d?\d?\d?-?\d?\d?\*\*\/? ?-?\*?\*?-? ?\d?\d?\d?\d?-?\d?\d?\d?\d?", data_save)
    data_save = Remover(" ?\/ ?[Tt] ?[Ee] ?[Ll] .+\/", data_save)
    data_save = Remover("\(?\[? ?회 ?원 ?용? ?\]?\)?주? ?소? ? ?:?가? ?입? ?후? ?", data_save)
    data_save = Remover(" ?했? ?영? ?수? ?바? ?랍? ?처? ?리? ?혜? ?택? ?을? ?환? ?불? ?됩? ?받? ?으? ?셨? ?연? ?중? ?3?6?5?일? ?조? ?제? ?하? ?였? ?청? ?구? ?있? ?양? ?해? ?부? ?탁? ?가? ?능? ?시? ?키? ?셔? ?야? ?드? ?립? ?필? ?요? ?하? ?겠? ?습? ?저? ?희? ?진? ?료? ?합? ?니 ?다 ?\.? ?", data_save)
    data_save = Remover(" ?\[ ?[sS] ?[hH] ?[Ii] ?[nN] ?[hH] ?[aA] ?[nN] ?[mM]? ?[aA]? ?[sS]? ?[tT]? ?[eE]? ?[rR]?[vV]? ?[iI]? ?[sS]? ?[aA]? ?\]?", data_save)
    data_save = Remover(" ?알? ?림? ?자? ?동? ?이? ?체? ?K ?I ?S ?로 ?제? ?[출줄]? ?알? ?림? ?자? ?동? ?이? ?체? ?", data_save)
    data_save = Remover(" ?\[? 이? ?계? ?산? ?서? ?는? ?물? ?품? ?반? ?품? ?시? ?본? ?Q? ?R? ?[현연]? ?금? ?영 ?수 ?증 ?을? ?필? ?히? ?지? ?참? ?하? ?여? ?주? ?시? ?기? ?신? ?청? ?완? ?료? ?발? ?급? ?설? ?정? ?으? ?로? ?사? ?용? ?할? ?수? ?있? ?으?며? ?,? ?재? ?발? ?행? ?하? ?지? ?않? ?교? ?환? ?및? ?없? ?으? ?면? ?\]?", data_save)
    data_save = Remover(" ?상 ?품 ?명 ?앞? ?에? ?\*? ?은? ?면? ?세? ?물? ?청? ?구? ?품? ?스? ?:? ?", data_save)
    data_save = Remover(" ?\( ?V ?A ?T ? ?포? ?함? ?\) ?원?", data_save)
    data_save = Remover(" ?\[? 단? ?위? ?당? ?1? ?회? ?청? ?구? ?오? ?늘? ?청 ?구 ? ?일? ?:? ?\d{0,3}[,\.]?\d{0,3}[,\.]?\d{0,3} ?대? ?상? ?자? ?항? ?목? ?완? ?료? ?시? ?각? ?-? ?\]?\)?", data_save)
    data_save = Remover(" ?거? ?[가-힣]{0,1} ?매? ?일 ?시 ?:? ?\/?할? ?부? ?비? ?고? ?", data_save)
    data_save = Remover(" ?:? ?발 ?:? ?행 ?:?일 ?:? ?", data_save)
    data_save = Remover(" ?1?\.? ?신용 ?매? ?출? ?전? ?표? ?등? ?급? ?:? ?", data_save)
    data_save = Remover(" ?일? ?자? ?환? ?자? ?이? ?름? ? ?세 ?부 ?내 ?역 ?수? ?량? ?물? ?품? ?", data_save)
    data_save = Remover(" ?지 ?침 ?사 ?항 ?:? ?오? ?[후전]{0,1}\d?시? ?오? ?[후전]{0,1} ?[0-2]?\d?시?", data_save)
    data_save = Remover(" ?유? ?효? ?기? ?간? ?\/? ?거? ?래? ?유? ?형? ?할 ?부 ?개? ?월? ?공? ?급? ?가? ?액? ?:? ?[1-9]?\d{0,2}[,\.]?\d?\d?\d?[,\.]?\d?\d?\d? ?원?개? ?월? ?", data_save)
    data_save = Remover(" ?결? ?제? ?방? ?법? ?단 ?말 ?기 ?I? ?D? ?:? ?\(? ?고? ?객? ?용? ?\)? ?N? ?O? ?", data_save)
    data_save = Remover(" ?알 ?림 ?메? ?세? ?지? ?전? ?자? ?서? ?명? ?전? ?표? ?임? ?:? ?전? ?자? ?서? ?명? ?전? ?표? ?문? ?의? ?:? ?E? ?D? ?C? ?매? ?출? ?표? ?톡? ?도? ?착? ?", data_save)
    data_save = Remover(" ?V ?A ?N ?K ?E ?Y ?:? ?\d{0,16} ?", data_save)
    data_save = Remover(" ?창? ?구? ?전? ?자? ?매 ?입 ? ?사? ?일? ?명? ?시? ?또? ?는? ?고?불? ?가? ? ?:? ?원? ?", data_save)
    data_save = Remover(" ?전 ?자 ?전 ?표 ?", data_save)
    data_save = Remover(" ?전 ?자 ?서 ?명 ?전 ?표 ?임? ?", data_save)
    data_save = Remover(" ?전 ?자 ?차 ?트 ?", data_save)
    data_save = Remover(" ?전 ?자 ?서 ?명 ?", data_save)
    data_save = Remover(" ?항? ?목? ?상? ?품? ?총? ?진? ?료? ?구? ?분? ?진? ?찰? ?비? ?료? ?내? ?용? ?단? ?가? ?항? ?목? ?명? ?수 ?량 ?단? ?위? ?가? ?적? ?립? ?용? ?항? ?목? ?:? ?", data_save)
    data_save = Remover(" ?일 ?반 ?진 ?료 ?시 ?간 ?:? ?야? ?간? ?응? ?급? ?진? ?료? ?: ?오? ?[후전]{0,1} ?[0-2]{0,1}\d?시? ?-? ?야? ?간? ?응? ?급? ?진? ?료? ?:? ?오? ?[후전]{0,1} ?-? ?", data_save)
    data_save = Remover(" ?고 ?객 ?성? ?명 ?:? ?[가-힣]{2,4} ?", data_save)  # 고객명
    data_save = Remover(" ?고 ?객 ?이 ?름 ?:? ?[가-힣]{2,4} ?", data_save)  # 고객명
    data_save = Remover(" ?실? ?제? ?와? ?다? ?른? ?신? ?표? ?\(?\[? ?고 ?객 ?용? ?센? ?터? ?보? ?관? ?용? ?-?\]?\)?상? ?호? ?:? ?", data_save)
    data_save = Remover(" ?물 ?품 ?가 ?액 ?:? ?[1-9]{0,1}\d{0,2}[,\.]{0,1}\d{0,3}[,\.]{0,1}\d{0,3} ?원? ?원? ?[1-9]{0,1}\d{0,2}[,\.]{0,1}\d{0,3}[,\.]{0,1}\d{0,3} ?원?행? ?일? ?받? ?을? ?받? ?은? ?결? ?제? ?수? ?단? ?별? ?결? ?제? ?내? ?역? ?액? ?:? ?가? ?액? ?:? ?=? ?", data_save)
    data_save = Remover(" ?남? ?은? ?현? ?재? ?[12]? ?\.? ?이? ?전? ?미 ?수 ?금? ?변? ?제? ?발? ?생? ?원? ?:? ?0? ?총? ?액? ?:? ?월? ?", data_save)
    data_save = Remover(" ?총? ?당? ?일? ?전? ?캐? ?시? ?백? ?적 ?립 ?금? ?사? ?용? ?:? ?", data_save)
    data_save = Remover(" ?종? ?이? ?영? ?수? ?증? ?과? ?동? ?일? ?한? ?내 ?용 ?", data_save)
    data_save = Remover(" ?실? ?제? ?세? ?가? ?격? ?상? ?세? ?기? ?타? ?거? ?래? ?방? ?문? ?및? ?미? ?내? ?원? ?예? ?방? ?접? ?종? ?물? ?진? ?료? ?비? ?결? ?제? ?용? ?품? ?내 ?역 ?품? ?목? ?단? ?기? ?서? ?을? ?물? ?명? ?:? ?으? ?로? ?확? ?인? ?증? ?시?", data_save)
    data_save = Remover(" ?\[ ?[Hh]? ?[Yy]? ?[Uu]? ?[Nn]? ?[Dd]? ?[Aa]? ?[Ii]? ?[Kk]? ?[Oo]? ?[Nn]? ?[Aa]? ?[Ll]? ?[Oo]? ?[Tt]? ?[Tt]? ?[Ee]? ?[Mm]? ?[Aa]? ?[Ss]? ?[Tt]? ?[Ee]? ?[Rr]? ?[cC] ?[aA] ?[rR] ?[dD] ?\]", data_save)
    data_save = Remover(" ?문? ?결? ?국? ?제 ?예 ?정 ?일? ?자? ?:? ?[1-9]{0,1}\d{0,2}[,\.]{0,1}\d{0,3}[,\.]{0,1}\d{0,3} ?행? ?일? ?:? ?", data_save)
    data_save = Remover(" ?지? ?도? ?보? ?기? ?\·?\.? ?상 ?세 ?", data_save)
    data_save = Remover(" ?\[? ?\(?K? ?E? ?B? ?H? ?A? ?N? ?A? ?S? ?A? ?M? ?S? ?U? ?N? ?G? ?H? ?C? ? ?V ?[Iil] ?S ?A ?C?R?E?D?I?T? ?\)? ?T? ?V? ?R? ?\]? ?:? ?", data_save)
    data_save = Remover(" 1\+2 ", data_save)
    data_save = Remover(" ?\(? ?\[? ?법 ?인 ?\]? ?\)? ?", data_save)
    data_save = Remover(" ?-? ?1일 ?\d ?회 ?", data_save)
    data_save = Remover(" \*+ ", data_save)
    data_save = Remover("진 ?료 ?합 ?니 ?다 ?", data_save)
    data_save = Remover("★", data_save)
    data_save = Remover("S ?e ?r ?i ?a ?l ?N? ?o? ?\.? ?:? ?", data_save)
    # 진료비 관련된 잘못된 데이터 제거
    data_save = re.sub("([가-힣]+초? ?재? ?진 ?료 ?비? ?)", " 진료 ", data_save)
    # 소재지에 붙어있는 한글데이터 모두 제거(주소 추출 전 해당 내용 확인)
    data_save = Remover("[가-힣]+ ?소재지 ?:? ?[가-힣]+", data_save)
    data_save = Remover("^-? ?1? ?\*? ?□? ?\/? ?\~? ?\[? ?\]? ?\*?\×? ?\.? ?", data_save)
    data_save = Remover("원장님 \[? ?\]? ?~?\*? ?\[? ?\]?", data_save)
    data_save = Remover("\[ \]", data_save)
    data_save = Remover(" % ", data_save)
    data_save = Remover(".+\[[Ww] ?e ?b ?발 ?신 ?\].+", data_save)

    # 시작할때 있는 공백 제거
    data_save = Remove_Multiple_Space(data_save)
    data_save = re.sub("^ ", "", data_save)
    return data_save

# 금액 추출하는 함수
def Cost(data_save):
    cost = []

    #regex_0 = "([가-힣a-zA-Z\+1-9 \-\(\)\/\~\[\]\.\,\·\&\:\#\*]{2,}) ?([1-9]\d{0,2}[kK][gGo]? ?상?이?하?미?만?초?과?)? ([1-9]\d{0,2}[,\.]\d{3}) ?원? \d{1,2} [1-9]\d{0,2}[,\.]\d{3} ?원?"  # 정규식 추가
    regex_1 = " ?([가-힣a-zA-Z\(]{2,}) ?\( ?([1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3}) ?\) ?"
    regex_2 = " ?([가-힣a-zA-Z\(]{2,}) ?\( ?([1-9]\d{0,2}[,\.]\d{3}) ?\) ?"
    regex_3 = "([가-힣a-zA-Z\+1-9 \-\(\)\/\~\[\]\.\,\·\&\:\#\*]{2,}) ([1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3}) ?원? \d{1,2} [1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3} ?원?"
    regex_4 = "([가-힣a-zA-Z\+1-9 \-\(\)\/\~\[\]\.\,\·\&\:\#\*]{2,}) ([1-9]\d{0,2}[,\.]\d{3}) ?원? \d{1,2} [1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3} ?원?"
    regex_5 = "([가-힣a-zA-Z\+1-9 \-\(\)\/\~\[\]\.\,\·\&\:\#\*]{2,}) ([1-9]\d{0,2}[,\.]\d{3}) ?원? \d{1,2} [1-9]\d{0,2}[,\.]\d{3} ?원?"
    regex_6 = "([가-힣a-zA-Z\+1-9 \-\(\)\/\~\[\]\.\,\·\&\:\#\*]{2,}) ([1-9]\d{0,2}) ?원? \d{1,2} [1-9]\d{0,2}[,\.]\d{3} ?원?"
    regex_7 = "([가-힣a-zA-Z\+1-9 \-\(\)\/\~\[\]\.\,\·\&\:\#\*]{2,}) [1-9]\d{0,2} ?원? \d{1,2} ([1-9]\d{0,2}) ?원?"
    regex_8 = "([가-힣a-zA-Z\+1-9 \-\(\)\/\~\[\]\.\,\·\&\:\#\*]{2,}) \d{1,2} ([1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3}) ?원?"
    regex_9 = "([가-힣a-zA-Z\+1-9 \-\(\)\/\~\[\]\.\,\·\&\:\#\*]{2,}) \d{1,2} ([1-9]\d{0,2}[,\.]\d{3}) ?원?"
    regex_10 = "([가-힣a-zA-Z\+1-9 \-\(\)\/\~\[\]\.\,\·\&\:\#\*]{2,}) \d{1,2} ([1-9]\d{0,2}) ?원?"
    regex_11 = "(진 ?료 ?비?-?기?본?) ([1-9]\d{0,2}[,\.]\d{3}[,\.]?\d{0,3})"
    regex_12 = "([가-힣a-zA-Z\+1-9 \-\(\)\/\~\[\]\.\,\·\&\:\#\*]{2,}) ([1-9]\d{0,2}[,\.]\d{3}[,\.]\d{3}) \d{1,2} "
    regex_13 = "([가-힣a-zA-Z\+1-9 \-\(\)\/\~\[\]\.\,\·\&\:\#\*]{2,}) ([1-9]\d{0,2}[,\.]\d{3}) \d{1,2} "

    # cost_0 = re.findall(regex_0, data_save)
    # cost.extend(Cost_Maker(cost_0))
    # data_save = Remover(regex_1, data_save)

    cost_1 = re.findall(regex_1, data_save)
    cost.extend(Cost_Maker(cost_1))
    data_save = Remover(regex_1, data_save)

    cost_2 = re.findall(regex_2, data_save)
    cost.extend(Cost_Maker(cost_2))
    data_save = Remover(regex_2, data_save)

    cost_3 = re.findall(regex_3, data_save)
    cost.extend(Cost_Maker(cost_3))
    data_save = Remover(regex_3, data_save)

    cost_4 = re.findall(regex_4, data_save)
    cost.extend(Cost_Maker(cost_4))
    data_save = Remover(regex_4, data_save)

    cost_5 = re.findall(regex_5, data_save)
    cost.extend(Cost_Maker(cost_5))
    data_save = Remover(regex_5, data_save)

    cost_6 = re.findall(regex_6, data_save)
    cost.extend(Cost_Maker(cost_6))
    data_save = Remover(regex_6, data_save)

    cost_7 = re.findall(regex_7, data_save)
    cost.extend(Cost_Maker(cost_7))
    data_save = Remover(regex_7, data_save)

    cost_8 = re.findall(regex_8, data_save)
    cost.extend(Cost_Maker(cost_8))
    data_save = Remover(regex_8, data_save)

    cost_9 = re.findall(regex_9, data_save)
    cost.extend(Cost_Maker(cost_9))
    data_save = Remover(regex_9, data_save)

    cost_10 = re.findall(regex_10, data_save)
    cost.extend(Cost_Maker(cost_10))
    data_save = Remover(regex_10, data_save)

    cost_11 = re.findall(regex_11, data_save)
    cost.extend(Cost_Maker(cost_11))
    data_save = Remover(regex_11, data_save)

    cost_12 = re.findall(regex_12, data_save)
    cost.extend(Cost_Maker(cost_12))
    data_save = Remover(regex_12, data_save)

    cost_13 = re.findall(regex_13, data_save)
    cost.extend(Cost_Maker(cost_13))
    data_save = Remover(regex_13, data_save)

    data_save = re.sub("^ ", "", data_save)
    return data_save, cost


# final_hosp_info.csv 의 동물병원 DB와 비교하여 DB의 정보로 치환
def check_hospital_info(sub_data):
    hospital_info = csv_to_data('./final_hosp_info.csv')
    regi_number = sub_data[0]
    number = re.sub("^0", "", str(sub_data[1]))
    address = sub_data[2]
    hospital_name = sub_data[3]

    if regi_number in hospital_info and regi_number != '':
        try:
            index = np.where(regi_number == hospital_info)
            address = hospital_info[int(index[0])][2]
            hospital_name = hospital_info[int(index[0])][0]
            if number != '':
                pass
            else:
                number = str(0) + str(hospital_info[int(index[0])][1])
            return regi_number, number, address, hospital_name
        except:
            return regi_number, number, address, hospital_name

    elif number in hospital_info and number != '':
        try:
            index = np.where(number == hospital_info)
            address = hospital_info[int(index[0])][2]
            hospital_name = hospital_info[int(index[0])][0]
            if regi_number != '':
                pass
            else:
                regi_number = hospital_info[int(index[0])][3]
            return regi_number, str(sub_data[1]), address, hospital_name
        except:
            return regi_number, number, address, hospital_name

    else:
        return regi_number, number, address, hospital_name


# 리스트의 대문자를 소문자로 치환
def lower(original_list):
    lower_list = []
    for random_word in original_list:
        try:
            lower_word = random_word.lower()
            lower_list.append(lower_word)
        except:
            lower_list.append(random_word)
    return lower_list


# 진단명 데이터와 비교하여 분류안된 항목 검출
def check_removed_data(raw_data):
    with open("Keyword Labeling.json", "r", encoding='UTF-8-sig') as json_raw:
        json_word = json.load(json_raw)
    main_category = json_word['진단명']
    for master_key, main_value in main_category.items():
        word_data = lower([raw_data])
        if any(word in str(word_data) for word in lower(main_value)):
            return False
        else:
            return True

# 키워드 검색
def find_keyword(keyword):
    with open('./Keyword Labeling.json', 'r', encoding='UTF-8-sig') as f:
        json_data = json.load(f)
    main_category = json_data['진단명']
    for key, value in main_category.items():
        for i in value:
            if i in keyword:
                return 1
    return 0


# Cost 데이터 재 필터링
def ReFilterCost(data_saved):
    final = []

    filtering = data_saved.split(" ")
    for index, j in enumerate(filtering):
        price = []
        filtered = []
        result = find_keyword(j)
        if result == 1:
            count = index + 1
            count2 = 0
            while count < len(filtering):
                if count2 == 3:
                    break
                price.append(filtering[count])
                count = count + 1
                count2 = count2 + 1
            price = ' '.join(price)
            regex_0 = "([1-9]\d{0,2}[,\.]\d{3}) ?원? (\d{1,2}[\.]\d{1,2}) ([1-9]\d{0,2}[,\.]\d{3})? ?원?"
            regex_1 = "([1-9]\d{0,2}[,\.]\d{3}) ?원? \d{1,2} ([1-9]\d{0,2}[,\.]\d{3})? ?원?"
            regex_2 = "(\d{1,2}[\.]\d{1,2}) [1-9]\d{0,2}[,\.]\d{3} ?원?"
            regex_3 = "\d{1,2} ([1-9]\d{0,2}[,\.]\d{3}) ?원?"
            regex_4 = "([1-9]\d{0,2}[,\.]\d{3}) ?원?"
            cost_0 = re.findall(regex_0, price)
            filtered.extend(cost_0)
            price = Remover(regex_0, price)
            cost_1 = re.findall(regex_1, price)
            filtered.extend(cost_1)
            price = Remover(regex_1, price)
            cost_2 = re.findall(regex_2, price)
            filtered.extend(cost_2)
            price = Remover(regex_2, price)
            cost_3 = re.findall(regex_3, price)
            filtered.extend(cost_3)
            price = Remover(regex_3, price)
            cost_4 = re.findall(regex_4, price)
            filtered.extend(cost_4)
            price = Remover(regex_4, price)

            final.append(j)
            for i in filtered:
                if (isinstance(i, tuple)):
                    i = list(i)
                    for j in i:
                        final.append(j)
                    continue
                final.append(i)

    for i in final:
        data_saved = re.sub(re.escape(i), "", data_saved)
    return data_saved, final


# cost 표준화
def Cost_verification(cost_data):
    ver_cost = reg.check_disease_single(cost_data)
    return ver_cost


# lambda 로 들어온 event 를 decode 하여 naver clova 로 전송
def event_to_clova(event):
    result = event['body']
    str_decoded = base64.b64decode(result).decode('utf-8')
    decoded = eval(str_decoded)

    clova_api = decoded['clova_api']
    clova_key = decoded['clova_key']
    uuid = decoded['uuid']
    image_route = decoded['image']

    clova_result = naver_clova_reader(clova_api, clova_key, uuid, image_route)

    return clova_result


def main_code(row_data):
    temp = []
    temp1 = []
    temp2 = []
    temp3 = []

    data_saved, trash_check = filtering(row_data)
    data_saved = Remove_Words(data_saved)
    data_saved = OCR_Error_Correction(data_saved)
    data_saved, registration_number = Registration_Number(data_saved)
    try:
        temp.append(registration_number[0])
    except:
        temp.append('')

    # 날짜 데이터 추출
    data_saved, date = Charge_Date(data_saved)

    # 무게 데이터 추출
    data_saved, weight = Weight_Data(data_saved)

    # 동물명 추출
    data_saved, animal_name = Animal_Name(data_saved)

    # 비과세품목
    data_saved, non_texable_item = Non_Texable_item(data_saved)

    # 과세공급가액
    data_saved, texable_item = Texable_item(data_saved)

    # 세금 금액
    data_saved, tex = Tex(data_saved)

    # 전화번호
    data_saved, phone_number = Phone_Number(data_saved)
    try:
        temp.append(phone_number[0])
    except:
        temp.append('')

    # 소계
    data_saved, small_sum = Small_Sum(data_saved)

    # 총계
    data_saved, total_sum = Total_Sum(data_saved)

    # 할인
    data_saved, discount = Discount(data_saved)

    # 주소데이터
    data_saved, address = Address(data_saved)
    try:
        temp.append(address[0])
    except:
        temp.append('')

    # 대표자명
    data_saved, ceo = Ceo(data_saved)

    # 병원명
    data_saved, hospital_name = Hospital_name(data_saved)
    try:
        temp.append(hospital_name[0])
    except:
        temp.append('')

    # 담당자명
    data_saved, manager_name = Manager_name(data_saved)

    # 사업자등록번호, 주소, 전화번호, 병원명 검증 및 새로운 명 반환
    ver_registration_number, ver_phone_number, ver_address, ver_hospital_name = check_hospital_info(temp)
    data_saved, data_removed = receipt_filter(data_saved)

    # cost를 뽑아내기 전 전처리
    data_saved = Text_Whitespace_Text_Editer(data_saved)  # 문자 사이의 공백문자 제거
    data_saved = Too_Many_0_Remover(data_saved)  # 사이사이 너무 많은 숫자 있는 0 0 0 0 0 0 이런거 제거
    data_saved = Remove_Words_2(data_saved)
    data_saved = Error_0_Fixer(data_saved)

    # 금액
    data_saved, cost = Cost(data_saved)
    verified_cost = Cost_verification(cost)

    # 미분류된 진료내역 재필터링
    #data_saved, addition = ReFilterCost(data_saved)
    #cost.extend(addition)

    # 미분류에 진료 항목 확인 유무
    check_result = check_removed_data(data_saved)

    # 첫번째 날짜 가져오기
    date_one = ""
    if len(date) > 0:
        date_one = date[0]

    final_result = {"original": row_data,
                    "receipt_check" : trash_check,
                    "result": {
                        'date': date_one,
                        'weight': list(set(weight)),
                        'animal_name': animal_name,
                        'non_taxable_item': list(set(non_texable_item)),
                        'tax': list(set(tex)),
                        'small_sum': list(set(small_sum)),
                        'total_sum': list(set(total_sum)),
                        'discount': discount,
                        'ceo': ceo,
                        'registration_number': str(ver_registration_number),
                        'phone_number': str(ver_phone_number),
                        'address': str(ver_address),
                        'hospital_name': str(ver_hospital_name),
                        'data_removed': data_removed,
                        'cost': cost,
                        'check_result': check_result},
                    "standardization_result": {
                        'date': list(set(date)),
                        'weight': list(set(weight)),
                        'animal_name': animal_name,
                        'non_taxable_item': list(set(non_texable_item)),
                        'tax': list(set(tex)),
                        'small_sum': list(set(small_sum)),
                        'total_sum': list(set(total_sum)),
                        'discount': discount,
                        'ceo': ceo,
                        'registration_number': str(ver_registration_number),
                        'phone_number': str(ver_phone_number),
                        'address': str(ver_address),
                        'hospital_name': str(ver_hospital_name),
                        'data_removed': data_removed,
                        'cost': verified_cost,
                        'check_result': check_result}
                    }

    return final_result

