# dicom2npy
- dicom(`.dcm`) 형태의 CT 이미지를 파이썬에서 열고, 시각화하는 툴킷

## 사용법
### 깃 클론 & 데이터셋 배치
- 본 리포지토리를 다운받고, 하위에 dataset 경로를 만듭니다.
```
git clone https://github.com/skyil7/dicom2npy
cd dicom2npy

mkdir dataset
```

### Poetry 설치 및 실행 (없는 경우)
- [poetry 메뉴얼](https://python-poetry.org/docs/)을 참고하여 설치합니다.
- 아래 명령어로 가상환경을 실행합니다.
```
poetry shell
```

### 뷰어 실행
- streamlit 기반의 뷰어를 실행합니다.
```
streamlit run run_viewer.py
```

### 참고자료
- https://89douner.tistory.com/257

