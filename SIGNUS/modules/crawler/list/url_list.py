#URL 리스트 모음
#'url' : 게시판url, 별값, 'info' : 게시판정보, 'title_tag' : 검색속도를 빠르게하기 위한 게시판 대표 태그, 'login' : 비로그인에도 볼 수 있으면 0
#																											   로그인 해야만 볼 수 있으면 1

List = (\
	#세종대 메인 게시판 "sj1_main_..."
	#0
	{'url': "https://home.sejong.ac.kr/bbs/bbslist.do?bbsid=1896&wslID=swc&page=1&currentPage=",\
	'info': "sj1_main_founded",\
	'title_tag' : ["교내", "소식"], 'login' : 0},\
	#1
	{'url': "http://board.sejong.ac.kr/boardlist.do?searchField=ALL&searchLowItem=ALL&bbsConfigFK=333&siteGubun=19&menuGubun=1&currentPage=",\
	'info': "sj1_main_notice",\
	'title_tag' : ["교내", "공지"], 'login' : 0},\
	#2
	{'url': "http://board.sejong.ac.kr/boardlist.do?searchField=ALL&searchLowItem=ALL&bbsConfigFK=334&siteGubun=19&menuGubun=1&currentPage=",\
	'info': "sj1_main_entrance",\
	'title_tag' : ["교내", "입학"], 'login' : 0},\
	#3
	{'url': "http://board.sejong.ac.kr/boardlist.do?searchField=ALL&searchLowItem=ALL&bbsConfigFK=335&siteGubun=19&menuGubun=1&currentPage=",\
	'info': "sj1_main_student",\
	'title_tag' : ["교내", "학사", "공지"], 'login' : 0},\
	#4
	{'url': "http://board.sejong.ac.kr/boardlist.do?searchField=ALL&searchLowItem=ALL&bbsConfigFK=337&siteGubun=19&menuGubun=1&currentPage=",\
	'info': "sj1_main_job",\
	'title_tag' : ["교내", "취업&진로"], 'login' : 0},\
	#5
	{'url': "http://board.sejong.ac.kr/boardlist.do?searchField=ALL&searchLowItem=ALL&bbsConfigFK=338&siteGubun=19&menuGubun=1&currentPage=",\
	'info': "sj1_main_schoiarship",\
	'title_tag' : ["교내", "장학"], 'login' : 0},\
	#6
	{'url': "http://board.sejong.ac.kr/boardlist.do?searchField=ALL&searchLowItem=ALL&bbsConfigFK=339&siteGubun=19&menuGubun=1&currentPage=",\
	'info': "sj1_main_college",\
	'title_tag' : ["교내", "알바&구인"], 'login' : 0},\
	#7
	{'url': "http://board.sejong.ac.kr/boardlist.do?searchField=ALL&searchLowItem=ALL&bbsConfigFK=340&siteGubun=19&menuGubun=1&currentPage=",\
	'info': "sj1_main_bidding",\
	'title_tag' : ["교내", "입찰"], 'login' : 0},\
	#8
	{'url': "http://board.sejong.ac.kr/boardlist.do?searchField=ALL&searchLowItem=ALL&bbsConfigFK=353&siteGubun=19&menuGubun=1&currentPage=",\
	'info': "sj1_main_dataprocessFAQ",\
	'title_tag' : ["교내", "FAQ"], 'login' : 0},\
	#9
	{'url': "http://board.sejong.ac.kr/boardlist.do?searchField=ALL&searchLowItem=ALL&bbsConfigFK=697&siteGubun=19&menuGubun=1&currentPage=",\
	'info': "sj1_main_studentFAQ",\
	'title_tag' : ["교내", "FAQ"], 'login' : 0},\
	#10
	{'url': "http://board.sejong.ac.kr/boardlist.do?searchField=ALL&searchLowItem=ALL&bbsConfigFK=698&siteGubun=19&menuGubun=1&currentPage=",\
	'info': "sj1_main_schoiarshipFAQ",\
	'title_tag' : ["교내", "FAQ"], 'login' : 0},\
	#11
	{'url': "http://board.sejong.ac.kr/boardlist.do?searchField=ALL&searchLowItem=ALL&bbsConfigFK=699&siteGubun=19&menuGubun=1&currentPage=",\
	'info': "sj1_main_foreignerFAQ",\
	'title_tag' : ["교내", "국제", "FAQ"], 'login' : 0},\
	#12
	{'url': "http://board.sejong.ac.kr/boardlist.do?searchField=ALL&searchLowItem=ALL&bbsConfigFK=674&siteGubun=19&menuGubun=1&currentPage=",\
	'info': "sj1_main_foreignernotice",\
	'title_tag' : ["교내", "국제", "공지"], 'login' : 0},\
	#세종대 학생경력개발시스템 공지 "sj2_..."
	#13
	{'url': "http://udream.sejong.ac.kr/Community/Notice/NoticeList.aspx?rp=",\
	'post_url': "https://udream.sejong.ac.kr/Community/Notice/NoticeView.aspx?nnum=",\
	'info': "sj2_udream_notice",\
	'title_tag' : ["취업&진로"], 'login' : 1},\
	#세종대 학생경력개발시스템 채용정보 "sj3_..."
	#14
	{'url': "https://udream.sejong.ac.kr/Recruit/RecruitList.aspx?rp=",\
	'post_url': "https://udream.sejong.ac.kr/Recruit/RecruitView.aspx?rcdx=",\
	'info': "sj3_udream_jobinfo",\
	'title_tag' : ["취업&진로"], 'login' : 1},\
	#세종대 학생경력개발시스템 공채속보 "sj4_..."
	#15
	{'url': "http://udream.sejong.ac.kr/WorkCenter/WorkRecruit.aspx?rp=",\
	'info': "sj4_udream_workinfo",\
	'title_tag' : ["취업&진로"], 'login' : 1},\
	#세종대 학생경력개발시스템 청년인턴 "sj5_..."
	#16
	{'url': "http://udream.sejong.ac.kr/WorkCenter/WorkIntern.aspx?rp=",\
	'post_url': "https://www.work.go.kr/youngtomorrow/emp/internEmpInfoDetail.do?wantedAuthNo=",\
	'info': "sj5_udream_workyoung",\
	'title_tag' : ["취업&진로"], 'login' : 1},\
	#세종대학교 학술정보원 "sj6_library_..."
	#17
	{'url': "http://library.sejong.ac.kr/bbs/Bbs.ax?bbsID=1&pageSize=10&currentPage=",\
	'info': "sj6_library_notice",\
	'title_tag' : ["교내", "학술정보원", "공지"], 'login' : 0},\
	#18
	{'url': "http://library.sejong.ac.kr/bbs/Bbs.ax?bbsID=2&pageSize=10&currentPage=",\
	'info': "sj6_library_book",\
	'title_tag' : ["교내", "학술정보원", "도서"], 'login' : 0},\
	#19
	{'url': "http://library.sejong.ac.kr/bbs/Bbs.ax?bbsID=3&pageSize=10&currentPage=",\
	'info': "sj6_library_FAQ",\
	'title_tag' : ["교내", "학술정보원", "FAQ"], 'login' : 0},\
	#세종대 홍보원 "sj7_promotion_..."
	#20
	{'url': "http://www.sejongpr.ac.kr/sejongnewspaperlist.do?currentPage=",\
	'info': "sj7_promotion_article",\
	'title_tag' : ["교내", "홍보원", "소식"], 'login' : 0},\
	#21
	{'url': "http://www.sejongpr.ac.kr/sejongnewspaperlist.do?boardType=2&currentPage=",\
	'info': "sj7_promotion_prism",\
	'title_tag' : ["교내", "홍보원", "소식"], 'login' : 0},\
	#22
	{'url': "http://www.sejongpr.ac.kr/sejongnewspaperlist.do?boardType=4&currentPage=",\
	'info': "sj7_promotion_report",\
	'title_tag' : ["교내", "홍보원", "소식"], 'login' : 0},\
	#23
	{'url': "http://www.sejongpr.ac.kr/sejongnewspaperlist.do?boardType=3&currentPage=",\
	'post_url': "http://www.sejongpr.ac.kr/sejongnewspaperview.do?currentPage=1boardType=3&pkid=",\
	'info': "sj7_promotion_research",\
	'title_tag' : ["교내", "홍보원", "연구"], 'login' : 0},\
	#24
	{'url': "http://www.sejongpr.ac.kr/sejongnewspaperlist.do?boardType=26&currentPage=",\
	'info': "sj7_promotion_speech",\
	'title_tag' : ["교내", "홍보원", "세미나", "행사", "취업&진로"], 'login' : 0},\
	#세종대 홍보원 언론게시판 "sj8_promotion_media"
	#25
	{'url': "http://www.sejongpr.ac.kr/sejongnewspaperlist.do?boardType=5&currentPage=",\
	'info': "sj8_promotion_media",\
	'title_tag' : ["홍보원", "소식"], 'login' : 0},\
	#세종대 학과사이트
	#26 :::: 중국통상학과
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?bbsid=1045&wslID=cndpt&currentPage=",\
	'info': "sj9_chinatrade_notice",\
	'title_tag' : ["교내", "중국통상학과", "공지"], 'login' : 0},\
	#27
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?bbsid=781&wslID=cndpt&currentPage=",\
	'info': "sj9_chinatrade_job",\
	'title_tag' : ["교내", "중국통상학과", "취업&진로"], 'login' : 0},\
	#28 :::: 역사학과
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=517&wslID=histdpt&currentPage=",\
	'info': "sj9_history_notice",\
	'title_tag' : ["교내", "역사학과", "공지"], 'login' : 0},\
	#29
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=521&wslID=histdpt&currentPage=",\
	'info': "sj9_history_data",\
	'title_tag' : ["교내", "역사학과"], 'login' : 0},\
	#30 :::: 경제통신학과
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=443&wslID=entdpt&currentPage=",\
	'info': "sj9_ecotrade_notice",\
	'title_tag' : ["교내", "경제통상학과", "공지"], 'login' : 0},\
	#31
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=445&wslID=entdpt&currentPage=",\
	'info': "sj9_ecotrade_event",\
	'title_tag' : ["교내", "경제통상학과", "행사"], 'login' : 0},\
	#32
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=687&wslID=admdpt&currentPage=",\
	'info': "sj9_administ_notice",\
	'title_tag' : ["교내", "행정학과", "공지"], 'login' : 0},\
	#33
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=1086&wslID=mnadpt&currentPage=",\
	'info': "sj9_management_notice",\
	'title_tag' : ["교내", "경영학부", "공지"], 'login' : 0},\
	#34
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=1182&wslID=mnadpt&currentPage=",\
	'info': "sj9_management_job",\
	'title_tag' : ["교내", "경영학과", "취업&진로"], 'login' : 0},\
	#35
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=1731&wslID=hoteldpt&currentPage=",\
	'info': "sj9_hotel_notice",\
	'title_tag' : ["교내", "호텔관광대학", "공지"], 'login' : 0},\
	#36
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=1126&wslID=digitdpt&currentPage=",\
	'info': "sj9_software_notice",\
	'title_tag' : ["교내", "소프트웨어학과", "공지"], 'login' : 0},\
	#37
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=1236&wslID=electrodpt&currentPage=",\
	'info': "sj9_elecommunication_notice",\
	'title_tag' : ["교내", "전자정보통신공학과", "공지"], 'login' : 0},\
	#38
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=1425&wslID=electrodpt&currentPage=",\
	'info': "sj9_elecommunication_data",\
	'title_tag' : ["교내", "전자정보통신공학과"], 'login' : 0},\
	#39
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=571&wslID=isdpt&currentPage=",\
	'info': "sj9_infoprotection_notice",\
	'title_tag' : ["교내", "정보보호학과", "공지"], 'login' : 0},\
	#40
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=575&wslID=isdpt&currentPage=",\
	'info': "sj9_infoprotection_job",\
	'title_tag' : ["교내", "정보보호학과", "취업&진로"], 'login' : 0},\
	#41
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=665&wslID=energydpt&currentPage=",\
	'info': "sj9_energy_notice",\
	'title_tag' : ["교내", "에너지자원공학과", "공지"], 'login' : 0},\
	#42
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=1601&wslID=nanodpt&currentPage=",\
	'info': "sj9_nano_notice",\
	'title_tag' : ["교내", "나노신소재공학과", "공지"], 'login' : 0},\
	#43
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=619&wslID=nanodpt&currentPage=",\
	'info': "sj9_nano_job",\
	'title_tag' : ["교내", "나노신소재공학과", "취업&진로"], 'login' : 0},\
	#44
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=681&wslID=nanodpt&currentPage=",\
	'info': "sj9_nano_FAQ",\
	'title_tag' : ["교내", "나노신소재공학과", "FAQ"], 'login' : 0},\
	#45
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=1629&wslID=dsedpt&currentPage=",\
	'info': "sj9_defensesys_notice",\
	'title_tag' : ["교내", "국방시스템공학과", "공지"], 'login' : 0},\
	#46
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=1375&wslID=iddpt&currentPage=",\
	'info': "sj9_indusdesign_notice",\
	'title_tag' : ["교내", "산업디자인학과", "공지"], 'login' : 0},\
	#47
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=525&wslID=iddpt&currentPage=",\
	'info': "sj9_indusdesign_data",\
	'title_tag' : ["교내", "산업디자인학과"], 'login' : 0},\
	#48
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=1371&wslID=design&currentPage=",\
	'info': "sj9_designinnovation_studentnotice",\
	'title_tag' : ["교내", "디자인이노베이션", "공지", "학사"], 'login' : 0},\
	#49
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=1822&wslID=design&currentPage=",\
	'info': "sj9_designinnovation_notice",\
	'title_tag' : ["교내", "디자인이노베이션", "공지"], 'login' : 0},\
	#50
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=1373&wslID=design&currentPage=",\
	'info': "sj9_designinnovation_data",\
	'title_tag' : ["교내", "디자인이노베이션"], 'login' : 0},\
	#51
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=1401&wslID=anitec&currentPage=",\
	'info': "sj9_animation_notice",\
	'title_tag' : ["교내", "만화애니메이션학과", "공지"], 'login' : 0},\
	#52
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=641&wslID=pedpt&currentPage=",\
	'info': "sj9_pysical_notice",\
	'title_tag' : ["교내", "체육학과", "공지"], 'login' : 0},\
	#53
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=645&wslID=pedpt&currentPage=",\
	'info': "sj9_pysical_job",\
	'title_tag' : ["교내", "체육학과", "취업&진로"], 'login' : 0},\
	#54
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=1318&wslID=dancedpt&currentPage=",\
	'info': "sj9_dance_notice",\
	'title_tag' : ["교내", "무용학과", "공지"], 'login' : 0},\
	#55
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=1320&wslID=dancedpt&currentPage=",\
	'info': "sj9_dance_event",\
	'title_tag' : ["교내", "무용학과", "행사"], 'login' : 0},\
	#56
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?&bbsid=1035&wslID=openmajor&currentPage=",\
	'info': "sj9_law_notice",\
	'title_tag' : ["교내", "법학부", "공지"], 'login' : 0},\
	#세종대학교 물리학과 홈페이지 [sj10_pysics_notice]
	#57
	{'url': "http://physics.sejong.ac.kr/bbs/zboard.php?id=news_notice&page=",\
	'info': "sj10_pysics_notice",\
	'title_tag' : ["교내", "물리학과", "공지"], 'login' : 0},\
	#세종대학교 일어일문
	# 학과 홈페이지 [sj11_japanese_notice]
	#58
	{'url': "http://japan.sejong.ac.kr/index.php?mid=dpt_notice&page=",\
	'info': "sj11_japanese_notice",\
	'title_tag' : ["교내", "일어일문학과", "공지"], 'login' : 0},\
	#세종대학교 건축학과 홈페이지 [sj12_archi_...]
	#59
	{'url': "http://arch.sejong.ac.kr/events/notice",\
	'info': "sj12_archi_notice",\
	'title_tag' : ["교내", "건축학과", "공지/"], 'login' : 0},\
	#60
	{'url': "http://arch.sejong.ac.kr/events/news",\
	'info': "sj12_archi_news",\
	'title_tag' : ["교내", "건축학과", "소식"], 'login' : 0},\
	#세종대학교 컴퓨터공학과 홈페이지 [sj13_computer_...]
	#61
	{'url': "http://ce.sejong.ac.kr/index.php?mid=itinformation&page=",\
	'info': "sj13_computer_notice",\
	'title_tag' : ["교내", "컴퓨터공학과", "공지"], 'login' : 0},\
	#62
	{'url': "http://ce.sejong.ac.kr/index.php?mid=contest&page=",\
	'info': "sj13_computer_event",\
	'title_tag' : ["교내", "컴퓨터공학과", "공모전&대외활동"], 'login' : 0},\
	#63
	{'url': "http://ce.sejong.ac.kr/index.php?mid=job&page=",\
	'info': "sj13_computer_job",\
	'title_tag' : ["교내", "컴퓨터공학과", "취업&진로"], 'login' : 0},\
	#세종대학교 지능기전공학부 홈페이지 [sj14_imc_...]
	#64
	{'url': "http://imc.sejong.ac.kr/bbs_shop/list.htm?&board_code=notice&page=",\
	'info': "sj14_imc_notice",\
	'title_tag' : ["교내", "지능기전공학부", "공지"], 'login' : 0},\
	#65
	{'url': "http://imc.sejong.ac.kr/bbs_shop/list.htm?&board_code=news&page=",\
	'info': "sj14_imc_news",\
	'title_tag' : ["교내", "지능기전공학부", "소식"], 'login' : 0},\
	#66
	{'url': "http://imc.sejong.ac.kr/bbs_shop/list.htm?&board_code=class&page=",\
	'info': "sj14_imc_student",\
	'title_tag' : ["교내", "지능기전공학부", "학사"], 'login' : 0},\
	#세종대학교 대양휴머니티칼리지 [sj15_classic_...]
	#67
	{'url': "http://board.sejong.ac.kr/boardlist.do?bbsConfigFK=806&searchLowItem=&currentPage=",\
	'info': "sj15_classic_notice",\
	'title_tag' : ["교내", "대양휴머니티칼리지", "공지"], 'login' : 0},\
	#68
	{'url': "http://board.sejong.ac.kr/boardlist.do?bbsConfigFK=807&searchLowItem=&currentPage=",\
	'info': "sj15_classic_news",\
	'title_tag' : ["교내", "대양휴머니티칼리지", "소식"], 'login' : 0},\
	#69
	{'url': "http://board.sejong.ac.kr/boardlist.do?bbsConfigFK=804&searchLowItem=&currentPage=",\
	'info': "sj15_classic_creative",\
	'title_tag' : ["교내", "대양휴머니티칼리지", "창의학기제"], 'login' : 0},\
	#70
	{'url': "http://board.sejong.ac.kr/boardlist.do?bbsConfigFK=810&searchLowItem=&currentPage=",\
	'info': "sj15_classic_event",\
	'title_tag' : ["교내", "대양휴머니티칼리지", "공모전&대외활동", "행사"], 'login' : 0},\
	#71
	{'url': "http://board.sejong.ac.kr/boardlist.do?bbsConfigFK=805&searchLowItem=&currentPage=",\
	'info': "sj15_classic_shp",\
	'title_tag' : ["교내", "대양휴머니티칼리지", "SHP"], 'login' : 0},\
	#네이버카페 [sj16_..._...]
	#72
	{'url': "https://cafe.naver.com/ArticleList.nhn?search.clubid=24196743&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=",\
	'info': "sj16_navercafe_foreigner",\
	'title_tag' : ["네이버카페", "국제", "교환학생"], 'login' : 0},\
	#73
	{'url': "https://cafe.naver.com/ArticleList.nhn?search.clubid=27389285&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=",\
	'info': "sj16_navercafe_music",\
	'title_tag' : ["네이버카페", "음악과"], 'login' : 0},\
	#74
	{'url': "https://cafe.naver.com/ArticleList.nhn?search.clubid=27460434&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=",\
	'info': "sj16_navercafe_animation",\
	'title_tag' : ["네이버카페", "만화애니메이션학과"], 'login' : 0},\
	#75
	{'url': "https://cafe.naver.com/ArticleList.nhn?search.clubid=26913200&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=",\
	'info': "sj16_navercafe_math",\
	'title_tag' : ["네이버카페", "수학통계학부"], 'login' : 0},\
	#76
	{'url': "https://cafe.naver.com/ArticleList.nhn?search.clubid=25399964&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=",\
	'info': "sj16_navercafe_korean",\
	'title_tag' : ["네이버카페", "국어국문학과"], 'login' : 0},\
	#77
	{'url': "https://cafe.naver.com/ArticleList.nhn?search.clubid=26106419&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=",\
	'info': "sj16_navercafe_environmentenergy",\
	'title_tag' : ["네이버카페", "환경에너지공간융합학과"], 'login' : 0},\
	#78
	{'url': "https://cafe.naver.com/ArticleList.nhn?search.clubid=27933276&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=",\
	'info': "sj16_navercafe_chemistry",\
	'title_tag' : ["네이버카페", "화학과"], 'login' : 0},\
	#79
	{'url': "https://cafe.naver.com/ArticleList.nhn?search.clubid=25721790&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=",\
	'info': "sj16_navercafe_sjnanuri",\
	'title_tag' : ["네이버카페", "세종나누리", "봉사"], 'login' : 0},\
	#80
	{'url': "https://cafe.naver.com/ArticleList.nhn?search.clubid=28918157&search.boardtype=L&search.questionTab=A&search.totalCount=103&search.page=",\
	'info': "sj16_navercafe_eleinfoengineer",\
	'title_tag' : ["네이버카페", "전자정보공학대학"], 'login' : 0},\
	#81
	{'url': "https://cafe.naver.com/ArticleList.nhn?search.clubid=29017374&search.boardtype=L&search.questionTab=A&search.totalCount=52&search.page=",\
	'info': "sj16_navercafe_imc",\
	'title_tag' : ["네이버카페", "지능기전공학부"], 'login' : 0},\
	#82
	{'url': "https://cafe.naver.com/ArticleList.nhn?search.clubid=28987205&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=",\
	'info': "sj16_navercafe_club",\
	'title_tag' : ["네이버카페", "동아리&모임", "UNSA"], 'login' : 0},\
	#학생생활상담소 [sj17_mind_...]
	#83
	{'url': "http://counsel.sejong.ac.kr/index.php?mid=menu05&page=",\
	'info': "sj17_counselor_notice",\
	'title_tag' : ["고민&상담", "공지"], 'login' : 0},\
	#84
	{'url': "http://counsel.sejong.ac.kr/index.php?mid=menu052&page=",\
	'info': "sj17_counselor_free",\
	'title_tag' : ["고민&상담"], 'login' : 0},\
	#SKBS [sj18_skbs_...]
	#85
	{'url': "http://www.skbs.kr/index.php?mid=notice&page=",\
	'info': "sj18_skbs_notice",\
	'title_tag' : ["방송국", "공지", "교내"], 'login' : 0},\
	#86
	{'url': "http://www.skbs.kr/index.php?mid=festivalinfo&page=",\
	'info': "sj18_skbs_event",\
	'title_tag' : ["방송국", "행사"], 'login' : 0},\
	#87
	{'url': "http://www.skbs.kr/index.php?mid=sejongnews&page=",\
	'info': "sj18_skbs_article",\
	'title_tag' : ["방송국", "소식"], 'login' : 0},\
	#88
	{'url': "http://www.skbs.kr/index.php?mid=todaymusic&page=",\
	'info': "sj18_skbs_music",\
	'title_tag' : ["방송국", "음악", "교내"], 'login' : 0},\
	#89
	{'url': "http://www.skbs.kr/index.php?mid=skbsnews&page=",\
	'info': "sj18_skbs_news",\
	'title_tag' : ["방송국", "소식", "교내"], 'login' : 0},\
	#총학생회 [sj19_chong_]
	#90
	{'url': "http://www.sejongstudent.com/xe/index.php?mid=notice&category=226&page=",\
	'info': "sj19_chong_news",\
	'title_tag' : ["총학생회", "소식", "교내"], 'login' : 0},\
	#91
	{'url': "http://www.sejongstudent.com/xe/index.php?mid=notice&category=228&page=",\
	'info': "sj19_chong_notice",\
	'title_tag' : ["총학생회", "공지", "교내"], 'login' : 0},\
	#92
	{'url': "http://www.sejongstudent.com/xe/index.php?mid=lost&page=",\
	'info': "sj19_chong_lost",\
	'title_tag' : ["총학생회", "분실물", "교내"], 'login' : 0},\
	#디시인사이드 세종대갤러리 [sj20_sejong_dc]
	#93
	{'url': "https://gall.dcinside.com/board/lists/?id=sejong&page=",\
	'info': "sj20_sejong_dc",\
	'title_tag' : ["커뮤니티", "기타"], 'login' : 0},\
	#세종위키백과 [sj21_sejong_wiki]
	#94
	{'url': "http://sejong.wiki/",\
	'info': "sj21_sejong_wiki",\
	'title_tag' : ["위키백과", "기타"], 'login' : 0},\
	#에브리타임 책방 [sj23_everytime_book]
	#95
	{'url': "https://bookstore.everytime.kr/?campus=60",\
	'info': "sj23_everytime_book",\
	'title_tag' : ["커뮤니티", "장터"], 'login' : 0},\
	#세종알리 [sj24_sejong_allie]
	#96
	{'url': "http://univalli.com/allisejong/search_news.php?&page=",\
	'info': "sj24_sejong_allie",\
	'title_tag' : ["세종알리", "교내", "소식"], 'login' : 0},\
	#씽굿 [sig25_thinkgood_info]
	#97
	{'url': "https://www.thinkcontest.com/Contest/CateField.html?s=ing&page=",\
	'info': "sig25_thinkgood_info",\
	'title_tag' : ["씽굿", "공모전&대외활동"], 'login' : 0},\
	#캠퍼스픽 [sig26_campuspick_...]
	#98
	{'url': "https://www.campuspick.com/activity",\
	'info': "sig26_campuspick_activity",\
	'title_tag' : ["캠퍼스픽", "공모전&대외활동"], 'login' : 0},\
	#99
	{'url': "https://www.campuspick.com/contest",\
	'info': "sig26_campuspick_contest",\
	'title_tag' : ["캠퍼스픽", "공모전&대외활동"], 'login' : 0},\
	#캠퍼스픽 스터디 [sig27_campuspick_...]
	#100
	{'url': "https://www.campuspick.com/study/list?category1=1&category2=0",\
	'info': "sig27_campuspick_language",\
	'title_tag' : ["캠퍼스픽", "동아리&모임"], 'login' : 1},\
	#101
	{'url': "https://www.campuspick.com/study/list?category1=2&category2=0",\
	'info': "sig27_campuspick_job",\
	'title_tag' : ["캠퍼스픽", "취업&진로", "동아리&모임"], 'login' : 1},\
	#102
	{'url': "https://www.campuspick.com/study/list?category1=3&category2=0",\
	'info': "sig27_campuspick_certificate",\
	'title_tag' : ["캠퍼스픽", "동아리&모임"], 'login' : 1},\
	#103
	{'url': "https://www.campuspick.com/study/list?category1=4&category2=0",\
	'info': "sig27_campuspick_study",\
	'title_tag' : ["캠퍼스픽", "동아리&모임"], 'login' : 1},\
	#캠퍼스픽 동아리 [sig28_campuspick_club]
	#104
	{'url': "https://www.campuspick.com/club?category=2",\
	'info': "sig28_campuspick_club",\
	'title_tag' : ["캠퍼스픽", "동아리&모임"], 'login' : 0},\
	#행복기숙사 [sj29_sejong_dormitory]
	#105
	{'url': "https://happydorm.sejong.ac.kr/sejong/bbs/getGolist.kmc?bbs_locgbn=SJ&bbs_id=notice&pPage=",\
	'info': "sj29_sejong_dormitory",\
	'title_tag' : ["행복기숙사"], 'login' : 0},\
	#세종대역 [sj30_sejongstation_...]
	#106
	{'url': "http://cafe484.daum.net/_c21_/bbs_list?grpid=1SVkj&fldid=KOYa&lastbbsdepth=000vLzzzzzzzzzzzzzzzzzzzzzzzzz&prev_page=1&listnum=20&page=",\
	'info': "sj30_sejongstation_notice",\
	'title_tag' : ["세종대역", "공지"], 'login' : 1},\
	#107
	{'url': "http://cafe484.daum.net/_c21_/bbs_list?grpid=1SVkj&fldid=KOaP&lastbbsdepth=000JIzzzzzzzzzzzzzzzzzzzzzzzzz&prev_page=1&listnum=20&page=",\
	'info': "sj30_sejongstation_news",\
	'title_tag' : ["세종대역", "소식"], 'login' : 0},\
	#108
	{'url': "http://cafe484.daum.net/_c21_/bbs_list?grpid=1SVkj&fldid=KObl&lastbbsdepth=003Auzzzzzzzzzzzzzzzzzzzzzzzzz&prev_page=1&listnum=20&page=",\
	'info': "sj30_sejongstation_free",\
	'title_tag' : ["세종대역", "커뮤니티", "기타"], 'login' : 1},\
	#109
	{'url': "http://cafe484.daum.net/_c21_/bbs_list?grpid=1SVkj&fldid=VWl0&lastbbsdepth=001V7zzzzzzzzzzzzzzzzzzzzzzzzz&prev_page=1&listnum=20&page=",\
	'info': "sj30_sejongstation_secret",\
	'title_tag' : ["세종대역", "커뮤니티", "기타"], 'login' : 1},\
	#110
	{'url': "http://cafe484.daum.net/_c21_/bbs_list?grpid=1SVkj&fldid=KRl2&lastbbsdepth=004kdzzzzzzzzzzzzzzzzzzzzzzzzz&prev_page=1&listnum=20&page=",\
	'info': "sj30_sejongstation_qna",\
	'title_tag' : ["세종대역", "커뮤니티", "기타"], 'login' : 1},\
	#111
	{'url': "http://cafe484.daum.net/_c21_/bbs_list?grpid=1SVkj&fldid=U5ed&lastbbsdepth=0003pzzzzzzzzzzzzzzzzzzzzzzzzz&prev_page=1&listnum=20&page=",\
	'info': "sj30_sejongstation_tip",\
	'title_tag' : ["세종대역", "커뮤니티", "기타"], 'login' : 1},\
	#112
	{'url': "http://cafe484.daum.net/_c21_/bbs_list?grpid=1SVkj&fldid=KOdx&lastbbsdepth=00001zzzzzzzzzzzzzzzzzzzzzzzzz&prev_page=1&listnum=20&page=",\
	'info': "sj30_sejongstation_graduation",\
	'title_tag' : ["세종대역", "취업&진로", "졸업", "기타", "커뮤니티"], 'login' : 1},\
	#113
	{'url': "http://cafe484.daum.net/_c21_/bbs_list?grpid=1SVkj&fldid=UdBM&lastbbsdepth=00047zzzzzzzzzzzzzzzzzzzzzzzzz&prev_page=1&listnum=20&page=",\
	'info': "sj30_sejongstation_job",\
	'title_tag' : ["세종대역", "취업&진로", "기타", "커뮤니티"], 'login' : 1},\
	#114
	{'url': "http://cafe484.daum.net/_c21_/bbs_list?grpid=1SVkj&fldid=KObP&lastbbsdepth=000Eozzzzzzzzzzzzzzzzzzzzzzzzz&prev_page=1&listnum=20&page=",\
	'info': "sj30_sejongstation_activity",\
	'title_tag' : ["세종대역", "공모전&대외활동", "커뮤니티"], 'login' : 1},\
	#115
	{'url': "http://cafe484.daum.net/_c21_/bbs_list?grpid=1SVkj&fldid=il3i&lastbbsdepth=0001Kzzzzzzzzzzzzzzzzzzzzzzzzz&prev_page=1&listnum=20&page=",\
	'info': "sj30_sejongstation_club",\
	'title_tag' : ["세종대역", "동아리&모임", "커뮤니티"], 'login' : 1},\
	#116
	{'url': "http://cafe484.daum.net/_c21_/bbs_list?grpid=1SVkj&fldid=KOdc&lastbbsdepth=0006Mzzzzzzzzzzzzzzzzzzzzzzzzz&prev_page=1&listnum=20&page=",\
	'info': "sj30_sejongstation_study",\
	'title_tag' : ["세종대역", "동아리&모임", "커뮤니티"], 'login' : 1},\
	#117
	{'url': "http://cafe484.daum.net/_c21_/bbs_list?grpid=1SVkj&fldid=KObe&lastbbsdepth=0004Jzzzzzzzzzzzzzzzzzzzzzzzzz&prev_page=1&listnum=20&page=",\
	'info': "sj30_sejongstation_food",\
	'title_tag' : ["세종대역", "커뮤니티", "기타"], 'login' : 1},\
	#118
	{'url': "http://cafe484.daum.net/_c21_/bbs_list?grpid=1SVkj&fldid=KOco&lastbbsdepth=001VHzzzzzzzzzzzzzzzzzzzzzzzzz&prev_page=1&listnum=20&page=",\
	'info': "sj30_sejongstation_trade",\
	'title_tag' : ["세종대역", "장터", "커뮤니티", "기타"], 'login' : 1},\
	#세종대 두드림 [sj31_sejongstation_...] [sj32_sejongstation_...]
	#119
	{'url': "https://do.sejong.ac.kr/ko/program/all/list/all/",\
	'info': "sj31_dodream_event",\
	'title_tag' : ["두드림", "행사"], 'login' : 0},\
	#120
	{'url': "https://do.sejong.ac.kr/ko/guide/notige/list/",\
	'info': "sj32_dodream_promotion",\
	'title_tag' : ["두드림", "홍보"], 'login' : 0},\
	#세종대 전자도서관 [sj33_mobilelibrary_...]
	#121
	{'url': "https://ebook.sejong.ac.kr/board/board_list.asp?b_id=1&page_num=",\
	'info': "sj33_mobilelibrary_notice",\
	'title_tag' : ["전자도서관", "공지"], 'login' : 0},\
	#122
	#에브리타임 모든 게시판 [sj34_everytime_all]
	{'url': "https://everytime.kr",\
	'info': "sj34_everytime_all",\
	'title_tag' : ["커뮤니티"], 'login' : 1},
	#데티즌 공모전 [sig35_detizen_...]
	#123
	{'url': "http://www.detizen.com/contest/?Category=1&IngYn=Y&PC=",\
	'info': "sig35_detizen_contest",\
	'title_tag' : ["공모전&대외활동"], 'login' : 0},\
	#124
	{'url': "http://www.detizen.com/activity/?Category=3&IngYn=Y&PC=",\
	'info': "sig35_detizen_activity",\
	'title_tag' : ["공모전&대외활동"], 'login' : 0},\
	#잡코리아
	#잡코리아 꿀팁[sig36_jobkoreatip_tip]
	#125
	{'url': "http://www.jobkorea.co.kr/goodjob/Tip?schCtgr=0&TipKwrdArray=알바생&TipKwrdArray=정보&TipKwrdArray=대화&TipKwrdArray=대기업&TipKwrdArray=뉴스&TipKwrdArray=상식퀴즈&TipKwrdArray=면접&TipKwrdArray=직장인&TipKwrdArray=연봉&TipKwrdArray=취준생&Page=",\
	'info': "sig36_jobkoreatip_tip",\
	'title_tag' : ["취업&진로"], 'login' : 0},\
	#잡코리아 [sig37_jobkorea_...]
	#126
	{'url': "http://www.jobkorea.co.kr/starter/?&schWork=2&isSaved=1&LinkGubun=0&Page=",\
	'info': "sig37_jobkorea_job",\
	'title_tag' : ["취업&진로"], 'login' : 0},\
	#127
	{'url': "http://www.jobkorea.co.kr/Starter/?&LinkGubun=0&Page=",\
	'info': "sig37_jobkorea_public",\
	'title_tag' : ["취업&진로"], 'login' : 0},\
	#세종대공기밥 [sj38_sejongbab_...]
	#128
	{'url': "http://www.gongibob.com/bbs_review.html?page=&viewnum=0&viewpagelimit=10",\
	'info': "sj38_sejongbab_tip",\
	'title_tag' : ["취업&진로"], 'login' : 0},\
	#이공계인력중계센터 [sj39_rndjob_...]
	#129
	{'url': "http://rndjob.or.kr/yard/notice.asp?&cur_pack=0&sfield=&gtxt=&gbn=A01&page=",\
	'info': "sig39_rndjob_job",\
	'title_tag' : ["취업&진로"], 'login' : 0},\
	#세종대학교 job solution [sj40~sj42_jobsolution_...]
	#130
	{'url': "http://u.educe.co.kr/jobsej/?mod=recruit&m_idx=217&orderword=pd&page=",\
	'info': "sj40_jobsolution_job",\
	'title_tag' : ["취업&진로"], 'login' : 0},\
	#131
	{'url': "http://u.educe.co.kr/jobsej/?mod=jobFair&m_idx=227&page=",\
	'info': "sj41_jobsolutionAnother_semina",\
	'title_tag' : ["취업&진로", "행사", "세미나"], 'login' : 0},\
	#132
	{'url': "http://u.educe.co.kr/jobsej/?mod=interview&m_idx=57&page=",\
	'info': "sj42_jobsolutionAnother_review",\
	'title_tag' : ["취업&진로"], 'login' : 0},\
	#133
	{'url': "http://u.educe.co.kr/jobsej/?mod=afterInterview&m_idx=89&page=",\
	'info': "sj42_jobsolutionAnother_interview",\
	'title_tag' : ["취업&진로"], 'login' : 0},\
	#인디드 [sig43_indeed_job]
	#134
	{'url': "https://kr.indeed.com/jobs?q=&l=서울&start=",\
	'info': "sig43_indeed_job",\
	'title_tag' : ["취업&진로"], 'login' : 0},\
	#네이버블로그 [sj44_naverblog_...]
	#135
	{'url': "https://m.blog.naver.com/PostList.nhn?blogId=sejong_univ&from=postList",\
	'info': "sj44_naverblog_sejong",\
	'title_tag' : ["교내"], 'login' : 0},\
	#136
	{'url': "https://m.blog.naver.com/PostList.nhn?blogId=b_ob02",\
	'info': "sj44_naverblog_campustown",\
	'title_tag' : ["교내"], 'login' : 0},\
	#세종대학교 컴퓨터공학과
	#137
	{'url': "http://home.sejong.ac.kr/bbs/bbslist.do?bbsid=487&wslID=cedpt&searchField=&searchValue=&currentPage=1&page=",\
	'info': "sj9_computer_notice",\
	'title_tag' : ["교내", "컴퓨터공학과", "공지"], 'login' : 0},\
	#138 무중력지대
	{'url': "http://youthzone.kr/program_applies?page=",\
	'info': "sig45_infor_notice",\
	'title_tag' : ["모집"], 'login' : 0},\
	#139
	{'url': "http://youthzone.kr/external_programs?page=",\
	'info': "sig45_external_notice",\
	'title_tag' : ["모집"], 'login' : 0},\
	#140
	{'url': "http://youthzone.kr/reviews?page=",\
	'info': "sig45_review_data",\
	'title_tag' : ["모집"], 'login' : 0},\
	#141 애드캠퍼스
	{'url': "https://addcampus.com/community/board/1?page=1&search_txt=",\
	'info': "sig46_addcampus_board",\
	'title_tag' : ["커뮤니티"], 'login' : 0},\
	#142 20대연구소
	{'url': "https://www.20slab.org/SNSColumn?pageidx=",\
	'info': "sig47_20lab_column",\
	'title_tag' : ["소식"], 'login' : 0},\
	#143
	{'url': "https://www.20slab.org/Infographics?pageidx=",\
	'info': "sig47_20lab_infographics",\
	'title_tag' : ["소식"], 'login' : 0},\
	#144
	{'url': "https://www.20slab.org/Press?pageidx=",\
	'info': "sig47_20lab_announcement",\
	'title_tag' : ["소식"], 'login' : 0},\
	#145
	{'url': "https://www.20slab.org/Data?pageidx=",\
	'info': "sig47_20lab_data",\
	'title_tag' : ["소식"], 'login' : 0},\
	#146
	{'url': "https://www.20slab.org/Report?pageidx=",\
	'info': "sig47_20lab_report",\
	'title_tag' : ["소식"], 'login' : 0},\
	#147 VMS
	{'url': "https://www.vms.or.kr/partspace/recruit.do?area=&areagugun=&acttype=&status=1&termgbn=&page=",\
	'info': "sig48_vms_volunteer",\
	'title_tag' : ["봉사"], 'login' : 0},\
	#148 캠퍼스픽 커뮤니티 - 알바
	{'url': "https://www.campuspick.com/community?id=3098",\
	'info': "sig50_campuspick_parttime",\
	'title_tag' : ["알바&구인"], 'login' : 0},\
	#149 대학내일
	{'url': "https://univ20.com/",\
	'info': "sig51_univ20_main",\
	'title_tag' : ["소식"], 'login' : 0},\
	#150 온라인 청년센터
	{'url': "https://www.youthcenter.go.kr/board/boardList.do?bbsNo=3&ntceStno=&pageUrl=board%2Fboard&orderBy=REG_DTM&orderMode=DESC&pageIndex=",\
	'info': "sig52_youthcenter_info",\
	'title_tag' : ["소식"], 'login' : 0},\
	#151 한국 장학재단 공지사항
	{'url': "https://www.kosaf.go.kr/ko/notice.do?&page=",\
	'info': "sig53_kosaf_info",\
	'title_tag' : ["소식"], 'login' : 0},\
	#152 Naver news 대학교
	{'url': "https://search.naver.com/search.naver?&where=news&query=%EB%8C%80%ED%95%99%EA%B5%90&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&start=&refresh_start=0",\
	'info': "sig54_naver_news",\
	'title_tag' : ["소식"], 'login' : 0},\
	)
