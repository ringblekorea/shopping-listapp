# 🛒 쇼핑 리스트 앱

순수 HTML/CSS/JavaScript로 만든 간단한 쇼핑 리스트 웹 앱입니다. 별도의 빌드나 서버 없이 브라우저에서 바로 실행됩니다.

## 기능

- 항목 추가 (버튼 클릭 또는 Enter 키)
- 체크박스로 완료 표시 (취소선 처리)
- 항목 개별 삭제
- 완료된 항목 한번에 비우기
- 남은 항목 개수 표시
- `localStorage`를 이용한 데이터 영구 저장 (새로고침해도 유지)
- 빈 입력 무시 처리

## 사용 방법

`index.html` 파일을 브라우저에서 열기만 하면 됩니다.

## 테스트

Playwright 기반 UI 자동화 테스트가 포함되어 있습니다.

```bash
pip install playwright
playwright install chromium
python test_shopping_list.py
```

추가 / 체크 / 삭제 / 새로고침 후 유지 / 완료 항목 비우기 등의 동작을 검증합니다.
