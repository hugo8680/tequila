CREATE TABLE IF NOT EXISTS `t_user`(
	`uid` INT(6) UNSIGNED AUTO_INCREMENT,
	`status` BOOLEAN NOT NULL DEFAULT TRUE,
	`username` VARCHAR(12) NOT NULL,
	`email`  VARCHAR(40) NOT NULL,
	`phone` VARCHAR(11) NULL,
	`password` VARCHAR(40) NOT NULL,
	`point` INT(4) DEFAULT 0,
	`sex` BOOLEAN DEFAULT TRUE,
	`address` VARCHAR(60) NULL,
	CONSTRAINT pk_user_uid PRIMARY KEY (uid),
	UNIQUE (uid, username, email, phone)
)AUTO_INCREMENT=100000;


CREATE TABLE IF NOT EXISTS `t_tag`(
	`tid` INT(6) UNSIGNED AUTO_INCREMENT,
	`status` BOOLEAN NOT NULL DEFAULT TRUE,
	`tag_name` VARCHAR(12) NOT NULL,
	CONSTRAINT pk_tag_tid PRIMARY KEY (tid),
	UNIQUE(tid)
)AUTO_INCREMENT=100000;


CREATE TABLE IF NOT EXISTS `t_question`(
	`qid` INT(6) UNSIGNED AUTO_INCREMENT,
	`status` BOOLEAN NOT NULL DEFAULT TRUE,
	`abstract` VARCHAR(24) NOT NULL,
	`content` VARCHAR(10240) NOT NULL,
	`uid` INT(6) UNSIGNED NOT NULL,
	`tid` INT(6) UNSIGNED NOT NULL,
	CONSTRAINT pk_question_qid PRIMARY KEY (qid),
	CONSTRAINT fk_question_user_uid FOREIGN KEY (uid) REFERENCES t_user (uid),
	CONSTRAINT fk_question_tag_tid FOREIGN KEY (tid) REFERENCES t_tag (tid),
	UNIQUE(qid, uid, tid)
)AUTO_INCREMENT=100000;


CREATE TABLE IF NOT EXISTS `t_answer`(
	`aid` INT(6) UNSIGNED AUTO_INCREMENT,
	`status` BOOLEAN NOT NULL DEFAULT TRUE,
	`content` VARCHAR(4096) NOT NULL,
	`qid` INT(6) UNSIGNED NOT NULL,
	CONSTRAINT pk_answer_aid PRIMARY KEY (aid),
	CONSTRAINT fk_answer_question_qid FOREIGN KEY (qid) REFERENCES t_question (qid),
	UNIQUE(aid, qid)
)AUTO_INCREMENT=100000;


ALTER TABLE t_user ADD INDEX idx_user(username(8), email(8), phone(8));
ALTER TABLE t_question ADD INDEX idx_question(abstract(8), content(8));
ALTER TABLE t_answer ADD INDEX idx_answer(content(8));
ALTER TABLE t_tag ADD INDEX idx_tag(tag_name(2));


INSERT INTO t_user(username, email, password) VALUES (
	'hugo',
	'zhang8680@outlook.com',
	'18f3e922a1d1a9a140efbbe894bc829eeec260d8'
);

INSERT INTO t_tag(tag_name) VALUES ('Python'), ('C#'), ('Docker');
