# DB 처음 초기화 할 때 필요한 데이터들.
# 현재 구조상 어디에 이 default_data.py 를 둬야할지 애매하여 우선 여기에 두었음.

default_master_config = [
    {   
        # 추천에 필요한 지표
        "key": "RECOMMENDATION",
        "value":
        {
            "FASTTEXT_SIM_PERCENT": 0.7,
            "TOS_WEIGHT": 1,
            "TAS_WEIGHT": 1,
            "FAS_WEIGHT": 1,
            "RANDOM_WEIGHT": 1,
            "DEFAULT_DATE": 60,
            "POSTS_NUM_BY_CATEGORY": [60, 33, 33, 33, 18],
            # ???? 알아봐야함.
            "SJ_RECOMMENDATION_POST_NUM": 500
            "SJ_RECOMMENDATION_POST_WEIGHT": 150
            "SJ_RECOMMENDATION_POST_MINUS_WEIGHT": -75
        }
    },
    {   
        # 관심사 측정에 필요한 지표
        "key": "TENDENCY",
        "value":
        {
            "FAV_TAG_WEIGHT": 4,
            "VIEW_TAG_WEIGHT": 3,
            "TAG_SUM_WEIGHT": 1.5
            "FAV_TOPIC_WEIGHT": 35,
            "VIEW_TOPIC_WEIGHT": 30,
            "SEARCH_TOPIC_WEIGHT": 25,
            "NEWSFEED_TOPIC_WEIGHT": 10
        }
    },
    {   
        # 사용자 관련 지표
        "key": "USER",
        "value":
        {
            "LOG_LIMIT": {"view": 100, "search": 40, "fav": 20, "newsfeed": 30},
            "COLD_START": 10,
            "TAG_SUM_WEIGHT": 1.5
            "FAV_TOPIC_WEIGHT": 35,
            "VIEW_TOPIC_WEIGHT": 30,
            "SEARCH_TOPIC_WEIGHT": 25,
            "NEWSFEED_TOPIC_WEIGHT": 10
        }
    },
    {   
        # 개수 및 제한 관련 지표
        "key": "NUMBER_LIMIT",
        "value":
        {
            "RETURN_NUM": 150
            "C_S_LIMIT": 5000, # Category Search DB document 최대 호출 제한 개수
            "T_N_LIMIT": 2000,  # Topic newsfeed DB document 최대 호출 제한 개수
            "PUBLIC_N_LIMIT": 250, # 비회원 추천 뉴스피드 DB document 최대 호출 제한 개수
            "C_S_DEFAULT_DATE": 365, # 카테고리 검색 날짜 제한 (최대 몇 일)
            "REALTIME_LIMIT": 20, # 실시간 검색어 검색 제한 리미트
            "REALTIME_RETURN_NUM": 10 # 실시간 검색어 반환 개수
        }
    }
]

default_category = [
    #대학교
    {
        'category_name': '대학교',
        'info': 
        [
            'sj1_main_founded', 'sj1_main_notice', 'sj1_main_entrance', 'sj1_main_job',  'sj1_main_schoiarship', 'sj1_main_college', 'sj1_main_bidding', 'sj1_main_dataprocessFAQ', 'sj1_main_studentFAQ', 'sj1_main_schoiarshipFAQ', 'sj1_main_foreignerFAQ', 'sj1_main_foreignernotice', 'sj1_main_student', 'sj6_library_notice', 'sj6_library_book', 'sj6_library_FAQ', 'sj7_promotion_article', 'sj7_promotion_prism', 'sj7_promotion_report', 'sj7_promotion_research', 'sj7_promotion_speech', 'sj8_promotion_media', 'sj15_classic_notice', 'sj15_classic_news', 'sj15_classic_creative', 'sj15_classic_event', 'sj15_classic_shp', 'sj17_counselor_notice', 'sj17_counselor_free', 'sj18_skbs_notice', 'sj18_skbs_event', 'sj18_skbs_article', 'sj18_skbs_music', 'sj18_skbs_news', 'sj19_chong_news', 'sj19_chong_notice', 'sj19_chong_lost','sj24_sejong_allie', 'sj29_sejong_dormitory', 'sj33_mobilelibrary_notice', 'sj44_naverblog_sejong', 'sj44_naverblog_campustown'
        ],
        'tag': 
        [
            '장학', '사이버강의', '수강', '졸업', '조교', 'faq', '소식', '학사', '국제', '교환학생', '수강편람', '입학', '학술정보원', '입찰', '방송국', '홍보원', '교내', '전화번호부', 'ck사업단', '총학생회', '행복기숙사', '전자도서관', '학사일정', '대양휴머니티칼리지', '에델바이스', '학부', 'kmooc', '블랙보드', 'uis', '학기', '창의', '학술'
        ] + 
        [
            '세종대학교', '세종대', '세종인', '휴학', '학교', '연구', '전공', '사업단', '홍보원', '장학금', '기숙사', '도서관', '세사대', '캠퍼스타운', '학위', '캠퍼스'
        ]
    },
    #동아리&모임
    {
        'category_name': '동아리&모임',
        'info': 
        [
            'sj27_campuspick_language', 'sj27_campuspick_job', 'sj27_campuspick_certificate', 'sj27_campuspick_study', 'sj28_campuspick_club'
        
        ],
        'tag': 
        [
            '멘토링', '동아리&모임', '방송국', '총학생회', '동아리', '모임', '스터디', '서포터즈', '봉사단'
        ] + 
        [
            '동호회', '봉사', '아카데미', '학생회', '중앙동아리', '멘토', '멘티', '소모임', 'skbs'
        ]
    },
    #공모전&행사
    {
        'category_name': '공모전&행사',
        'info': 
        [
            'sj25_thinkgood_info', 'sj26_campuspick_activity', 'sj26_campuspick_contest', 'sj31_dodream_event', 'sj32_dodream_promotion', 'sj35_detizen_contest', 'sj35_detizen_activity'
        ],
        'tag': 
        [
            '행사', '공모전&대외활동', '세미나', '봉사', '두드림', '봉사단', '공모전', '대외활동', '대내활동', '특강', '강연', '대회', '경연', '대양홀', '콩쿨', '콩쿠르', '개최', '축제', '기념', '콘서트', '콘테스트', '연주회', '대동제', '힘미제', '박람회', '캠프', '컨퍼런스', '콘퍼런스', '간담회', '파티', '경진'
        ] + 
        [
            '시상식', '상금', '대상', '최우수상', '우수상', '금상', '은상', '동상', '장려상', '아이디어', '예선', '본선', '페스티벌', '강사', '이벤트', '강당', '다과회', '원정대'
        ]
    },
    #진로&구인
    {
        'category_name': '진로&구인',
        'info': 
        [
            'sj2_udream_notice', 'sj3_udream_jobinfo', 'sj4_udream_workinfo', 'sj5_udream_workyoung', 'sj36_jobkoreatip_tip', 'sj37_jobkorea_job', 'sj37_jobkorea_public', 'sj38_sejongbab_tip', 'sj39_rndjob_job', 'sj40_jobsolution_job', 'sj41_jobsolutionAnother_semina', 'sj42_jobsolutionAnother_review', 'sj42_jobsolutionAnother_interview', 'sj43_indeed_job'
        ],
        'tag': 
        [
            '취업&진로', '창업', '모집', '과외&강사', '알바&구인', '공개채용', '추천채용', '특별채용', '수시채용', '인턴', '계약직', '정규직', '경력', '기술직', '의료직', '교직', '마케팅', '조리직', '서비스직', '알바', '구인', '과외', '강사', '취업', '진로', '채용', '직업', '일자리', '인턴쉽', '인턴십', '산업체'
        ] + 
        [
            '포트폴리오', '이력', '이력서', '자소서', '자기소개서', '급여', '연봉', '아르바이트', '파트타임', '사무직', '현장직', '시급', '근무', '근무지', '자격증', '일일직', '노동', '근로', '업종'
        ]
    },
    #커뮤니티
    {
        'category_name': '커뮤니티',
        'info': 
        [
            'sj20_sejong_dc', 'sj30_sejongstation_notice', 'sj30_sejongstation_news', 'sj30_sejongstation_free', 'sj30_sejongstation_secret', 'sj30_sejongstation_qna', 'sj30_sejongstation_tip', 'sj30_sejongstation_graduation', 'sj30_sejongstation_job', 'sj30_sejongstation_activity', 'sj30_sejongstation_club', 'sj30_sejongstation_study', 'sj30_sejongstation_food', 'sj30_sejongstation_trade', 'community'
        ],
        'tag': 
        [
            '학식', '고민&상담', '종교', '여행', '커뮤니티', '분실물', '연애', '세종냥이', '홍보', '세종대역'
        ] + 
        [
            '커뮤니티', '카페', '영화', '독서', '문화', '생활', '개강', '종강'
        ]
    },
    #예외(검색용)
    {
        'category_name': '예외',
        'info':
        [
            'sj9_chinatrade_notice', 'sj9_chinatrade_job', 'sj9_history_notice', 'sj9_history_data', 'sj9_ecotrade_notice', 'sj9_ecotrade_event', 'sj9_administ_notice', 'sj9_management_notice', 'sj9_management_job', 'sj9_hotel_notice', 'sj9_software_notice', 'sj9_elecommunication_notice', 'sj9_elecommunication_data', 'sj9_infoprotection_notice', 'sj9_infoprotection_job', 'sj9_energy_notice', 'sj9_nano_notice', 'sj9_nano_job', 'sj9_nano_FAQ', 'sj9_defensesys_notice', 'sj9_indusdesign_notice', 'sj9_indusdesign_data', 'sj9_designinnovation_studentnotice', 'sj9_designinnovation_notice', 'sj9_designinnovation_data', 'sj9_animation_notice', 'sj9_pysical_notice', 'sj9_pysical_job', 'sj9_dance_notice', 'sj9_dance_event', 'sj9_law_notice', 'sj10_pysics_notice', 'sj11_japanese_notice', 'sj12_archi_notice', 'sj12_archi_news', 'sj13_computer_notice', 'sj13_computer_event', 'sj13_computer_job', 'sj14_imc_notice', 'sj14_imc_news', 'sj14_imc_student', 'sj16_navercafe_foreigner', 'sj16_navercafe_music', 'sj16_navercafe_animation', 'sj16_navercafe_math', 'sj16_navercafe_korean', 'sj16_navercafe_environmentenergy', 'sj16_navercafe_chemistry', 'sj16_navercafe_sjnanuri', 'sj16_navercafe_eleinfoengineer', 'sj16_navercafe_imc', 'sj16_navercafe_club', 'sj21_sejong_wiki', 'sj9_computer_notice'
        ],
        'tag': []
    },
    {
        'category_name': '미사용',
        'info':
        [
            'sj23_everytime_book', 'sj34_everytime_all'
        ],
        'tag': []
    }
]

default_realtime = [
	['세종대', 0.9],
	['장학금', 0.9],
	['학식', 0.9],
	['공모전', 0.9],
	['공결', 0.9],
	['스터디', 0.9],
	['세종사회봉사', 0.9],
	['수강', 0.9],
	['기초코딩', 0.9],
	['학술정보원', 0.9],
	['교양', 0.9],
	['토익', 0.9],
	['동아리', 0.9],
	['야식행사', 0.9],
	['기숙사', 0.9],
	['대양AI센터', 0.9],
	['어린이대공원', 0.9],
	['카페', 0.9],
	['맛집', 0.9],
	['대동제', 0.9]
]