
#My Trade

##Task Breakdown
- myTrade.exe 프로그램을 실행시킬 수 있다.
    - [ ] py프로그램을 exe로 변환할 수 있다. py2exe
- 로그인 버튼을 누르고 로그인 한다.
    - [x] 키움증권 ocx를 연결한다.
    - [x] 로그인 버튼을 만들고 로그인을 처리한다.
- 국내 종합주가지수와 등락폭을 확인한다.
    - [x] 로그인 후 처리 이벤트에 항목 삽입한다.
    - [x] 종합 주가지수와 등락폭을 얻어와 기본정보창에 보여준다.
- 나스탁의 종합주가지수와 등락폭을 확인한다.
    - [x] 로그인 후 처리 이벤트에 항목 삽입한다.
    - [x] 나스탁의 종합주가지수와 등락폭을 확인하여 기본정보창에 보여준다.
- 주식 정보를 조회할 수 있다.
    - [x] 모든 주식명을 볼 수 있다.
    - [x] 주식명을 입력하여 일치되는 주식을 검색할 수 있다.
    - [x] 검색된 주식명의 현재가와 등락폭을 알 수 있다.
- 시스템 메시지를 볼 수 있다.
    - [x] 로그 출력창을 통해 시스템 메시지를 볼 수 있다.
- 주식을 매수할 수 있다.    
    - [x] 선택된 주식을 수량으로 매수할 수 있다.
    - [x] 선택된 주식을 금액으로 매수할 수 있다.
- 주식을 매도할 수 있다.
    - [x] 보유 주식을 확인할 수 있다.
    - [x] 보유 주식의 현재가와 등락폭과 수익률과 수익금액을 알 수 있다.
    - [x] 보유 주식을 선택하여 수량으로 매도할 수 있다.
    - [x] 보유 주식을 선택하여 금액으로 매도할 수 있다. 
- 내 정보에서 보유 현금, 보유 주식수량, 보유 주식수량의 현재 가치를 알 수 있다.
    - [ ] 로그인 후 처리 이벤트에 항목 삽입
    - [x] 내 정보를 조회하여 보유현금을 보여준다
    - [x] 내 정보를 조회하여 보유주식수량을 보여준다     
    - [x] 보유 주식수량을 현금으로 환산하여 보여준다
    - [x] 보유 주식수량 현금 가치액을 보유 현금과 합산하여 총 자산가치를 보여준다.
- 내 정보에서 현재 예약한 주문들을 확인할 수 있다.
    - [ ] 현재 예약된 주문을 확인하여 보여준다.
- 이전에 예약한 매도 주문과 매수주문이 체결됐음을 확인한다.
    - [ ] 예약한 주문이 존재하는지 확인하고 체결여부를 확인하여 보여준다.
    - [ ] 체결된 것을 확인할 수 있을까?
- 주가를 예상하여 매수, 매도를 예약한다.
    - [ ] 시장이 열리지 않은 상태에서도 예약 주문을 할 수 있을까?
    - [ ] 금액의 %를 기준으로 예약 주문을 할 수 있다.
    - [ ] 금액을 기준으로 예약 주문을 할 수 있다.
- 매수 매도가 예약되었다는 알림을 확인한다.
    - [ ] 예약의 성공 여부를 확인할 수 있다.
- 실행 도중 매수, 매도가 완료됐다고 알림을 확인한다.
    - [ ] 키움증권으로부터 이벤트를 받아 알림을 보여준다.
- 디버그 유틸
    - [x] 분리된 로그 창을 볼 수 있다.