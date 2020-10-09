from pymongo import MongoClient
from modules.recommender.fasttext import Recommender
import os

FT = Recommender(os.getenv("SIGNUS_FT_MODEL_PATH"))
#대학교
category_university = {
	'category_name' : '대학교',
	'info': 
		[
			'sj1_main_founded', 'sj1_main_notice', 'sj1_main_entrance', 'sj1_main_job',  'sj1_main_schoiarship',
			'sj1_main_college', 'sj1_main_bidding', 'sj1_main_dataprocessFAQ', 'sj1_main_studentFAQ',
			'sj1_main_schoiarshipFAQ','sj1_main_foreignerFAQ', 'sj1_main_foreignernotice',
			'sj1_main_student', 'sj6_library_notice', 'sj6_library_book','sj6_library_FAQ',
			'sj7_promotion_article', 'sj7_promotion_prism', 'sj7_promotion_report', 'sj7_promotion_research',
			'sj7_promotion_speech', 'sj8_promotion_media', 'sj15_classic_notice', 'sj15_classic_news',
			'sj15_classic_creative','sj15_classic_event', 'sj15_classic_shp', 'sj17_counselor_notice',
			'sj17_counselor_free', 'sj18_skbs_notice','sj18_skbs_event', 'sj18_skbs_article'
			'sj18_skbs_music', 'sj18_skbs_news', 'sj19_chong_news', 'sj19_chong_notice',
			'sj19_chong_lost', 'sj20_sejong_dc', 'sj24_sejong_allie', 'sj29_sejong_dormitory'
			'sj30_sejongstation_notice', 'sj30_sejongstation_news',
			'sj30_sejongstation_free', 'sj30_sejongstation_secret', 'sj30_sejongstation_qna',
			'sj30_sejongstation_tip', 'sj30_sejongstation_graduation', 'sj30_sejongstation_job',
			'sj30_sejongstation_activity', 'sj30_sejongstation_club', 'sj30_sejongstation_study',
			'sj30_sejongstation_food', 'sj30_sejongstation_trade', 'sj33_mobilelibrary_notice',
			'sj44_naverblog_sejong','sj44_naverblog_campustown','sig46_addcampus_board','sig47_20lab_column',
			'sig47_20lab_announcement','sig47_20lab_announcement','sig47_20lab_data','sig47_20lab_report',
			'sig48_vms_volunteer','sig50_campuspick_parttime','sig51_univ20_main','sig52_youthcenter_info',
			'sig53_kosaf_info','sig54_naver_news'
		],
	'tag': 
		[
			'장학', '사이버강의', '수강', '졸업', '조교', 'faq', '소식', '학사', '국제',
			'교환학생', '수강편람', '입학', '학술정보원', '입찰', '방송국', '홍보원', '교내',
			'전화번호부', 'ck사업단', '총학생회', '행복기숙사', '전자도서관', '학사일정',
			'대양휴머니티칼리지', '에델바이스', '학부', 'kmooc', '블랙보드', 'uis', '학기', '창의', '학술',
			'세종대학교', '세종대', '세종인', '휴학', '학교', '연구', '전공', '사업단',
			'홍보원', '장학금', '기숙사', '도서관', '세사대', '캠퍼스타운', '학위', '캠퍼스'
		],
	'info_num': [],
	'topic_vector': []
}
#동아리&모임
category_club = {
	'category_name': '동아리&모임',
	'info': 
		[
		'sig27_campuspick_language', 'sig27_campuspick_job', 'sig27_campuspick_certificate',
		'sig27_campuspick_study', 'sig28_campuspick_club'
		],
	'tag': 
		[
			'멘토링', '동아리&모임', '방송국', '총학생회', '동아리', '모임', '스터디', '서포터즈', '봉사단',
			'동호회', '봉사', '아카데미', '학생회', '중앙동아리', '멘토', '멘티', '소모임', 'skbs'
		],
	'info_num': [],
	'topic_vector': []
}
#공모전&행사
category_competition = {
	'category_name': '공모전&행사',
	'info': 
		[
		'sig25_thinkgood_info', 'sig26_campuspick_activity', 'sig26_campuspick_contest',
		'sj31_dodream_event', 'sj32_dodream_promotion', 'sig35_detizen_contest', 'sig35_detizen_activity'
		],
	'tag': 
		[
			'행사', '공모전&대외활동', '세미나', '봉사', '두드림', '봉사단', '공모전', '대외활동',
			'대내활동', '특강', '강연', '대회', '경연', '대양홀', '콩쿨', '콩쿠르', '개최', '축제',
			'기념', '콘서트', '콘테스트', '연주회', '대동제', '힘미제', '박람회', '캠프', '컨퍼런스',
			'콘퍼런스', '간담회', '파티', '경진', '시상식', '상금', '대상', '최우수상', '우수상',
			'금상', '은상', '동상', '장려상', '아이디어', '예선', '본선', '페스티벌', '강사', '이벤트', '강당', '다과회', '원정대'
		],
	'info_num': [],
	'topic_vector': []
}
#진로&구인
category_course = {
	'category_name': '진로&구인',
	'info': 
		[
			'sj2_udream_notice', 'sj3_udream_jobinfo', 'sj4_udream_workinfo', 'sj5_udream_workyoung',
			'sig36_jobkoreatip_tip', 'sig37_jobkorea_job', 'sig37_jobkorea_public', 'sj38_sejongbab_tip',
			'sig39_rndjob_job', 'sj40_jobsolution_job', 'sj41_jobsolutionAnother_semina',
			'sj42_jobsolutionAnother_review', 'sj42_jobsolutionAnother_interview', 'sig43_indeed_job',
			'sig45_infor_notice','sig45_external_notice','sig45_review_data','sig50_campuspick_parttime'
		],
	'tag': 
		[
			'취업&진로', '창업', '모집', '과외&강사', '알바&구인', '공개채용', '추천채용', '특별채용', '수시채용',
			'인턴', '계약직', '정규직', '경력', '기술직', '의료직', '교직', '마케팅', '조리직', '서비스직', '알바',
			'구인', '과외', '강사', '취업', '진로', '채용', '직업', '일자리', '인턴쉽', '인턴십', '산업체',
			'포트폴리오', '이력', '이력서', '자소서', '자기소개서', '급여', '연봉', '아르바이트', '파트타임',
			'사무직', '현장직', '시급', '근무', '근무지', '자격증', '일일직', '노동', '근로', '업종'
		],
	'info_num': [],
	'topic_vector': []
}
#예외
category_except = {
	'category_name': '예외',
	'info':
		[
			'sj9_chinatrade_notice', 'sj9_chinatrade_job', 'sj9_history_notice', 'sj9_history_data', 
			'sj9_ecotrade_notice', 'sj9_ecotrade_event', 'sj9_administ_notice', 'sj9_management_notice',
			'sj9_management_job', 'sj9_hotel_notice', 'sj9_software_notice', 'sj9_elecommunication_notice',
			'sj9_elecommunication_data', 'sj9_infoprotection_notice', 'sj9_infoprotection_job',
			'sj9_energy_notice', 'sj9_nano_notice', 'sj9_nano_job', 'sj9_nano_FAQ', 'sj9_defensesys_notice',
			'sj9_indusdesign_notice', 'sj9_indusdesign_data', 'sj9_designinnovation_studentnotice',
			'sj9_designinnovation_notice', 'sj9_designinnovation_data', 'sj9_animation_notice',
			'sj9_pysical_notice', 'sj9_pysical_job', 'sj9_dance_notice', 'sj9_dance_event',
			'sj9_law_notice', 'sj10_pysics_notice', 'sj11_japanese_notice', 'sj12_archi_notice',
			'sj12_archi_news', 'sj13_computer_notice', 'sj13_computer_event', 'sj13_computer_job',
			'sj14_imc_notice', 'sj14_imc_news', 'sj14_imc_student', 'sj16_navercafe_foreigner',
			'sj16_navercafe_music', 'sj16_navercafe_animation', 'sj16_navercafe_math', 'sj16_navercafe_korean',
			'sj16_navercafe_environmentenergy', 'sj16_navercafe_chemistry', 'sj16_navercafe_sjnanuri',
			'sj16_navercafe_eleinfoengineer', 'sj16_navercafe_imc', 'sj16_navercafe_club', 'sj21_sejong_wiki',
			'sj9_computer_notice'
		],
	'tag': [],
	'info_num': [],
}
#미사용
category_unused = {
	'category_name': '미사용',
	'info':
		[
		'sj23_everytime_book', 'sj34_everytime_all'
		],
	'tag': [],
	'info_num': [],
}

def create_table_category(db):
# 테이블 존재 유무 파악
	collist = db.list_collection_names()
	if 'category' in collist:
		print(":::: category 테이블이 존재 합니다 ::::")
		return
	insert_to_category(db)

def insert_to_category(db):
	db_list = db.list_collection_names()
	post_info = []

	if 'post_info' in db_list:
		post_info = list(db.post_info.find())

	info_num_index = []
	for i in range(len(post_info)):
		if post_info[i]['info_num'] == 0: #0번째는 sj_domain -> 예시
			continue
		tup=(post_info[i]['info'],post_info[i]['info_num']) #('sj1_main_notice',1)
		info_num_index.append(list(tup))

	categories = [category_university, category_club, category_competition, category_course, category_except, category_unused]
	
	for category in categories:
		for info_list in category['info']:
			for i in range(len(info_num_index)):
				if info_list == info_num_index[i][0]:
					(category['info_num']).append(info_num_index[i][1])
					break
		if len(category['tag']) != 0: #태그리스트가 비어 있지 않은 경우에만 topic_vector 생성
   			category['topic_vector'] = FT.doc2vec(category['tag']).tolist()
		db.category.insert(category)
	print(":::: category 테이블 생성 완료! ::::")