BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `wordtags` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`created_date`	datetime NOT NULL,
	`modified_date`	datetime NOT NULL,
	`wotagtext`	varchar ( 20 ) NOT NULL UNIQUE,
	`wotagcomment`	varchar ( 200 ) NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `words_wordtags` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`words_id`	integer NOT NULL,
	`wordtags_id`	integer NOT NULL,
	FOREIGN KEY(`words_id`) REFERENCES `words`(`id`),
	FOREIGN KEY(`wordtags_id`) REFERENCES `wordtags`(`id`)
);
CREATE TABLE IF NOT EXISTS `words` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`created_date`	datetime NOT NULL,
	`modified_date`	datetime NOT NULL,
	`status`	integer NOT NULL,
	`order`	integer,
	`wordtext`	varchar ( 250 ),
	`isnotword`	bool NOT NULL,
	`translation`	varchar ( 500 ),
	`romanization`	varchar ( 100 ),
	`customsentence`	varchar ( 1000 ),
	`wordinside_order`	text,
	`isCompoundword`	bool NOT NULL,
	`show_compoundword`	bool NOT NULL,
	`compoundword_id`	integer,
	`grouper_of_same_words_id`	integer,
	`language_id`	integer,
	`owner_id`	integer NOT NULL,
	`sentence_id`	integer,
	`text_id`	integer,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`),
	FOREIGN KEY(`language_id`) REFERENCES `languages`(`id`),
	FOREIGN KEY(`compoundword_id`) REFERENCES `words`(`id`),
	FOREIGN KEY(`text_id`) REFERENCES `texts`(`id`),
	FOREIGN KEY(`grouper_of_same_words_id`) REFERENCES `Grouper_of_same_words`(`id`),
	FOREIGN KEY(`sentence_id`) REFERENCES `sentences`(`id`)
);
CREATE TABLE IF NOT EXISTS `texttags` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`created_date`	datetime NOT NULL,
	`modified_date`	datetime NOT NULL,
	`txtagtext`	varchar ( 20 ) NOT NULL UNIQUE,
	`txtagcomment`	varchar ( 200 ) NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `texts_texttags` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`texts_id`	integer NOT NULL,
	`texttags_id`	integer NOT NULL,
	FOREIGN KEY(`texttags_id`) REFERENCES `texttags`(`id`),
	FOREIGN KEY(`texts_id`) REFERENCES `texts`(`id`)
);
CREATE TABLE IF NOT EXISTS `texts` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`created_date`	datetime NOT NULL,
	`modified_date`	datetime NOT NULL,
	`title`	varchar ( 200 ) NOT NULL,
	`text`	text NOT NULL,
	`annotatedtext`	text NOT NULL,
	`audiouri`	varchar ( 200 ),
	`sourceuri`	varchar ( 1000 ),
	`language_id`	integer NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`language_id`) REFERENCES `languages`(`id`),
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `socialaccount_socialtoken` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`token`	text NOT NULL,
	`token_secret`	text NOT NULL,
	`expires_at`	datetime,
	`account_id`	integer NOT NULL,
	`app_id`	integer NOT NULL,
	FOREIGN KEY(`account_id`) REFERENCES `socialaccount_socialaccount`(`id`),
	FOREIGN KEY(`app_id`) REFERENCES `socialaccount_socialapp`(`id`)
);
CREATE TABLE IF NOT EXISTS `socialaccount_socialapp_sites` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`socialapp_id`	integer NOT NULL,
	`site_id`	integer NOT NULL,
	FOREIGN KEY(`socialapp_id`) REFERENCES `socialaccount_socialapp`(`id`),
	FOREIGN KEY(`site_id`) REFERENCES `django_site`(`id`)
);
CREATE TABLE IF NOT EXISTS `socialaccount_socialapp` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`provider`	varchar ( 30 ) NOT NULL,
	`name`	varchar ( 40 ) NOT NULL,
	`client_id`	varchar ( 191 ) NOT NULL,
	`key`	varchar ( 191 ) NOT NULL,
	`secret`	varchar ( 191 ) NOT NULL
);
CREATE TABLE IF NOT EXISTS `socialaccount_socialaccount` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`provider`	varchar ( 30 ) NOT NULL,
	`uid`	varchar ( 191 ) NOT NULL,
	`last_login`	datetime NOT NULL,
	`date_joined`	datetime NOT NULL,
	`user_id`	integer NOT NULL,
	`extra_data`	text NOT NULL,
	FOREIGN KEY(`user_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `sentences` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`created_date`	datetime NOT NULL,
	`modified_date`	datetime NOT NULL,
	`order`	integer NOT NULL,
	`sentencetext`	text,
	`language_id`	integer NOT NULL,
	`owner_id`	integer NOT NULL,
	`text_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`),
	FOREIGN KEY(`text_id`) REFERENCES `texts`(`id`),
	FOREIGN KEY(`language_id`) REFERENCES `languages`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_texts_per_page` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	integer NOT NULL,
	`min`	integer NOT NULL,
	`max`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_text_visit_statuses_via_key` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`min`	integer,
	`max`	integer,
	`stdft`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_text_r_frameheight_percent` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	integer NOT NULL,
	`min`	integer NOT NULL,
	`max`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_text_l_framewidth_percent` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	integer NOT NULL,
	`min`	integer NOT NULL,
	`max`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_text_h_frameheight_with_audio` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	integer NOT NULL,
	`min`	integer NOT NULL,
	`max`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_text_h_frameheight_no_audio` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	integer NOT NULL,
	`min`	integer NOT NULL,
	`max`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_test_sentence_count` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`min`	integer,
	`max`	integer,
	`stdft`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_test_r_frameheight_percent` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	integer NOT NULL,
	`min`	integer NOT NULL,
	`max`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_test_main_frame_waiting_time` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	integer NOT NULL,
	`min`	integer NOT NULL,
	`max`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_test_l_framewidth_percent` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	integer NOT NULL,
	`min`	integer NOT NULL,
	`max`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_test_h_frameheight` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	integer NOT NULL,
	`min`	integer NOT NULL,
	`max`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_test_edit_frame_waiting_time` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	integer NOT NULL,
	`min`	integer NOT NULL,
	`max`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_terms_per_page` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	integer NOT NULL,
	`min`	integer NOT NULL,
	`max`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_term_translation_delimiters` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`stdft`	varchar ( 40 ) NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_term_sentence_count` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`min`	integer,
	`max`	integer,
	`stdft`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_tags_per_page` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	integer NOT NULL,
	`min`	integer NOT NULL,
	`max`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_similar_terms_count` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	integer NOT NULL,
	`min`	integer NOT NULL,
	`max`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_show_text_word_counts` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`min`	integer,
	`max`	integer,
	`stdft`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_show_all_words` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`min`	integer,
	`max`	integer,
	`stdft`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_mobile_display_mode` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`min`	integer,
	`max`	integer,
	`stdft`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currentwordtag2` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currentwordtag12` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currentwordtag1` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currentwordstatus` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currentwordsort` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currentwordquery` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currentwordpage` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currenttextsort` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currenttextquery` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currenttextpage` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currenttext_id` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currentlang_name` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currentlang_id` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currentarchivetexttag2` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currentarchivetexttag12` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currentarchivetexttag1` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currentarchivequery` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_currentarchivepage` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	varchar ( 40 ) NOT NULL,
	`min`	integer,
	`max`	integer,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `lwt_settings_archivedtexts_per_page` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`stvalue`	varchar ( 40 ),
	`stdft`	integer NOT NULL,
	`min`	integer NOT NULL,
	`max`	integer NOT NULL,
	`isinteger`	bool NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `languages` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`created_date`	datetime NOT NULL,
	`modified_date`	datetime NOT NULL,
	`name`	varchar ( 40 ) NOT NULL UNIQUE,
	`dict1uri`	varchar ( 200 ) NOT NULL,
	`dict2uri`	varchar ( 200 ),
	`googletranslateuri`	varchar ( 200 ),
	`exporttemplate`	varchar ( 1000 ),
	`textsize`	integer NOT NULL,
	`charactersubstitutions`	varchar ( 500 ) NOT NULL,
	`regexpsplitsentences`	varchar ( 500 ) NOT NULL,
	`exceptionssplitsentences`	varchar ( 500 ) NOT NULL,
	`regexpwordcharacters`	varchar ( 500 ) NOT NULL,
	`removespaces`	integer NOT NULL,
	`spliteachchar`	integer NOT NULL,
	`righttoleft`	integer NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `django_site` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	varchar ( 50 ) NOT NULL,
	`domain`	varchar ( 100 ) NOT NULL UNIQUE
);
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
CREATE TABLE IF NOT EXISTS `django_session` (
	`session_key`	varchar ( 40 ) NOT NULL,
	`session_data`	text NOT NULL,
	`expire_date`	datetime NOT NULL,
	PRIMARY KEY(`session_key`)
);
CREATE TABLE IF NOT EXISTS `django_migrations` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`app`	varchar ( 255 ) NOT NULL,
	`name`	varchar ( 255 ) NOT NULL,
	`applied`	datetime NOT NULL
);
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-10-01 07:24:36.053632');
INSERT INTO `django_migrations` VALUES (2,'auth','0001_initial','2017-10-01 07:24:36.297404');
INSERT INTO `django_migrations` VALUES (3,'admin','0001_initial','2017-10-01 07:24:36.541369');
INSERT INTO `django_migrations` VALUES (4,'admin','0002_logentry_remove_auto_add','2017-10-01 07:24:36.785670');
INSERT INTO `django_migrations` VALUES (5,'contenttypes','0002_remove_content_type_name','2017-10-01 07:24:37.073149');
INSERT INTO `django_migrations` VALUES (6,'auth','0002_alter_permission_name_max_length','2017-10-01 07:24:37.295128');
INSERT INTO `django_migrations` VALUES (7,'auth','0003_alter_user_email_max_length','2017-10-01 07:24:37.841359');
INSERT INTO `django_migrations` VALUES (8,'auth','0004_alter_user_username_opts','2017-10-01 07:24:38.063414');
INSERT INTO `django_migrations` VALUES (9,'auth','0005_alter_user_last_login_null','2017-10-01 07:24:38.306953');
INSERT INTO `django_migrations` VALUES (10,'auth','0006_require_contenttypes_0002','2017-10-01 07:24:38.412347');
INSERT INTO `django_migrations` VALUES (11,'auth','0007_alter_validators_add_error_messages','2017-10-01 07:24:38.633917');
INSERT INTO `django_migrations` VALUES (12,'auth','0008_alter_user_username_max_length','2017-10-01 07:24:38.878369');
INSERT INTO `django_migrations` VALUES (13,'lwt','0001_initial','2017-10-01 07:24:41.431124');
INSERT INTO `django_migrations` VALUES (14,'sessions','0001_initial','2017-10-01 07:24:41.652800');
INSERT INTO `django_migrations` VALUES (15,'sites','0001_initial','2017-10-01 07:24:41.863718');
INSERT INTO `django_migrations` VALUES (16,'sites','0002_alter_domain_unique','2017-10-01 07:24:42.074580');
INSERT INTO `django_migrations` VALUES (17,'account','0001_initial','2017-10-01 07:25:44.856302');
INSERT INTO `django_migrations` VALUES (18,'account','0002_email_max_length','2017-10-01 07:25:45.188112');
INSERT INTO `django_migrations` VALUES (19,'socialaccount','0001_initial','2017-10-01 07:25:45.597057');
INSERT INTO `django_migrations` VALUES (20,'socialaccount','0002_token_max_lengths','2017-10-01 07:25:45.906914');
INSERT INTO `django_migrations` VALUES (21,'socialaccount','0003_extra_data_default_dict','2017-10-01 07:25:46.162211');
CREATE TABLE IF NOT EXISTS `django_content_type` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`app_label`	varchar ( 100 ) NOT NULL,
	`model`	varchar ( 100 ) NOT NULL
);
INSERT INTO `django_content_type` VALUES (1,'admin','logentry');
INSERT INTO `django_content_type` VALUES (2,'auth','permission');
INSERT INTO `django_content_type` VALUES (3,'auth','group');
INSERT INTO `django_content_type` VALUES (4,'auth','user');
INSERT INTO `django_content_type` VALUES (5,'contenttypes','contenttype');
INSERT INTO `django_content_type` VALUES (6,'sessions','session');
INSERT INTO `django_content_type` VALUES (7,'sites','site');
INSERT INTO `django_content_type` VALUES (8,'lwt','grouper_of_same_words');
INSERT INTO `django_content_type` VALUES (9,'lwt','languages');
INSERT INTO `django_content_type` VALUES (10,'lwt','sentences');
INSERT INTO `django_content_type` VALUES (11,'lwt','settings_archivedtexts_per_page');
INSERT INTO `django_content_type` VALUES (12,'lwt','settings_currentarchivepage');
INSERT INTO `django_content_type` VALUES (13,'lwt','settings_currentarchivequery');
INSERT INTO `django_content_type` VALUES (14,'lwt','settings_currentarchivetexttag1');
INSERT INTO `django_content_type` VALUES (15,'lwt','settings_currentarchivetexttag12');
INSERT INTO `django_content_type` VALUES (16,'lwt','settings_currentarchivetexttag2');
INSERT INTO `django_content_type` VALUES (17,'lwt','settings_currentlang_id');
INSERT INTO `django_content_type` VALUES (18,'lwt','settings_currentlang_name');
INSERT INTO `django_content_type` VALUES (19,'lwt','settings_currenttext_id');
INSERT INTO `django_content_type` VALUES (20,'lwt','settings_currenttextpage');
INSERT INTO `django_content_type` VALUES (21,'lwt','settings_currenttextquery');
INSERT INTO `django_content_type` VALUES (22,'lwt','settings_currenttextsort');
INSERT INTO `django_content_type` VALUES (23,'lwt','settings_currentwordpage');
INSERT INTO `django_content_type` VALUES (24,'lwt','settings_currentwordquery');
INSERT INTO `django_content_type` VALUES (25,'lwt','settings_currentwordsort');
INSERT INTO `django_content_type` VALUES (26,'lwt','settings_currentwordstatus');
INSERT INTO `django_content_type` VALUES (27,'lwt','settings_currentwordtag1');
INSERT INTO `django_content_type` VALUES (28,'lwt','settings_currentwordtag12');
INSERT INTO `django_content_type` VALUES (29,'lwt','settings_currentwordtag2');
INSERT INTO `django_content_type` VALUES (30,'lwt','settings_mobile_display_mode');
INSERT INTO `django_content_type` VALUES (31,'lwt','settings_show_all_words');
INSERT INTO `django_content_type` VALUES (32,'lwt','settings_show_text_word_counts');
INSERT INTO `django_content_type` VALUES (33,'lwt','settings_similar_terms_count');
INSERT INTO `django_content_type` VALUES (34,'lwt','settings_tags_per_page');
INSERT INTO `django_content_type` VALUES (35,'lwt','settings_term_sentence_count');
INSERT INTO `django_content_type` VALUES (36,'lwt','settings_term_translation_delimiters');
INSERT INTO `django_content_type` VALUES (37,'lwt','settings_terms_per_page');
INSERT INTO `django_content_type` VALUES (38,'lwt','settings_test_edit_frame_waiting_time');
INSERT INTO `django_content_type` VALUES (39,'lwt','settings_test_h_frameheight');
INSERT INTO `django_content_type` VALUES (40,'lwt','settings_test_l_framewidth_percent');
INSERT INTO `django_content_type` VALUES (41,'lwt','settings_test_main_frame_waiting_time');
INSERT INTO `django_content_type` VALUES (42,'lwt','settings_test_r_frameheight_percent');
INSERT INTO `django_content_type` VALUES (43,'lwt','settings_test_sentence_count');
INSERT INTO `django_content_type` VALUES (44,'lwt','settings_text_h_frameheight_no_audio');
INSERT INTO `django_content_type` VALUES (45,'lwt','settings_text_h_frameheight_with_audio');
INSERT INTO `django_content_type` VALUES (46,'lwt','settings_text_l_framewidth_percent');
INSERT INTO `django_content_type` VALUES (47,'lwt','settings_text_r_frameheight_percent');
INSERT INTO `django_content_type` VALUES (48,'lwt','settings_text_visit_statuses_via_key');
INSERT INTO `django_content_type` VALUES (49,'lwt','settings_texts_per_page');
INSERT INTO `django_content_type` VALUES (50,'lwt','texts');
INSERT INTO `django_content_type` VALUES (51,'lwt','texttags');
INSERT INTO `django_content_type` VALUES (52,'lwt','words');
INSERT INTO `django_content_type` VALUES (53,'lwt','wordtags');
INSERT INTO `django_content_type` VALUES (54,'account','emailaddress');
INSERT INTO `django_content_type` VALUES (55,'account','emailconfirmation');
INSERT INTO `django_content_type` VALUES (56,'socialaccount','socialaccount');
INSERT INTO `django_content_type` VALUES (57,'socialaccount','socialapp');
INSERT INTO `django_content_type` VALUES (58,'socialaccount','socialtoken');
CREATE TABLE IF NOT EXISTS `django_admin_log` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`object_id`	text,
	`object_repr`	varchar ( 200 ) NOT NULL,
	`action_flag`	smallint unsigned NOT NULL,
	`change_message`	text NOT NULL,
	`content_type_id`	integer,
	`user_id`	integer NOT NULL,
	`action_time`	datetime NOT NULL,
	FOREIGN KEY(`user_id`) REFERENCES `auth_user`(`id`),
	FOREIGN KEY(`content_type_id`) REFERENCES `django_content_type`(`id`)
);
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`user_id`	integer NOT NULL,
	`permission_id`	integer NOT NULL,
	FOREIGN KEY(`user_id`) REFERENCES `auth_user`(`id`),
	FOREIGN KEY(`permission_id`) REFERENCES `auth_permission`(`id`)
);
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`user_id`	integer NOT NULL,
	`group_id`	integer NOT NULL,
	FOREIGN KEY(`user_id`) REFERENCES `auth_user`(`id`),
	FOREIGN KEY(`group_id`) REFERENCES `auth_group`(`id`)
);
CREATE TABLE IF NOT EXISTS `auth_user` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`password`	varchar ( 128 ) NOT NULL,
	`last_login`	datetime,
	`is_superuser`	bool NOT NULL,
	`first_name`	varchar ( 30 ) NOT NULL,
	`last_name`	varchar ( 30 ) NOT NULL,
	`email`	varchar ( 254 ) NOT NULL,
	`is_staff`	bool NOT NULL,
	`is_active`	bool NOT NULL,
	`date_joined`	datetime NOT NULL,
	`username`	varchar ( 150 ) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS `auth_permission` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`content_type_id`	integer NOT NULL,
	`codename`	varchar ( 100 ) NOT NULL,
	`name`	varchar ( 255 ) NOT NULL,
	FOREIGN KEY(`content_type_id`) REFERENCES `django_content_type`(`id`)
);
INSERT INTO `auth_permission` VALUES (1,1,'add_logentry','Can add log entry');
INSERT INTO `auth_permission` VALUES (2,1,'change_logentry','Can change log entry');
INSERT INTO `auth_permission` VALUES (3,1,'delete_logentry','Can delete log entry');
INSERT INTO `auth_permission` VALUES (4,2,'add_permission','Can add permission');
INSERT INTO `auth_permission` VALUES (5,2,'change_permission','Can change permission');
INSERT INTO `auth_permission` VALUES (6,2,'delete_permission','Can delete permission');
INSERT INTO `auth_permission` VALUES (7,3,'add_group','Can add group');
INSERT INTO `auth_permission` VALUES (8,3,'change_group','Can change group');
INSERT INTO `auth_permission` VALUES (9,3,'delete_group','Can delete group');
INSERT INTO `auth_permission` VALUES (10,4,'add_user','Can add user');
INSERT INTO `auth_permission` VALUES (11,4,'change_user','Can change user');
INSERT INTO `auth_permission` VALUES (12,4,'delete_user','Can delete user');
INSERT INTO `auth_permission` VALUES (13,5,'add_contenttype','Can add content type');
INSERT INTO `auth_permission` VALUES (14,5,'change_contenttype','Can change content type');
INSERT INTO `auth_permission` VALUES (15,5,'delete_contenttype','Can delete content type');
INSERT INTO `auth_permission` VALUES (16,6,'add_session','Can add session');
INSERT INTO `auth_permission` VALUES (17,6,'change_session','Can change session');
INSERT INTO `auth_permission` VALUES (18,6,'delete_session','Can delete session');
INSERT INTO `auth_permission` VALUES (19,7,'add_site','Can add site');
INSERT INTO `auth_permission` VALUES (20,7,'change_site','Can change site');
INSERT INTO `auth_permission` VALUES (21,7,'delete_site','Can delete site');
INSERT INTO `auth_permission` VALUES (22,8,'add_grouper_of_same_words','Can add grouper_of_same_words');
INSERT INTO `auth_permission` VALUES (23,8,'change_grouper_of_same_words','Can change grouper_of_same_words');
INSERT INTO `auth_permission` VALUES (24,8,'delete_grouper_of_same_words','Can delete grouper_of_same_words');
INSERT INTO `auth_permission` VALUES (25,9,'add_languages','Can add languages');
INSERT INTO `auth_permission` VALUES (26,9,'change_languages','Can change languages');
INSERT INTO `auth_permission` VALUES (27,9,'delete_languages','Can delete languages');
INSERT INTO `auth_permission` VALUES (28,10,'add_sentences','Can add sentences');
INSERT INTO `auth_permission` VALUES (29,10,'change_sentences','Can change sentences');
INSERT INTO `auth_permission` VALUES (30,10,'delete_sentences','Can delete sentences');
INSERT INTO `auth_permission` VALUES (31,11,'add_settings_archivedtexts_per_page','Can add settings_archivedtexts_per_page');
INSERT INTO `auth_permission` VALUES (32,11,'change_settings_archivedtexts_per_page','Can change settings_archivedtexts_per_page');
INSERT INTO `auth_permission` VALUES (33,11,'delete_settings_archivedtexts_per_page','Can delete settings_archivedtexts_per_page');
INSERT INTO `auth_permission` VALUES (34,12,'add_settings_currentarchivepage','Can add settings_currentarchivepage');
INSERT INTO `auth_permission` VALUES (35,12,'change_settings_currentarchivepage','Can change settings_currentarchivepage');
INSERT INTO `auth_permission` VALUES (36,12,'delete_settings_currentarchivepage','Can delete settings_currentarchivepage');
INSERT INTO `auth_permission` VALUES (37,13,'add_settings_currentarchivequery','Can add settings_currentarchivequery');
INSERT INTO `auth_permission` VALUES (38,13,'change_settings_currentarchivequery','Can change settings_currentarchivequery');
INSERT INTO `auth_permission` VALUES (39,13,'delete_settings_currentarchivequery','Can delete settings_currentarchivequery');
INSERT INTO `auth_permission` VALUES (40,14,'add_settings_currentarchivetexttag1','Can add settings_currentarchivetexttag1');
INSERT INTO `auth_permission` VALUES (41,14,'change_settings_currentarchivetexttag1','Can change settings_currentarchivetexttag1');
INSERT INTO `auth_permission` VALUES (42,14,'delete_settings_currentarchivetexttag1','Can delete settings_currentarchivetexttag1');
INSERT INTO `auth_permission` VALUES (43,15,'add_settings_currentarchivetexttag12','Can add settings_currentarchivetexttag12');
INSERT INTO `auth_permission` VALUES (44,15,'change_settings_currentarchivetexttag12','Can change settings_currentarchivetexttag12');
INSERT INTO `auth_permission` VALUES (45,15,'delete_settings_currentarchivetexttag12','Can delete settings_currentarchivetexttag12');
INSERT INTO `auth_permission` VALUES (46,16,'add_settings_currentarchivetexttag2','Can add settings_currentarchivetexttag2');
INSERT INTO `auth_permission` VALUES (47,16,'change_settings_currentarchivetexttag2','Can change settings_currentarchivetexttag2');
INSERT INTO `auth_permission` VALUES (48,16,'delete_settings_currentarchivetexttag2','Can delete settings_currentarchivetexttag2');
INSERT INTO `auth_permission` VALUES (49,17,'add_settings_currentlang_id','Can add settings_currentlang_id');
INSERT INTO `auth_permission` VALUES (50,17,'change_settings_currentlang_id','Can change settings_currentlang_id');
INSERT INTO `auth_permission` VALUES (51,17,'delete_settings_currentlang_id','Can delete settings_currentlang_id');
INSERT INTO `auth_permission` VALUES (52,18,'add_settings_currentlang_name','Can add settings_currentlang_name');
INSERT INTO `auth_permission` VALUES (53,18,'change_settings_currentlang_name','Can change settings_currentlang_name');
INSERT INTO `auth_permission` VALUES (54,18,'delete_settings_currentlang_name','Can delete settings_currentlang_name');
INSERT INTO `auth_permission` VALUES (55,19,'add_settings_currenttext_id','Can add settings_currenttext_id');
INSERT INTO `auth_permission` VALUES (56,19,'change_settings_currenttext_id','Can change settings_currenttext_id');
INSERT INTO `auth_permission` VALUES (57,19,'delete_settings_currenttext_id','Can delete settings_currenttext_id');
INSERT INTO `auth_permission` VALUES (58,20,'add_settings_currenttextpage','Can add settings_currenttextpage');
INSERT INTO `auth_permission` VALUES (59,20,'change_settings_currenttextpage','Can change settings_currenttextpage');
INSERT INTO `auth_permission` VALUES (60,20,'delete_settings_currenttextpage','Can delete settings_currenttextpage');
INSERT INTO `auth_permission` VALUES (61,21,'add_settings_currenttextquery','Can add settings_currenttextquery');
INSERT INTO `auth_permission` VALUES (62,21,'change_settings_currenttextquery','Can change settings_currenttextquery');
INSERT INTO `auth_permission` VALUES (63,21,'delete_settings_currenttextquery','Can delete settings_currenttextquery');
INSERT INTO `auth_permission` VALUES (64,22,'add_settings_currenttextsort','Can add settings_currenttextsort');
INSERT INTO `auth_permission` VALUES (65,22,'change_settings_currenttextsort','Can change settings_currenttextsort');
INSERT INTO `auth_permission` VALUES (66,22,'delete_settings_currenttextsort','Can delete settings_currenttextsort');
INSERT INTO `auth_permission` VALUES (67,23,'add_settings_currentwordpage','Can add settings_currentwordpage');
INSERT INTO `auth_permission` VALUES (68,23,'change_settings_currentwordpage','Can change settings_currentwordpage');
INSERT INTO `auth_permission` VALUES (69,23,'delete_settings_currentwordpage','Can delete settings_currentwordpage');
INSERT INTO `auth_permission` VALUES (70,24,'add_settings_currentwordquery','Can add settings_currentwordquery');
INSERT INTO `auth_permission` VALUES (71,24,'change_settings_currentwordquery','Can change settings_currentwordquery');
INSERT INTO `auth_permission` VALUES (72,24,'delete_settings_currentwordquery','Can delete settings_currentwordquery');
INSERT INTO `auth_permission` VALUES (73,25,'add_settings_currentwordsort','Can add settings_currentwordsort');
INSERT INTO `auth_permission` VALUES (74,25,'change_settings_currentwordsort','Can change settings_currentwordsort');
INSERT INTO `auth_permission` VALUES (75,25,'delete_settings_currentwordsort','Can delete settings_currentwordsort');
INSERT INTO `auth_permission` VALUES (76,26,'add_settings_currentwordstatus','Can add settings_currentwordstatus');
INSERT INTO `auth_permission` VALUES (77,26,'change_settings_currentwordstatus','Can change settings_currentwordstatus');
INSERT INTO `auth_permission` VALUES (78,26,'delete_settings_currentwordstatus','Can delete settings_currentwordstatus');
INSERT INTO `auth_permission` VALUES (79,27,'add_settings_currentwordtag1','Can add settings_currentwordtag1');
INSERT INTO `auth_permission` VALUES (80,27,'change_settings_currentwordtag1','Can change settings_currentwordtag1');
INSERT INTO `auth_permission` VALUES (81,27,'delete_settings_currentwordtag1','Can delete settings_currentwordtag1');
INSERT INTO `auth_permission` VALUES (82,28,'add_settings_currentwordtag12','Can add settings_currentwordtag12');
INSERT INTO `auth_permission` VALUES (83,28,'change_settings_currentwordtag12','Can change settings_currentwordtag12');
INSERT INTO `auth_permission` VALUES (84,28,'delete_settings_currentwordtag12','Can delete settings_currentwordtag12');
INSERT INTO `auth_permission` VALUES (85,29,'add_settings_currentwordtag2','Can add settings_currentwordtag2');
INSERT INTO `auth_permission` VALUES (86,29,'change_settings_currentwordtag2','Can change settings_currentwordtag2');
INSERT INTO `auth_permission` VALUES (87,29,'delete_settings_currentwordtag2','Can delete settings_currentwordtag2');
INSERT INTO `auth_permission` VALUES (88,30,'add_settings_mobile_display_mode','Can add settings_mobile_display_mode');
INSERT INTO `auth_permission` VALUES (89,30,'change_settings_mobile_display_mode','Can change settings_mobile_display_mode');
INSERT INTO `auth_permission` VALUES (90,30,'delete_settings_mobile_display_mode','Can delete settings_mobile_display_mode');
INSERT INTO `auth_permission` VALUES (91,31,'add_settings_show_all_words','Can add settings_show_all_words');
INSERT INTO `auth_permission` VALUES (92,31,'change_settings_show_all_words','Can change settings_show_all_words');
INSERT INTO `auth_permission` VALUES (93,31,'delete_settings_show_all_words','Can delete settings_show_all_words');
INSERT INTO `auth_permission` VALUES (94,32,'add_settings_show_text_word_counts','Can add settings_show_text_word_counts');
INSERT INTO `auth_permission` VALUES (95,32,'change_settings_show_text_word_counts','Can change settings_show_text_word_counts');
INSERT INTO `auth_permission` VALUES (96,32,'delete_settings_show_text_word_counts','Can delete settings_show_text_word_counts');
INSERT INTO `auth_permission` VALUES (97,33,'add_settings_similar_terms_count','Can add settings_similar_terms_count');
INSERT INTO `auth_permission` VALUES (98,33,'change_settings_similar_terms_count','Can change settings_similar_terms_count');
INSERT INTO `auth_permission` VALUES (99,33,'delete_settings_similar_terms_count','Can delete settings_similar_terms_count');
INSERT INTO `auth_permission` VALUES (100,34,'add_settings_tags_per_page','Can add settings_tags_per_page');
INSERT INTO `auth_permission` VALUES (101,34,'change_settings_tags_per_page','Can change settings_tags_per_page');
INSERT INTO `auth_permission` VALUES (102,34,'delete_settings_tags_per_page','Can delete settings_tags_per_page');
INSERT INTO `auth_permission` VALUES (103,35,'add_settings_term_sentence_count','Can add settings_term_sentence_count');
INSERT INTO `auth_permission` VALUES (104,35,'change_settings_term_sentence_count','Can change settings_term_sentence_count');
INSERT INTO `auth_permission` VALUES (105,35,'delete_settings_term_sentence_count','Can delete settings_term_sentence_count');
INSERT INTO `auth_permission` VALUES (106,36,'add_settings_term_translation_delimiters','Can add settings_term_translation_delimiters');
INSERT INTO `auth_permission` VALUES (107,36,'change_settings_term_translation_delimiters','Can change settings_term_translation_delimiters');
INSERT INTO `auth_permission` VALUES (108,36,'delete_settings_term_translation_delimiters','Can delete settings_term_translation_delimiters');
INSERT INTO `auth_permission` VALUES (109,37,'add_settings_terms_per_page','Can add settings_terms_per_page');
INSERT INTO `auth_permission` VALUES (110,37,'change_settings_terms_per_page','Can change settings_terms_per_page');
INSERT INTO `auth_permission` VALUES (111,37,'delete_settings_terms_per_page','Can delete settings_terms_per_page');
INSERT INTO `auth_permission` VALUES (112,38,'add_settings_test_edit_frame_waiting_time','Can add settings_test_edit_frame_waiting_time');
INSERT INTO `auth_permission` VALUES (113,38,'change_settings_test_edit_frame_waiting_time','Can change settings_test_edit_frame_waiting_time');
INSERT INTO `auth_permission` VALUES (114,38,'delete_settings_test_edit_frame_waiting_time','Can delete settings_test_edit_frame_waiting_time');
INSERT INTO `auth_permission` VALUES (115,39,'add_settings_test_h_frameheight','Can add settings_test_h_frameheight');
INSERT INTO `auth_permission` VALUES (116,39,'change_settings_test_h_frameheight','Can change settings_test_h_frameheight');
INSERT INTO `auth_permission` VALUES (117,39,'delete_settings_test_h_frameheight','Can delete settings_test_h_frameheight');
INSERT INTO `auth_permission` VALUES (118,40,'add_settings_test_l_framewidth_percent','Can add settings_test_l_framewidth_percent');
INSERT INTO `auth_permission` VALUES (119,40,'change_settings_test_l_framewidth_percent','Can change settings_test_l_framewidth_percent');
INSERT INTO `auth_permission` VALUES (120,40,'delete_settings_test_l_framewidth_percent','Can delete settings_test_l_framewidth_percent');
INSERT INTO `auth_permission` VALUES (121,41,'add_settings_test_main_frame_waiting_time','Can add settings_test_main_frame_waiting_time');
INSERT INTO `auth_permission` VALUES (122,41,'change_settings_test_main_frame_waiting_time','Can change settings_test_main_frame_waiting_time');
INSERT INTO `auth_permission` VALUES (123,41,'delete_settings_test_main_frame_waiting_time','Can delete settings_test_main_frame_waiting_time');
INSERT INTO `auth_permission` VALUES (124,42,'add_settings_test_r_frameheight_percent','Can add settings_test_r_frameheight_percent');
INSERT INTO `auth_permission` VALUES (125,42,'change_settings_test_r_frameheight_percent','Can change settings_test_r_frameheight_percent');
INSERT INTO `auth_permission` VALUES (126,42,'delete_settings_test_r_frameheight_percent','Can delete settings_test_r_frameheight_percent');
INSERT INTO `auth_permission` VALUES (127,43,'add_settings_test_sentence_count','Can add settings_test_sentence_count');
INSERT INTO `auth_permission` VALUES (128,43,'change_settings_test_sentence_count','Can change settings_test_sentence_count');
INSERT INTO `auth_permission` VALUES (129,43,'delete_settings_test_sentence_count','Can delete settings_test_sentence_count');
INSERT INTO `auth_permission` VALUES (130,44,'add_settings_text_h_frameheight_no_audio','Can add settings_text_h_frameheight_no_audio');
INSERT INTO `auth_permission` VALUES (131,44,'change_settings_text_h_frameheight_no_audio','Can change settings_text_h_frameheight_no_audio');
INSERT INTO `auth_permission` VALUES (132,44,'delete_settings_text_h_frameheight_no_audio','Can delete settings_text_h_frameheight_no_audio');
INSERT INTO `auth_permission` VALUES (133,45,'add_settings_text_h_frameheight_with_audio','Can add settings_text_h_frameheight_with_audio');
INSERT INTO `auth_permission` VALUES (134,45,'change_settings_text_h_frameheight_with_audio','Can change settings_text_h_frameheight_with_audio');
INSERT INTO `auth_permission` VALUES (135,45,'delete_settings_text_h_frameheight_with_audio','Can delete settings_text_h_frameheight_with_audio');
INSERT INTO `auth_permission` VALUES (136,46,'add_settings_text_l_framewidth_percent','Can add settings_text_l_framewidth_percent');
INSERT INTO `auth_permission` VALUES (137,46,'change_settings_text_l_framewidth_percent','Can change settings_text_l_framewidth_percent');
INSERT INTO `auth_permission` VALUES (138,46,'delete_settings_text_l_framewidth_percent','Can delete settings_text_l_framewidth_percent');
INSERT INTO `auth_permission` VALUES (139,47,'add_settings_text_r_frameheight_percent','Can add settings_text_r_frameheight_percent');
INSERT INTO `auth_permission` VALUES (140,47,'change_settings_text_r_frameheight_percent','Can change settings_text_r_frameheight_percent');
INSERT INTO `auth_permission` VALUES (141,47,'delete_settings_text_r_frameheight_percent','Can delete settings_text_r_frameheight_percent');
INSERT INTO `auth_permission` VALUES (142,48,'add_settings_text_visit_statuses_via_key','Can add settings_text_visit_statuses_via_key');
INSERT INTO `auth_permission` VALUES (143,48,'change_settings_text_visit_statuses_via_key','Can change settings_text_visit_statuses_via_key');
INSERT INTO `auth_permission` VALUES (144,48,'delete_settings_text_visit_statuses_via_key','Can delete settings_text_visit_statuses_via_key');
INSERT INTO `auth_permission` VALUES (145,49,'add_settings_texts_per_page','Can add settings_texts_per_page');
INSERT INTO `auth_permission` VALUES (146,49,'change_settings_texts_per_page','Can change settings_texts_per_page');
INSERT INTO `auth_permission` VALUES (147,49,'delete_settings_texts_per_page','Can delete settings_texts_per_page');
INSERT INTO `auth_permission` VALUES (148,50,'add_texts','Can add texts');
INSERT INTO `auth_permission` VALUES (149,50,'change_texts','Can change texts');
INSERT INTO `auth_permission` VALUES (150,50,'delete_texts','Can delete texts');
INSERT INTO `auth_permission` VALUES (151,51,'add_texttags','Can add texttags');
INSERT INTO `auth_permission` VALUES (152,51,'change_texttags','Can change texttags');
INSERT INTO `auth_permission` VALUES (153,51,'delete_texttags','Can delete texttags');
INSERT INTO `auth_permission` VALUES (154,52,'add_words','Can add words');
INSERT INTO `auth_permission` VALUES (155,52,'change_words','Can change words');
INSERT INTO `auth_permission` VALUES (156,52,'delete_words','Can delete words');
INSERT INTO `auth_permission` VALUES (157,53,'add_wordtags','Can add wordtags');
INSERT INTO `auth_permission` VALUES (158,53,'change_wordtags','Can change wordtags');
INSERT INTO `auth_permission` VALUES (159,53,'delete_wordtags','Can delete wordtags');
INSERT INTO `auth_permission` VALUES (160,54,'add_emailaddress','Can add email address');
INSERT INTO `auth_permission` VALUES (161,54,'change_emailaddress','Can change email address');
INSERT INTO `auth_permission` VALUES (162,54,'delete_emailaddress','Can delete email address');
INSERT INTO `auth_permission` VALUES (163,55,'add_emailconfirmation','Can add email confirmation');
INSERT INTO `auth_permission` VALUES (164,55,'change_emailconfirmation','Can change email confirmation');
INSERT INTO `auth_permission` VALUES (165,55,'delete_emailconfirmation','Can delete email confirmation');
INSERT INTO `auth_permission` VALUES (166,56,'add_socialaccount','Can add social account');
INSERT INTO `auth_permission` VALUES (167,56,'change_socialaccount','Can change social account');
INSERT INTO `auth_permission` VALUES (168,56,'delete_socialaccount','Can delete social account');
INSERT INTO `auth_permission` VALUES (169,57,'add_socialapp','Can add social application');
INSERT INTO `auth_permission` VALUES (170,57,'change_socialapp','Can change social application');
INSERT INTO `auth_permission` VALUES (171,57,'delete_socialapp','Can delete social application');
INSERT INTO `auth_permission` VALUES (172,58,'add_socialtoken','Can add social application token');
INSERT INTO `auth_permission` VALUES (173,58,'change_socialtoken','Can change social application token');
INSERT INTO `auth_permission` VALUES (174,58,'delete_socialtoken','Can delete social application token');
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`group_id`	integer NOT NULL,
	`permission_id`	integer NOT NULL,
	FOREIGN KEY(`group_id`) REFERENCES `auth_group`(`id`),
	FOREIGN KEY(`permission_id`) REFERENCES `auth_permission`(`id`)
);
CREATE TABLE IF NOT EXISTS `auth_group` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	varchar ( 80 ) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS `account_emailconfirmation` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`created`	datetime NOT NULL,
	`sent`	datetime,
	`key`	varchar ( 64 ) NOT NULL UNIQUE,
	`email_address_id`	integer NOT NULL,
	FOREIGN KEY(`email_address_id`) REFERENCES `account_emailaddress`(`id`)
);
CREATE TABLE IF NOT EXISTS `account_emailaddress` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`verified`	bool NOT NULL,
	`primary`	bool NOT NULL,
	`user_id`	integer NOT NULL,
	`email`	varchar ( 254 ) NOT NULL UNIQUE,
	FOREIGN KEY(`user_id`) REFERENCES `auth_user`(`id`)
);
CREATE TABLE IF NOT EXISTS `Grouper_of_same_words` (
	`created_date`	datetime NOT NULL,
	`modified_date`	datetime NOT NULL,
	`id`	integer NOT NULL,
	`owner_id`	integer NOT NULL,
	FOREIGN KEY(`owner_id`) REFERENCES `auth_user`(`id`),
	PRIMARY KEY(`id`)
);
CREATE INDEX IF NOT EXISTS `wordtags_owner_id_7563889b` ON `wordtags` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `words_wordtags_wordtags_id_6ae9ef2c` ON `words_wordtags` (
	`wordtags_id`
);
CREATE UNIQUE INDEX IF NOT EXISTS `words_wordtags_words_id_wordtags_id_1e7d9918_uniq` ON `words_wordtags` (
	`words_id`,
	`wordtags_id`
);
CREATE INDEX IF NOT EXISTS `words_wordtags_words_id_daf3efff` ON `words_wordtags` (
	`words_id`
);
CREATE INDEX IF NOT EXISTS `words_text_id_6e518423` ON `words` (
	`text_id`
);
CREATE INDEX IF NOT EXISTS `words_sentence_id_c57b6da1` ON `words` (
	`sentence_id`
);
CREATE INDEX IF NOT EXISTS `words_owner_id_fde1fb06` ON `words` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `words_language_id_947d8eac` ON `words` (
	`language_id`
);
CREATE INDEX IF NOT EXISTS `words_grouper_of_same_words_id_743c64b9` ON `words` (
	`grouper_of_same_words_id`
);
CREATE INDEX IF NOT EXISTS `words_compoundword_id_26771cbf` ON `words` (
	`compoundword_id`
);
CREATE INDEX IF NOT EXISTS `texttags_owner_id_4c2d9b21` ON `texttags` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `texts_texttags_texttags_id_b7709475` ON `texts_texttags` (
	`texttags_id`
);
CREATE UNIQUE INDEX IF NOT EXISTS `texts_texttags_texts_id_texttags_id_2ff95f7a_uniq` ON `texts_texttags` (
	`texts_id`,
	`texttags_id`
);
CREATE INDEX IF NOT EXISTS `texts_texttags_texts_id_85417bc1` ON `texts_texttags` (
	`texts_id`
);
CREATE INDEX IF NOT EXISTS `texts_owner_id_a19eb88a` ON `texts` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `texts_language_id_6979385a` ON `texts` (
	`language_id`
);
CREATE UNIQUE INDEX IF NOT EXISTS `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` ON `socialaccount_socialtoken` (
	`app_id`,
	`account_id`
);
CREATE INDEX IF NOT EXISTS `socialaccount_socialtoken_app_id_636a42d7` ON `socialaccount_socialtoken` (
	`app_id`
);
CREATE INDEX IF NOT EXISTS `socialaccount_socialtoken_account_id_951f210e` ON `socialaccount_socialtoken` (
	`account_id`
);
CREATE UNIQUE INDEX IF NOT EXISTS `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` ON `socialaccount_socialapp_sites` (
	`socialapp_id`,
	`site_id`
);
CREATE INDEX IF NOT EXISTS `socialaccount_socialapp_sites_socialapp_id_97fb6e7d` ON `socialaccount_socialapp_sites` (
	`socialapp_id`
);
CREATE INDEX IF NOT EXISTS `socialaccount_socialapp_sites_site_id_2579dee5` ON `socialaccount_socialapp_sites` (
	`site_id`
);
CREATE INDEX IF NOT EXISTS `socialaccount_socialaccount_user_id_8146e70c` ON `socialaccount_socialaccount` (
	`user_id`
);
CREATE UNIQUE INDEX IF NOT EXISTS `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` ON `socialaccount_socialaccount` (
	`provider`,
	`uid`
);
CREATE INDEX IF NOT EXISTS `sentences_text_id_b79ef097` ON `sentences` (
	`text_id`
);
CREATE INDEX IF NOT EXISTS `sentences_owner_id_77428696` ON `sentences` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `sentences_language_id_1c84a94e` ON `sentences` (
	`language_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_texts_per_page_owner_id_19250112` ON `lwt_settings_texts_per_page` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_text_visit_statuses_via_key_owner_id_960609a4` ON `lwt_settings_text_visit_statuses_via_key` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_text_r_frameheight_percent_owner_id_3ee99d08` ON `lwt_settings_text_r_frameheight_percent` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_text_l_framewidth_percent_owner_id_6cb7ce4d` ON `lwt_settings_text_l_framewidth_percent` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_text_h_frameheight_with_audio_owner_id_8abd9026` ON `lwt_settings_text_h_frameheight_with_audio` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_text_h_frameheight_no_audio_owner_id_3771ee1b` ON `lwt_settings_text_h_frameheight_no_audio` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_test_sentence_count_owner_id_baa4bd10` ON `lwt_settings_test_sentence_count` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_test_r_frameheight_percent_owner_id_570fdf5a` ON `lwt_settings_test_r_frameheight_percent` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_test_main_frame_waiting_time_owner_id_bc063bd8` ON `lwt_settings_test_main_frame_waiting_time` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_test_l_framewidth_percent_owner_id_86822bff` ON `lwt_settings_test_l_framewidth_percent` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_test_h_frameheight_owner_id_0e4db453` ON `lwt_settings_test_h_frameheight` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_test_edit_frame_waiting_time_owner_id_e05eea2f` ON `lwt_settings_test_edit_frame_waiting_time` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_terms_per_page_owner_id_76e16c2f` ON `lwt_settings_terms_per_page` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_term_translation_delimiters_owner_id_bf9a5b28` ON `lwt_settings_term_translation_delimiters` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_term_sentence_count_owner_id_da83db79` ON `lwt_settings_term_sentence_count` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_tags_per_page_owner_id_a62b8e01` ON `lwt_settings_tags_per_page` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_similar_terms_count_owner_id_e6611958` ON `lwt_settings_similar_terms_count` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_show_text_word_counts_owner_id_a98d9721` ON `lwt_settings_show_text_word_counts` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_show_all_words_owner_id_8d908745` ON `lwt_settings_show_all_words` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_mobile_display_mode_owner_id_4744e5ea` ON `lwt_settings_mobile_display_mode` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currentwordtag2_owner_id_e8386dff` ON `lwt_settings_currentwordtag2` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currentwordtag1_owner_id_5676a19e` ON `lwt_settings_currentwordtag1` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currentwordtag12_owner_id_346c10c1` ON `lwt_settings_currentwordtag12` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currentwordstatus_owner_id_b99153fe` ON `lwt_settings_currentwordstatus` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currentwordsort_owner_id_1c3568dd` ON `lwt_settings_currentwordsort` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currentwordquery_owner_id_44fac600` ON `lwt_settings_currentwordquery` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currentwordpage_owner_id_944c39b2` ON `lwt_settings_currentwordpage` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currenttextsort_owner_id_36dab4f3` ON `lwt_settings_currenttextsort` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currenttextquery_owner_id_b4bf4e79` ON `lwt_settings_currenttextquery` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currenttextpage_owner_id_e4a9c120` ON `lwt_settings_currenttextpage` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currenttext_id_owner_id_db070fb4` ON `lwt_settings_currenttext_id` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currentlang_name_owner_id_b573ba46` ON `lwt_settings_currentlang_name` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currentlang_id_owner_id_5416dc4d` ON `lwt_settings_currentlang_id` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currentarchivetexttag2_owner_id_da93b9d3` ON `lwt_settings_currentarchivetexttag2` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currentarchivetexttag1_owner_id_175b8897` ON `lwt_settings_currentarchivetexttag1` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currentarchivetexttag12_owner_id_5876b38d` ON `lwt_settings_currentarchivetexttag12` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currentarchivequery_owner_id_205eabc0` ON `lwt_settings_currentarchivequery` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_currentarchivepage_owner_id_eee7d915` ON `lwt_settings_currentarchivepage` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lwt_settings_archivedtexts_per_page_owner_id_31cd4dd9` ON `lwt_settings_archivedtexts_per_page` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `languages_owner_id_74c9833a` ON `languages` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `django_session_expire_date_a5c62663` ON `django_session` (
	`expire_date`
);
CREATE UNIQUE INDEX IF NOT EXISTS `django_content_type_app_label_model_76bd3d3b_uniq` ON `django_content_type` (
	`app_label`,
	`model`
);
CREATE INDEX IF NOT EXISTS `django_admin_log_user_id_c564eba6` ON `django_admin_log` (
	`user_id`
);
CREATE INDEX IF NOT EXISTS `django_admin_log_content_type_id_c4bce8eb` ON `django_admin_log` (
	`content_type_id`
);
CREATE UNIQUE INDEX IF NOT EXISTS `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` ON `auth_user_user_permissions` (
	`user_id`,
	`permission_id`
);
CREATE INDEX IF NOT EXISTS `auth_user_user_permissions_user_id_a95ead1b` ON `auth_user_user_permissions` (
	`user_id`
);
CREATE INDEX IF NOT EXISTS `auth_user_user_permissions_permission_id_1fbb5f2c` ON `auth_user_user_permissions` (
	`permission_id`
);
CREATE UNIQUE INDEX IF NOT EXISTS `auth_user_groups_user_id_group_id_94350c0c_uniq` ON `auth_user_groups` (
	`user_id`,
	`group_id`
);
CREATE INDEX IF NOT EXISTS `auth_user_groups_user_id_6a12ed8b` ON `auth_user_groups` (
	`user_id`
);
CREATE INDEX IF NOT EXISTS `auth_user_groups_group_id_97559544` ON `auth_user_groups` (
	`group_id`
);
CREATE UNIQUE INDEX IF NOT EXISTS `auth_permission_content_type_id_codename_01ab375a_uniq` ON `auth_permission` (
	`content_type_id`,
	`codename`
);
CREATE INDEX IF NOT EXISTS `auth_permission_content_type_id_2f476e4b` ON `auth_permission` (
	`content_type_id`
);
CREATE INDEX IF NOT EXISTS `auth_group_permissions_permission_id_84c5c92e` ON `auth_group_permissions` (
	`permission_id`
);
CREATE UNIQUE INDEX IF NOT EXISTS `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` ON `auth_group_permissions` (
	`group_id`,
	`permission_id`
);
CREATE INDEX IF NOT EXISTS `auth_group_permissions_group_id_b120cbf9` ON `auth_group_permissions` (
	`group_id`
);
CREATE INDEX IF NOT EXISTS `account_emailconfirmation_email_address_id_5b7f8c58` ON `account_emailconfirmation` (
	`email_address_id`
);
CREATE INDEX IF NOT EXISTS `account_emailaddress_user_id_2c513194` ON `account_emailaddress` (
	`user_id`
);
CREATE INDEX IF NOT EXISTS `Grouper_of_same_words_owner_id_419ece08` ON `Grouper_of_same_words` (
	`owner_id`
);
COMMIT;
