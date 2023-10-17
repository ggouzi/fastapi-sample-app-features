USE test;

INSERT INTO roles(id, name) VALUES(1, 'admin');
INSERT INTO roles(id, name) VALUES(2, 'user');

INSERT INTO `users` VALUES
(1,'admin','48579d7e8e12ababfe72f731abd7482a616d7e79cacd22508d8e0e296ae906f44e6c7b870c6e182e22b5c068ce44c1ccff8a5b3e114b721da0bc79bf920ece08',1,1,'2023-10-15 15:07:04',NULL,'$2b$12$6gH9uwwk/Mpputs36FtQAu',NULL,NULL,NULL,NULL);

INSERT INTO versions(version, supported) VALUES("0.1", 0);
INSERT INTO versions(version, supported) VALUES("0.2", 0);
INSERT INTO versions(version, supported) VALUES("0.3", 0);
INSERT INTO versions(version, supported) VALUES("0.4", 0);
INSERT INTO versions(version, supported) VALUES("0.5", 0);
INSERT INTO versions(version, supported) VALUES("0.6", 0);
INSERT INTO versions(version, supported) VALUES("0.7", 0);
INSERT INTO versions(version, supported) VALUES("0.8", 0);
INSERT INTO versions(version, supported) VALUES("1.0", 1);
