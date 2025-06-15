# 🔄 HEIC 이미지 변환기 v1.0

> **간단하고 안정적인 HEIC → JPEG/PNG/WEBP 변환 도구**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-3.0-red.svg)

## ✨ 주요 특징

### 🎯 **심플한 사용법**
- **3단계 변환**: 폴더 선택 → 설정 → 변환 완료
- **직관적 인터페이스**: 복잡한 설정 없이 바로 사용 가능
- **실시간 미리보기**: 선택한 이미지 즉시 확인
- **진행률 표시**: 변환 상태를 한눈에 파악

### 🚀 **안정적 성능**
- **배치 처리**: 여러 파일 동시 변환
- **원본 보존**: 원본 파일은 절대 변경하지 않음
- **오류 복구**: 일부 파일 실패 시에도 나머지 파일 계속 처리
- **메모리 최적화**: 안정적인 메모리 사용

### 🖼️ **다양한 형식 지원**
- **입력**: HEIC, HEIF 형식
- **출력**: JPEG, PNG, WEBP 형식
- **품질 조정**: 50% ~ 100% 품질 설정
- **메타데이터 보존**: EXIF 정보 유지

## 📥 설치 방법

### 방법 1: 실행 파일 다운로드 (추천)

**Windows 사용자:**
1. [Releases 페이지](https://github.com/lksee/heic-converter/releases)에서 `HEIC변환기-v1.0-Windows.exe` 다운로드
2. 다운로드한 파일을 실행
3. Python 설치 불필요!


### 방법 2: 소스코드 실행

```bash
# 1. 저장소 클론
git clone https://github.com/lksee/heic-converter.git
cd heic-converter

# 2. Python 가상환경 생성 (권장)
python -m venv heic_env

# Windows
heic_env\Scripts\activate

# macOS/Linux
source heic_env/bin/activate

# 3. 필수 패키지 설치
pip install -r requirements.txt

# 4. 프로그램 실행
python heic_converter.py
```

## 🚀 사용 방법

### 📖 기본 사용법

#### 1단계: 폴더 선택
- "HEIC 파일 폴더 선택" 버튼 클릭
- HEIC 파일이 들어있는 폴더 선택
- 자동으로 HEIC 파일들을 찾아서 목록 표시

#### 2단계: 설정 조정
- **출력 형식**: JPEG, PNG, WEBP 중 선택
- **품질 설정**: 슬라이더로 50%~100% 조정
- **미리보기**: 파일 목록에서 이미지 선택하여 확인

#### 3단계: 변환 실행
- "변환 시작" 버튼 클릭
- 진행률 바로 변환 상태 확인
- 완료 후 "결과 폴더 열기"로 변환된 파일 확인

### 🎛️ 설정 가이드

#### 출력 형식별 특징

| 형식 | 특징 | 추천 용도 |
|------|------|-----------|
| **JPEG** | 작은 파일 크기, 손실 압축 | 일반적인 사진, 웹 업로드 |
| **PNG** | 무손실 압축, 투명도 지원 | 스크린샷, 그래픽 |
| **WEBP** | 최신 형식, 효율적 압축 | 웹사이트, 모던 브라우저 |

#### 품질 설정 가이드

| 품질 | 용도 | 파일 크기 |
|------|------|-----------|
| **50-70%** | SNS 업로드, 웹용 | 가장 작음 |
| **80-90%** | 일반 사용, 공유용 | 보통 |
| **95-100%** | 인쇄용, 보관용 | 큼 |

## 📋 시스템 요구사항

### 최소 요구사항
- **OS**: Windows 10/11
- **RAM**: 2GB 이상
- **저장공간**: 50MB (프로그램) + 변환할 파일 크기의 2배
- **Python**: 3.8 이상 (소스코드 실행 시)

### 권장 요구사항
- **RAM**: 4GB 이상
- **저장공간**: 변환할 파일 크기의 3배
- **CPU**: 듀얼코어 이상

## 🔧 문제 해결

### 자주 발생하는 문제

#### ❌ "HEIC 파일을 열 수 없습니다"
**원인**: pillow-heif 모듈 문제
**해결법**:
```bash
pip uninstall pillow-heif
pip install pillow-heif
```

#### ❌ "변환 속도가 너무 느려요"
**해결법**:
- 품질을 80% 이하로 낮추기
- JPEG 형식 사용
- 한 번에 변환하는 파일 수 줄이기

#### ❌ "프로그램이 갑자기 종료됩니다"
**원인**: 메모리 부족 또는 손상된 HEIC 파일
**해결법**:
- 다른 파일들로 테스트
- 프로그램 재시작
- 시스템 재부팅

#### ❌ Windows에서 "바이러스 경고"
**원인**: 디지털 서명이 없는 실행 파일
**해결법**:
- Windows Defender에서 예외 추가
- 또는 소스코드로 직접 실행

### 성능 최적화 팁

#### 🚀 빠른 변환
```
✅ JPEG 형식 선택
✅ 품질 70-80% 설정
✅ 한 번에 50개 이하 파일 처리
```

#### 🎨 최고 품질
```
✅ PNG 또는 WEBP 형식
✅ 품질 95-100% 설정
✅ 충분한 저장 공간 확보
```

## 📊 지원되는 파일 형식

### 입력 형식
- ✅ `.heic` - Apple HEIC 형식
- ✅ `.heif` - HEIF 표준 형식
- ✅ `.HEIC` - 대문자 확장자
- ✅ `.HEIF` - 대문자 확장자

### 출력 형식
- ✅ **JPEG** (`.jpg`) - 호환성 최고
- ✅ **PNG** (`.png`) - 무손실 압축
- ✅ **WEBP** (`.webp`) - 차세대 형식

## 🔒 개인정보 보호

### 완전한 로컬 처리
- ✅ **오프라인 동작**: 인터넷 연결 불필요
- ✅ **데이터 보호**: 모든 처리가 컴퓨터에서만 실행
- ✅ **원본 보존**: 원본 파일은 절대 수정하지 않음
- ✅ **메타데이터 유지**: EXIF 정보 보존 (선택사항)

### 보안 기능
- 🔒 개인 정보가 외부로 전송되지 않음
- 🔒 변환 과정에서 임시 파일 자동 삭제
- 🔒 GPS 정보 등 민감한 데이터 선택적 제거 가능

## 📚 FAQ (자주 묻는 질문)

### Q: HEIC가 뭔가요?
A: Apple이 iPhone에서 사용하는 고효율 이미지 형식입니다. 같은 품질에서 JPEG보다 파일 크기가 약 50% 작습니다.

### Q: 변환하면 화질이 떨어지나요?
A: 품질을 90% 이상으로 설정하면 육안으로 구별하기 어려울 정도로 고품질을 유지합니다.

### Q: 한 번에 몇 개까지 변환할 수 있나요?
A: 이론상 제한은 없지만, 안정성을 위해 한 번에 100개 이하를 권장합니다.

### Q: 변환 속도는 어느 정도인가요?
A: 일반적인 iPhone 사진(12MP) 기준으로 파일당 1-2초 정도 소요됩니다.

### Q: 원본 파일이 삭제되나요?
A: 절대로 삭제되지 않습니다. 변환된 파일은 새로운 폴더에 저장됩니다.

## 📈 업데이트 내역

### v1.0 (현재 버전)
- ✅ 안정적인 UI 디자인
- ✅ 향상된 오류 처리
- ✅ 메모리 사용량 최적화
- ✅ 크로스 플랫폼 호환성 개선


## 🤝 지원 및 기여

### 버그 신고
이슈를 발견하셨다면:
1. [GitHub Issues](https://github.com/lksee/heic-converter/issues) 방문
2. 상세한 오류 내용과 스크린샷 첨부
3. 운영체제와 Python 버전 명시

### 기능 제안
새로운 기능 아이디어가 있으시면 언제든 GitHub Issues에 제안해주세요!

### 개발 참여
1. 저장소 Fork
2. 기능 브랜치 생성
3. 변경사항 구현
4. Pull Request 제출

## 📄 라이선스

이 프로젝트는 **MIT 라이선스** 하에 배포됩니다.
- ✅ 상업적 사용 가능
- ✅ 수정 및 배포 자유
- ✅ 사용료 없음

자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🙏 감사의 말

### 오픈소스 라이브러리
- **[Pillow](https://python-pillow.org/)** - 이미지 처리 엔진
- **[pillow-heif](https://github.com/bigcat88/pillow_heif)** - HEIC 형식 지원
- **[tkinter](https://docs.python.org/3/library/tkinter.html)** - GUI 프레임워크

### 커뮤니티
- 모든 사용자들의 피드백과 버그 리포트
- 베타 테스터들의 소중한 의견
- 오픈소스 커뮤니티의 지원

## 📞 연락처

### 개발자 정보
- **GitHub**: [lksee](https://github.com/lksee)
- **이메일**: bdwrtr@naver.com

### 프로젝트 링크
- **저장소**: [GitHub Repository](https://github.com/lksee/heic-converter)
- **릴리즈**: [Download Page](https://github.com/lksee/heic-converter/releases)

---

<div align="center">

**⭐ 이 프로젝트가 도움이 되셨다면 Star를 눌러주세요! ⭐**

Made with ❤️ for everyone who struggles with HEIC files

</div>

### 사용 시나리오

#### 시나리오 1: iPhone 사진 정리
1. iPhone에서 AirDrop으로 PC에 사진 전송
2. HEIC 변환기로 JPEG 변환 (품질 85%)
3. Google Photos나 클라우드에 업로드

#### 시나리오 2: 웹사이트용 이미지 준비
1. HEIC 사진을 WEBP로 변환 (품질 75%)
2. 파일 크기를 50% 이상 절약
3. 웹사이트 로딩 속도 향상

#### 시나리오 3: 인쇄용 고품질 변환
1. PNG 형식 선택 (무손실)
2. 품질 100% 설정
3. 인쇄소에 고품질 파일 제공

---

**🎯 v1.0은 안정성과 사용 편의성에 중점을 둔 버전입니다. 복잡한 설정 없이도 누구나 쉽게 HEIC 파일을 변환할 수 있습니다!**