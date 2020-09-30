from pymongo import MongoClient

def create_table_category(db):
	# 테이블 존재 유무 파악
	collist = db.list_collection_names()
	if 'category' in collist:
		print(":::: category 테이블이 존재 합니다 ::::")
		return

	db.category.insert([
		#대학교
		{
			'category_name': '대학교',
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
			'info_num': 0
		},
		#동아리&모임
		{
			'category_name': '동아리&모임',
			'info': 
			[
				'sig27_campuspick_language', 'sig27_campuspick_job', 'sig27_campuspick_certificate',
				'sig27_campuspick_study', 'sig28_campuspick_club'
			],
			'info_num': 0

		},
		#공모전&행사
		{
			'category_name': '공모전&행사',
			'info': 
			[
				'sig25_thinkgood_info', 'sig26_campuspick_activity', 'sig26_campuspick_contest',
				'sj31_dodream_event', 'sj32_dodream_promotion', 'sig35_detizen_contest', 'sig35_detizen_activity'
			],
			'info_num': 0

		},
		#진로&구인
		{
			'category_name': '진로&구인',
			'info': 
			[
				'sj2_udream_notice', 'sj3_udream_jobinfo', 'sj4_udream_workinfo', 'sj5_udream_workyoung',
				'sig36_jobkoreatip_tip', 'sig37_jobkorea_job', 'sig37_jobkorea_public', 'sj38_sejongbab_tip',
				'sig39_rndjob_job', 'sj40_jobsolution_job', 'sj41_jobsolutionAnother_semina',
				'sj42_jobsolutionAnother_review', 'sj42_jobsolutionAnother_interview', 'sig43_indeed_job',
				'sig45_infor_notice','sig45_external_notice','sig45_review_data','sig50_campuspick_parttime'
			],
			'info_num': 0

		},
		#예외(검색용)
		{
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
			'info_num': 0

		},
		{
			'category_name': '미사용',
			'info':
			[
				'sj23_everytime_book', 'sj34_everytime_all'
			],
			'info_num': 0

		}
	])
	print(":::: category 테이블 생성 완료! ::::")