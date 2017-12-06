-- lwt-backup-2017-10-23-13-29-33.sql.gz

DROP TABLE IF EXISTS languages;
CREATE TABLE `languages` (   `LgID` int(11) unsigned NOT NULL AUTO_INCREMENT,   `LgName` varchar(40) NOT NULL,   `LgDict1URI` varchar(200) NOT NULL,   `LgDict2URI` varchar(200) DEFAULT NULL,   `LgGoogleTranslateURI` varchar(200) DEFAULT NULL,   `LgExportTemplate` varchar(1000) DEFAULT NULL,   `LgTextSize` int(5) unsigned NOT NULL DEFAULT '100',   `LgCharacterSubstitutions` varchar(500) NOT NULL,   `LgRegexpSplitSentences` varchar(500) NOT NULL,   `LgExceptionsSplitSentences` varchar(500) NOT NULL,   `LgRegexpWordCharacters` varchar(500) NOT NULL,   `LgRemoveSpaces` int(1) unsigned NOT NULL DEFAULT '0',   `LgSplitEachChar` int(1) unsigned NOT NULL DEFAULT '0',   `LgRightToLeft` int(1) unsigned NOT NULL DEFAULT '0',   PRIMARY KEY (`LgID`),   UNIQUE KEY `LgName` (`LgName`) ) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
INSERT INTO languages VALUES('8','Hebrew','glosbe_api.php?from=he&dest=en&phrase=###','http://morfix.mako.co.il/default.aspx?q=###','*http://translate.google.com/?ie=UTF-8&sl=iw&tl=en&text=###','$y\\t$t\\n','150','','.!?:;','','\\x{0590}-\\x{05FF}','0','0','1');

DROP TABLE IF EXISTS sentences;
CREATE TABLE `sentences` (   `SeID` int(11) unsigned NOT NULL AUTO_INCREMENT,   `SeLgID` int(11) unsigned NOT NULL,   `SeTxID` int(11) unsigned NOT NULL,   `SeOrder` int(11) unsigned NOT NULL,   `SeText` text,   PRIMARY KEY (`SeID`),   KEY `SeLgID` (`SeLgID`),   KEY `SeTxID` (`SeTxID`),   KEY `SeOrder` (`SeOrder`) ) ENGINE=MyISAM AUTO_INCREMENT=357 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS tags2;
CREATE TABLE `tags2` (   `T2ID` int(11) unsigned NOT NULL AUTO_INCREMENT,   `T2Text` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,   `T2Comment` varchar(200) NOT NULL DEFAULT '',   PRIMARY KEY (`T2ID`),   UNIQUE KEY `T2Text` (`T2Text`) ) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
INSERT INTO tags2 VALUES('1','demo','');
INSERT INTO tags2 VALUES('2','basic','');

DROP TABLE IF EXISTS texts;
CREATE TABLE `texts` (   `TxID` int(11) unsigned NOT NULL AUTO_INCREMENT,   `TxLgID` int(11) unsigned NOT NULL,   `TxTitle` varchar(200) NOT NULL,   `TxText` text NOT NULL,   `TxAnnotatedText` longtext NOT NULL,   `TxAudioURI` varchar(200) DEFAULT NULL,   `TxSourceURI` varchar(1000) DEFAULT NULL,   PRIMARY KEY (`TxID`),   KEY `TxLgID` (`TxLgID`) ) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
INSERT INTO texts VALUES('8','8','Greetings','בוקר טוב\nאחר צהריים טובים\nערב טוב\nלילה טוב\nלהתראות','','http://lwt.sourceforge.net/media/hebrew.mp3',NULL);

DROP TABLE IF EXISTS texttags;
CREATE TABLE `texttags` (   `TtTxID` int(11) unsigned NOT NULL,   `TtT2ID` int(11) unsigned NOT NULL,   PRIMARY KEY (`TtTxID`,`TtT2ID`),   KEY `TtTxID` (`TtTxID`),   KEY `TtT2ID` (`TtT2ID`) ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
INSERT INTO texttags VALUES('8','1');
INSERT INTO texttags VALUES('8','2');

DROP TABLE IF EXISTS words;
CREATE TABLE `words` (   `WoID` int(11) unsigned NOT NULL AUTO_INCREMENT,   `WoLgID` int(11) unsigned NOT NULL,   `WoText` varchar(250) NOT NULL,   `WoTextLC` varchar(250) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,   `WoStatus` tinyint(4) NOT NULL,   `WoTranslation` varchar(500) NOT NULL DEFAULT '*',   `WoRomanization` varchar(100) DEFAULT NULL,   `WoSentence` varchar(1000) DEFAULT NULL,   `WoCreated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,   `WoStatusChanged` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',   `WoTodayScore` double NOT NULL DEFAULT '0',   `WoTomorrowScore` double NOT NULL DEFAULT '0',   `WoRandom` double NOT NULL DEFAULT '0',   PRIMARY KEY (`WoID`),   UNIQUE KEY `WoLgIDTextLC` (`WoLgID`,`WoTextLC`),   KEY `WoLgID` (`WoLgID`),   KEY `WoStatus` (`WoStatus`),   KEY `WoTextLC` (`WoTextLC`),   KEY `WoTranslation` (`WoTranslation`(333)),   KEY `WoCreated` (`WoCreated`),   KEY `WoStatusChanged` (`WoStatusChanged`),   KEY `WoTodayScore` (`WoTodayScore`),   KEY `WoTomorrowScore` (`WoTomorrowScore`),   KEY `WoRandom` (`WoRandom`) ) ENGINE=MyISAM AUTO_INCREMENT=221 DEFAULT CHARSET=utf8;
INSERT INTO words VALUES('152','8','טוב','טוב','1','good','tov','בוקר {טוב}','2011-08-30 12:00:00','2016-01-27 22:21:50','-4432.733031916795','-4439.713713856821','0.02784923000992204');
INSERT INTO words VALUES('153','8','בוקר','בוקר','1','morning','boker','{בוקר} טוב','2011-08-30 12:00:00','2016-01-27 22:21:50','-4432.733031916795','-4439.713713856821','0.7215302025168484');
INSERT INTO words VALUES('154','8','ערב','ערב','1','evening','erev','{ערב} טוב','2011-08-30 12:00:00','2016-01-27 22:21:50','-4432.733031916795','-4439.713713856821','0.524103353288121');
INSERT INTO words VALUES('155','8','לילה','לילה','1','night','laila','{לילה} טוב','2011-08-30 12:00:00','2016-01-27 22:21:50','-4432.733031916795','-4439.713713856821','0.45592618962370435');
INSERT INTO words VALUES('156','8','להתראות','להתראות','1','good bye','lehitraot','{להתראות}','2011-08-30 12:00:00','2016-01-27 22:21:50','-4432.733031916795','-4439.713713856821','0.707320918987804');
INSERT INTO words VALUES('157','8','טובים','טובים','1','good','tovim','אחר צהריים {טובים}','2011-08-30 12:00:00','2016-01-27 22:21:50','-4432.733031916795','-4439.713713856821','0.168826056801552');
INSERT INTO words VALUES('158','8','צהריים','צהריים','1','noon','tzahara\'im','אחר {צהריים} טובים','2011-08-30 12:00:00','2016-01-27 22:21:50','-4432.733031916795','-4439.713713856821','0.722167557777993');
INSERT INTO words VALUES('159','8','אחר','אחר','1','after / other','achar','{אחר} צהריים טובים','2011-08-30 12:00:00','2016-01-27 22:21:50','-4432.733031916795','-4439.713713856821','0.10435964921895383');
INSERT INTO words VALUES('160','8','בוקר טוב','בוקר טוב','1','good morning','boker tov','{בוקר טוב}','2011-09-02 19:00:09','2016-01-27 22:21:50','-4432.733031916795','-4439.713713856821','0.3552956034944352');
INSERT INTO words VALUES('161','8','אחר צהריים טובים','אחר צהריים טובים','1','good afternoon','achar tzahara\'im tovim','{אחר צהריים טובים}','2011-09-02 19:00:50','2016-01-27 22:21:50','-4432.733031916795','-4439.713713856821','0.46339910054895944');
INSERT INTO words VALUES('162','8','ערב טוב','ערב טוב','1','good evening','erev tov','{ערב טוב}','2011-09-02 19:01:21','2016-01-27 22:21:50','-4432.733031916795','-4439.713713856821','0.2511087229951366');
INSERT INTO words VALUES('163','8','לילה טוב','לילה טוב','1','good night','laila tov','{לילה טוב}','2011-09-02 19:01:50','2016-01-27 22:21:50','-4432.733031916795','-4439.713713856821','0.8653463440624497');
INSERT INTO words VALUES('164','8','אחר צהריים','אחר צהריים','1','afternoon','achar tzahara\'im','{אחר צהריים} טובים','2011-09-02 19:21:20','2016-01-27 22:21:50','-4432.733031916795','-4439.713713856821','0.5734055820604839');

