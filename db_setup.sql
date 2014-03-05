SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE TABLE IF NOT EXISTS `admin_queue` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `user` int(11) NOT NULL,
		  `type` varchar(12) NOT NULL,
		  `entry` int(11) NOT NULL,
		  `field` text NOT NULL,
		  `content` text NOT NULL,
		  PRIMARY KEY (`id`)
		) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=31 ;

CREATE TABLE IF NOT EXISTS `field_names` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `col_name` varchar(128) NOT NULL,
		  `name` varchar(128) NOT NULL,
		  `weight` int(11) NOT NULL,
		  PRIMARY KEY (`id`)
		) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=22 ;

CREATE TABLE IF NOT EXISTS `pages` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `date` date NOT NULL,
		  `title` text NOT NULL,
		  `content` longtext NOT NULL,
		  `weight` int(11) NOT NULL,
		  `header` int(11) NOT NULL,
		  PRIMARY KEY (`id`)
		) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=30 ;

CREATE TABLE IF NOT EXISTS `show_data` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `title` text NOT NULL,
		  `genre` text NOT NULL,
		  `secondary_genre` text NOT NULL,
		  `network` varchar(128) NOT NULL DEFAULT 'no_network',
		  `secondary_network` text NOT NULL,
		  `start_date` int(4) NOT NULL,
		  `end_date` int(4) NOT NULL,
		  PRIMARY KEY (`id`)
		) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=211 ;

CREATE TABLE IF NOT EXISTS `users` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `username` varchar(32) NOT NULL,
		  `password` varchar(96) NOT NULL,
		  `salt` varchar(96) NOT NULL,
		  `firstName` varchar(32) DEFAULT NULL,
		  `lastName` varchar(32) DEFAULT NULL,
		  `email` varchar(128) DEFAULT NULL,
		  `access` int(11) NOT NULL DEFAULT '0',
		  `uid` int(12) NOT NULL,
		  PRIMARY KEY (`id`)
		) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2682 ;

